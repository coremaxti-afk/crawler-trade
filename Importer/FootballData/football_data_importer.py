"""Controlled Football-Data odds importer.

Phase 1 only: staging-first import, dry-run, idempotent upserts and
validation. It does not download CSVs, create features/datasets/models, run
baselines, or alter SofaScore raw data.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.database import engine

SOURCE_NAME = "football-data"
DEFAULT_SOURCE_URL = "https://www.football-data.co.uk/mmz4281/2425/E0.csv"
REQUIRED_COLUMNS = {"Div", "Date", "Time", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"}

TEAM_NORMALIZATION = {
    "afc bournemouth": "bournemouth", "bournemouth": "bournemouth",
    "brighton": "brighton hove albion", "brighton & hove albion": "brighton hove albion",
    "ipswich": "ipswich town", "ipswich town": "ipswich town",
    "leicester": "leicester city", "leicester city": "leicester city",
    "liverpool": "liverpool", "liverpool fc": "liverpool",
    "man city": "manchester city", "manchester city": "manchester city",
    "man united": "manchester united", "manchester united": "manchester united",
    "newcastle": "newcastle united", "newcastle united": "newcastle united",
    "nott'm forest": "nottingham forest", "nottingham forest": "nottingham forest",
    "tottenham": "tottenham hotspur", "tottenham hotspur": "tottenham hotspur",
    "west ham": "west ham united", "west ham united": "west ham united",
    "wolves": "wolverhampton", "wolverhampton": "wolverhampton",
}


@dataclass
class CsvRow:
    row_number: int
    raw: dict[str, str]
    match_date: datetime | None
    home_team_raw: str | None
    away_team_raw: str | None
    home_team_normalized: str | None
    away_team_normalized: str | None
    home_goals: int | None
    away_goals: int | None
    result_raw: str | None


@dataclass
class MatchCandidate:
    match_id: int
    sofascore_event_id: int
    match_date: datetime | None
    home_team_normalized: str | None
    away_team_normalized: str | None
    home_goals: int | None
    away_goals: int | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import Football-Data CSV odds into PostgreSQL.")
    parser.add_argument("--csv", required=True)
    parser.add_argument("--season", required=True)
    parser.add_argument("--competition", required=True)
    parser.add_argument("--source-url", default=DEFAULT_SOURCE_URL)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--stage-only", action="store_true")
    parser.add_argument("--map-only", action="store_true")
    parser.add_argument("--odds-only", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    return parser.parse_args()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_team(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = " ".join(value.lower().replace(".", "").split())
    return TEAM_NORMALIZATION.get(normalized, normalized)


def parse_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_decimal(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return number if number > 0 else None


def parse_match_date(row: dict[str, str]) -> datetime | None:
    if not row.get("Date"):
        return None
    for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%y %H:%M"):
        try:
            return datetime.strptime(f"{row.get('Date')} {row.get('Time') or '00:00'}", fmt)
        except ValueError:
            pass
    return None


def read_csv_rows(csv_path: Path, limit: int | None) -> tuple[list[str], list[CsvRow]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames or []
        missing = sorted(REQUIRED_COLUMNS - set(fieldnames))
        if missing:
            raise ValueError(f"CSV missing required columns: {missing}")
        rows: list[CsvRow] = []
        for index, raw in enumerate(reader, start=1):
            if limit is not None and len(rows) >= limit:
                break
            home = raw.get("HomeTeam")
            away = raw.get("AwayTeam")
            rows.append(CsvRow(
                row_number=index,
                raw=dict(raw),
                match_date=parse_match_date(raw),
                home_team_raw=home,
                away_team_raw=away,
                home_team_normalized=normalize_team(home),
                away_team_normalized=normalize_team(away),
                home_goals=parse_int(raw.get("FTHG")),
                away_goals=parse_int(raw.get("FTAG")),
                result_raw=raw.get("FTR"),
            ))
    return fieldnames, rows


def run_mode(args: argparse.Namespace) -> str:
    selected = [args.stage_only, args.map_only, args.odds_only, args.all]
    if sum(1 for value in selected if value) > 1:
        raise ValueError("Use only one mode flag.")
    if args.stage_only:
        return "stage-only"
    if args.map_only:
        return "map-only"
    if args.odds_only:
        return "odds-only"
    return "all"


def load_matches(conn) -> list[MatchCandidate]:
    rows = conn.execute(text("""
        select match_id, sofascore_event_id, match_date, home_team, away_team, home_goals, away_goals
        from matches_master
        where sofascore_event_id is not null
        order by match_date, match_id
    """)).mappings().all()
    return [MatchCandidate(
        match_id=int(row["match_id"]),
        sofascore_event_id=int(row["sofascore_event_id"]),
        match_date=row["match_date"],
        home_team_normalized=normalize_team(row["home_team"]),
        away_team_normalized=normalize_team(row["away_team"]),
        home_goals=row["home_goals"],
        away_goals=row["away_goals"],
    ) for row in rows]


def map_row(row: CsvRow, matches: list[MatchCandidate]) -> dict[str, Any]:
    candidates = [m for m in matches
        if m.home_team_normalized == row.home_team_normalized
        and m.away_team_normalized == row.away_team_normalized
        and m.home_goals == row.home_goals
        and m.away_goals == row.away_goals]
    if row.match_date is not None:
        candidates = [m for m in candidates if m.match_date is None or abs((m.match_date.date() - row.match_date.date()).days) <= 1]
    if len(candidates) == 1:
        m = candidates[0]
        return {"mapping_status": "mapped", "mapping_method": "normalized_teams_score_date", "match_id": m.match_id,
                "sofascore_event_id": m.sofascore_event_id, "score_check_status": "score_match",
                "ambiguity_flag": False, "conflict_reason": None}
    if len(candidates) > 1:
        return {"mapping_status": "ambiguous", "mapping_method": "normalized_teams_score_date", "match_id": None,
                "sofascore_event_id": None, "score_check_status": None, "ambiguity_flag": True,
                "conflict_reason": f"{len(candidates)} candidates"}
    return {"mapping_status": "unmapped", "mapping_method": "normalized_teams_score_date", "match_id": None,
            "sofascore_event_id": None, "score_check_status": None, "ambiguity_flag": False, "conflict_reason": "no candidate"}


def bookmaker_from_prefix(prefix: str) -> tuple[str, str, bool, bool, bool, bool]:
    is_closing = prefix in {"PC", "PSC", "B365C", "BWC", "BFC", "WHC", "1XBC", "BFEC", "MaxC", "AvgC"} or ("C" in prefix and prefix != "PC")
    clean = prefix.replace("C", "") if prefix != "PC" else "P"
    if prefix == "MaxC":
        return "MaxC", "maximum", is_closing, False, False, True
    if prefix == "AvgC":
        return "AvgC", "average", is_closing, False, True, False
    if prefix.startswith("Max"):
        return "Max", "maximum", is_closing, False, False, True
    if prefix.startswith("Avg"):
        return "Avg", "average", is_closing, False, True, False
    return clean, "closing" if is_closing else "opening_like", is_closing, not is_closing, False, False


def add_odd(odds: list[dict[str, Any]], row: CsvRow, source_hash: str, csv_path: Path, source_url: str,
            market: str, selection: str, handicap_line: str | None, source_column: str, prefix: str, value: str | None) -> None:
    odds_value = parse_decimal(value)
    if odds_value is None:
        return
    bookmaker, odds_type, is_closing, is_opening_like, is_average, is_maximum = bookmaker_from_prefix(prefix)
    semantics = "football_data_c_column_candidate_closing" if is_closing else "football_data_non_c_column_preserved_as_opening_like_candidate"
    if is_average:
        semantics = "football_data_average_odds"
    if is_maximum:
        semantics = "football_data_maximum_odds"
    odds.append({
        "source_hash": source_hash, "source_file": str(csv_path), "source_url": source_url, "row_number": row.row_number,
        "market": market, "selection": selection, "handicap_line": handicap_line, "handicap_line_key": handicap_line or "",
        "odds_type": odds_type, "bookmaker_or_aggregator": bookmaker, "odds_value": odds_value,
        "source_column": source_column, "source_column_semantics": semantics, "is_closing": is_closing,
        "is_opening_like": is_opening_like, "is_average": is_average, "is_maximum": is_maximum,
    })


def extract_odds(row: CsvRow, source_hash: str, csv_path: Path, source_url: str) -> list[dict[str, Any]]:
    raw = row.raw
    odds: list[dict[str, Any]] = []
    for prefix in ("B365", "BW", "BF", "PS", "WH", "1XB", "Max", "Avg", "BFE"):
        for suffix, selection in (("H", "home_win"), ("D", "draw"), ("A", "away_win")):
            add_odd(odds, row, source_hash, csv_path, source_url, "match_odds_1x2", selection, None, f"{prefix}{suffix}", prefix, raw.get(f"{prefix}{suffix}"))
    for prefix in ("B365C", "BWC", "BFC", "PSC", "WHC", "1XBC", "MaxC", "AvgC", "BFEC"):
        for suffix, selection in (("H", "home_win"), ("D", "draw"), ("A", "away_win")):
            add_odd(odds, row, source_hash, csv_path, source_url, "match_odds_1x2", selection, None, f"{prefix}{suffix}", prefix, raw.get(f"{prefix}{suffix}"))
    for prefix, over_col, under_col in (
        ("B365", "B365>2.5", "B365<2.5"), ("P", "P>2.5", "P<2.5"), ("Max", "Max>2.5", "Max<2.5"),
        ("Avg", "Avg>2.5", "Avg<2.5"), ("BFE", "BFE>2.5", "BFE<2.5"), ("B365C", "B365C>2.5", "B365C<2.5"),
        ("PC", "PC>2.5", "PC<2.5"), ("MaxC", "MaxC>2.5", "MaxC<2.5"), ("AvgC", "AvgC>2.5", "AvgC<2.5"),
        ("BFEC", "BFEC>2.5", "BFEC<2.5")):
        add_odd(odds, row, source_hash, csv_path, source_url, "over_under_2_5", "over_2_5", None, over_col, prefix, raw.get(over_col))
        add_odd(odds, row, source_hash, csv_path, source_url, "over_under_2_5", "under_2_5", None, under_col, prefix, raw.get(under_col))
    for line_col, entries in (("AHh", (("B365", "B365AHH", "B365AHA"), ("P", "PAHH", "PAHA"), ("Max", "MaxAHH", "MaxAHA"), ("Avg", "AvgAHH", "AvgAHA"), ("BFE", "BFEAHH", "BFEAHA"))),
                              ("AHCh", (("B365C", "B365CAHH", "B365CAHA"), ("PC", "PCAHH", "PCAHA"), ("MaxC", "MaxCAHH", "MaxCAHA"), ("AvgC", "AvgCAHH", "AvgCAHA"), ("BFEC", "BFECAHH", "BFECAHA")))):
        handicap_line = raw.get(line_col) or None
        for prefix, home_col, away_col in entries:
            add_odd(odds, row, source_hash, csv_path, source_url, "asian_handicap", "home_handicap", handicap_line, home_col, prefix, raw.get(home_col))
            add_odd(odds, row, source_hash, csv_path, source_url, "asian_handicap", "away_handicap", handicap_line, away_col, prefix, raw.get(away_col))
    return odds


def register_csv_file(conn, csv_path: Path, source_hash: str, args: argparse.Namespace, row_count: int) -> int:
    return conn.execute(text("""
        insert into football_data_csv_files (competition_code, season, source_name, source_url, source_file, source_hash, registered_at, row_count, notes)
        values (:competition_code, :season, :source_name, :source_url, :source_file, :source_hash, :registered_at, :row_count, :notes)
        on conflict (source_hash) do update set competition_code=excluded.competition_code, season=excluded.season,
            source_name=excluded.source_name, source_url=excluded.source_url, source_file=excluded.source_file, row_count=excluded.row_count
        returning id
    """), {"competition_code": args.competition, "season": args.season, "source_name": SOURCE_NAME, "source_url": args.source_url,
           "source_file": str(csv_path), "source_hash": source_hash, "registered_at": utc_now(), "row_count": row_count,
           "notes": "football-data phase 1 controlled importer"}).scalar_one()


def import_staging_rows(conn, csv_file_id: int, source_hash: str, rows: list[CsvRow]) -> dict[int, int]:
    ids: dict[int, int] = {}
    sql = text("""
        insert into football_data_staging_rows (csv_file_id, source_hash, row_number, raw_row_json, division, match_date, home_team_raw, away_team_raw, home_goals, away_goals, result_raw, created_at)
        values (:csv_file_id, :source_hash, :row_number, cast(:raw_row_json as jsonb), :division, :match_date, :home_team_raw, :away_team_raw, :home_goals, :away_goals, :result_raw, :created_at)
        on conflict (source_hash, row_number) do update set csv_file_id=excluded.csv_file_id, raw_row_json=excluded.raw_row_json,
            division=excluded.division, match_date=excluded.match_date, home_team_raw=excluded.home_team_raw, away_team_raw=excluded.away_team_raw,
            home_goals=excluded.home_goals, away_goals=excluded.away_goals, result_raw=excluded.result_raw
        returning id
    """)
    for row in rows:
        ids[row.row_number] = int(conn.execute(sql, {"csv_file_id": csv_file_id, "source_hash": source_hash, "row_number": row.row_number,
            "raw_row_json": json.dumps(row.raw, ensure_ascii=False), "division": row.raw.get("Div"), "match_date": row.match_date,
            "home_team_raw": row.home_team_raw, "away_team_raw": row.away_team_raw, "home_goals": row.home_goals,
            "away_goals": row.away_goals, "result_raw": row.result_raw, "created_at": utc_now()}).scalar_one())
    return ids


def import_mapping_rows(conn, source_hash: str, rows: list[CsvRow], staging_ids: dict[int, int], matches: list[MatchCandidate]) -> dict[int, int]:
    ids: dict[int, int] = {}
    sql = text("""
        insert into football_data_match_mapping (staging_row_id, source_hash, row_number, sofascore_event_id, match_id, mapping_status,
            mapping_method, home_team_normalized, away_team_normalized, score_check_status, ambiguity_flag, conflict_reason, mapped_at)
        values (:staging_row_id, :source_hash, :row_number, :sofascore_event_id, :match_id, :mapping_status,
            :mapping_method, :home_team_normalized, :away_team_normalized, :score_check_status, :ambiguity_flag, :conflict_reason, :mapped_at)
        on conflict (source_hash, row_number) do update set staging_row_id=excluded.staging_row_id, sofascore_event_id=excluded.sofascore_event_id,
            match_id=excluded.match_id, mapping_status=excluded.mapping_status, mapping_method=excluded.mapping_method,
            home_team_normalized=excluded.home_team_normalized, away_team_normalized=excluded.away_team_normalized,
            score_check_status=excluded.score_check_status, ambiguity_flag=excluded.ambiguity_flag, conflict_reason=excluded.conflict_reason, mapped_at=excluded.mapped_at
        returning id
    """)
    for row in rows:
        staging_id = staging_ids.get(row.row_number) or conn.execute(text("select id from football_data_staging_rows where source_hash=:source_hash and row_number=:row_number"), {"source_hash": source_hash, "row_number": row.row_number}).scalar_one()
        mapping = map_row(row, matches)
        ids[row.row_number] = int(conn.execute(sql, {"staging_row_id": staging_id, "source_hash": source_hash, "row_number": row.row_number,
            **mapping, "home_team_normalized": row.home_team_normalized, "away_team_normalized": row.away_team_normalized, "mapped_at": utc_now()}).scalar_one())
    return ids


def mapped_rows(conn, source_hash: str) -> dict[int, dict[str, Any]]:
    rows = conn.execute(text("""
        select id, staging_row_id, row_number, match_id, sofascore_event_id, mapping_status
        from football_data_match_mapping where source_hash=:source_hash
    """), {"source_hash": source_hash}).mappings().all()
    return {int(row["row_number"]): dict(row) for row in rows}


def import_odds(conn, source_hash: str, rows: list[CsvRow], csv_path: Path, source_url: str) -> dict[str, int]:
    mappings = mapped_rows(conn, source_hash)
    summary = {"odds_inserted": 0, "odds_updated": 0, "rows_without_mapping": 0, "rows_not_mapped": 0}
    exists_sql = text("""select id from football_data_odds where sofascore_event_id=:sofascore_event_id and market=:market and selection=:selection
        and handicap_line_key=:handicap_line_key and odds_type=:odds_type and bookmaker_or_aggregator=:bookmaker_or_aggregator and source_hash=:source_hash limit 1""")
    upsert_sql = text("""
        insert into football_data_odds (staging_row_id, mapping_id, match_id, sofascore_event_id, source_hash, source_file, source_url, row_number,
            market, selection, handicap_line, handicap_line_key, odds_type, bookmaker_or_aggregator, odds_value, source_column, source_column_semantics,
            is_closing, is_opening_like, is_average, is_maximum, imported_at)
        values (:staging_row_id, :mapping_id, :match_id, :sofascore_event_id, :source_hash, :source_file, :source_url, :row_number,
            :market, :selection, :handicap_line, :handicap_line_key, :odds_type, :bookmaker_or_aggregator, :odds_value, :source_column,
            :source_column_semantics, :is_closing, :is_opening_like, :is_average, :is_maximum, :imported_at)
        on conflict (sofascore_event_id, market, selection, handicap_line_key, odds_type, bookmaker_or_aggregator, source_hash) do update set
            staging_row_id=excluded.staging_row_id, mapping_id=excluded.mapping_id, match_id=excluded.match_id, source_file=excluded.source_file,
            source_url=excluded.source_url, row_number=excluded.row_number, handicap_line=excluded.handicap_line, odds_value=excluded.odds_value,
            source_column=excluded.source_column, source_column_semantics=excluded.source_column_semantics, is_closing=excluded.is_closing,
            is_opening_like=excluded.is_opening_like, is_average=excluded.is_average, is_maximum=excluded.is_maximum, imported_at=excluded.imported_at
    """)
    for row in rows:
        mapping = mappings.get(row.row_number)
        if mapping is None:
            summary["rows_without_mapping"] += 1
            continue
        if mapping["mapping_status"] != "mapped":
            summary["rows_not_mapped"] += 1
            continue
        for odd in extract_odds(row, source_hash, csv_path, source_url):
            values = {**odd, "staging_row_id": mapping["staging_row_id"], "mapping_id": mapping["id"], "match_id": mapping["match_id"],
                      "sofascore_event_id": mapping["sofascore_event_id"], "imported_at": utc_now()}
            exists = conn.execute(exists_sql, values).scalar_one_or_none()
            conn.execute(upsert_sql, values)
            summary["odds_updated" if exists else "odds_inserted"] += 1
    return summary


def validate_import(conn, source_hash: str) -> dict[str, Any]:
    validation = {}
    for name, query in {
        "csv_files": "select count(*) from football_data_csv_files where source_hash=:source_hash",
        "staging_rows": "select count(*) from football_data_staging_rows where source_hash=:source_hash",
        "mapping_rows": "select count(*) from football_data_match_mapping where source_hash=:source_hash",
        "odds_rows": "select count(*) from football_data_odds where source_hash=:source_hash",
        "invalid_odds": "select count(*) from football_data_odds where source_hash=:source_hash and odds_value <= 0",
    }.items():
        validation[name] = conn.execute(text(query), {"source_hash": source_hash}).scalar_one()
    validation["mapping_status"] = dict(conn.execute(text("select mapping_status, count(*) from football_data_match_mapping where source_hash=:source_hash group by mapping_status order by mapping_status"), {"source_hash": source_hash}).all())
    validation["odds_by_market"] = dict(conn.execute(text("select market, count(*) from football_data_odds where source_hash=:source_hash group by market order by market"), {"source_hash": source_hash}).all())
    validation["odds_by_type"] = dict(conn.execute(text("select odds_type, count(*) from football_data_odds where source_hash=:source_hash group by odds_type order by odds_type"), {"source_hash": source_hash}).all())
    validation["odds_by_bookmaker_or_aggregator"] = dict(conn.execute(text("select bookmaker_or_aggregator, count(*) from football_data_odds where source_hash=:source_hash group by bookmaker_or_aggregator order by bookmaker_or_aggregator"), {"source_hash": source_hash}).all())
    validation["duplicate_odds_grain"] = conn.execute(text("""
        select count(*) from (select sofascore_event_id, market, selection, handicap_line_key, odds_type, bookmaker_or_aggregator, source_hash, count(*)
        from football_data_odds where source_hash=:source_hash group by sofascore_event_id, market, selection, handicap_line_key, odds_type, bookmaker_or_aggregator, source_hash having count(*) > 1) d
    """), {"source_hash": source_hash}).scalar_one()
    validation["orphan_odds"] = conn.execute(text("""
        select count(*) from football_data_odds o left join football_data_match_mapping m on m.id=o.mapping_id left join football_data_staging_rows s on s.id=o.staging_row_id
        where o.source_hash=:source_hash and (m.id is null or s.id is null)
    """), {"source_hash": source_hash}).scalar_one()
    return validation


def dry_run_summary(rows: list[CsvRow], matches: list[MatchCandidate], fieldnames: list[str], source_hash: str, csv_path: Path, source_url: str) -> dict[str, Any]:
    mappings = [map_row(row, matches) for row in rows]
    odds = [odd for row in rows for odd in extract_odds(row, source_hash, csv_path, source_url)]
    return {"source_hash": source_hash, "processed_rows": len(rows), "columns": len(fieldnames),
            "mapping_status": dict(Counter(m["mapping_status"] for m in mappings)), "estimated_odds": len(odds),
            "estimated_odds_by_market": dict(Counter(o["market"] for o in odds)),
            "estimated_odds_by_type": dict(Counter(o["odds_type"] for o in odds)),
            "estimated_odds_by_bookmaker_or_aggregator": dict(Counter(o["bookmaker_or_aggregator"] for o in odds)),
            "dry_run": True, "database_writes": 0}


def main() -> None:
    args = parse_args()
    mode = run_mode(args)
    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")
    started_at = utc_now()
    source_hash = file_hash(csv_path)
    fieldnames, rows = read_csv_rows(csv_path, args.limit)
    with engine.begin() as conn:
        matches = load_matches(conn)
    if args.dry_run:
        summary = dry_run_summary(rows, matches, fieldnames, source_hash, csv_path, args.source_url)
        summary["started_at"] = started_at.isoformat()
        summary["finished_at"] = utc_now().isoformat()
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return
    summary: dict[str, Any] = {"mode": mode, "source_hash": source_hash, "source_file": str(csv_path), "started_at": started_at.isoformat(),
        "processed_rows": len(rows), "staged_rows": 0, "mapped_rows": 0, "unmapped_rows": 0, "odds_inserted": 0, "odds_updated": 0, "failed_rows": 0}
    with engine.begin() as conn:
        staging_ids: dict[int, int] = {}
        if mode in {"all", "stage-only"}:
            csv_file_id = register_csv_file(conn, csv_path, source_hash, args, len(rows))
            staging_ids = import_staging_rows(conn, csv_file_id, source_hash, rows)
            summary["staged_rows"] = len(staging_ids)
        if mode in {"all", "map-only"}:
            mapping_ids = import_mapping_rows(conn, source_hash, rows, staging_ids, matches)
            summary["mapped_rows"] = len(mapping_ids)
        if mode in {"all", "odds-only"}:
            odds_summary = import_odds(conn, source_hash, rows, csv_path, args.source_url)
            summary.update(odds_summary)
        validation = validate_import(conn, source_hash)
    summary["validation"] = validation
    summary["finished_at"] = utc_now().isoformat()
    if validation.get("mapping_status"):
        summary["unmapped_rows"] = sum(c for s, c in validation["mapping_status"].items() if s != "mapped")
    print(json.dumps(summary, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
