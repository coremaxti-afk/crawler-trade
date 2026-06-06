"""Importer H8 SofaScore graph/shotmap raw artifacts.

Imports already collected raw files into PostgreSQL. It does not collect data,
create features, build datasets, run baselines, or modify raw JSON files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.database import engine

SOURCE_NAME = "sofascore"
GRAPH_ARTIFACT = "graph.json"
SHOTMAP_ARTIFACT = "shotmap.json"
KNOWN_GRAPH_MISSING_EVENT_ID = 12437015
KNOWN_GRAPH_MISSING_REASON = "HTTP 404 confirmado no endpoint /graph"
KNOWN_GRAPH_MISSING_DECISION = "keep_match_exclude_graph_required_outputs"
RAW_ROOT_CANDIDATES = [
    PROJECT_ROOT / "Crawler" / "Sofascore" / "data" / "raw" / "sofascore" / "premier_league_61627" / "matches",
    PROJECT_ROOT / "data" / "raw" / "sofascore" / "premier_league_61627" / "matches",
]
SCHEMA_FILE = PROJECT_ROOT / "database" / "migrations" / "20260606_create_h8_storage_tables.sql"


class H8ImportError(Exception):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import SofaScore H8 graph/shotmap raw artifacts into PostgreSQL.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--graph", action="store_true", help="Import graph.json only.")
    group.add_argument("--shotmap", action="store_true", help="Import shotmap.json only.")
    group.add_argument("--all", action="store_true", help="Import graph.json and shotmap.json.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and summarize without writing to the database.")
    parser.add_argument("--raw-root", default=None, help="Optional matches/{event_id} raw directory.")
    parser.add_argument("--create-schema", action="store_true", help="Apply the H8 schema SQL before importing.")
    parser.add_argument("--limit", type=int, default=None, help="Optional limit for local validation runs.")
    return parser.parse_args()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def resolve_raw_root(raw_root_arg: str | None = None) -> Path:
    candidates = [Path(raw_root_arg)] if raw_root_arg else RAW_ROOT_CANDIDATES
    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate
    checked = ", ".join(str(path) for path in candidates)
    raise FileNotFoundError(f"Raw root not found. Checked: {checked}")


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def as_json(value: Any) -> str | None:
    if value is None:
        return None
    return json.dumps(value, ensure_ascii=False)


def to_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def apply_schema() -> None:
    if not SCHEMA_FILE.exists():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_FILE}")
    sql = SCHEMA_FILE.read_text(encoding="utf-8-sig")
    with engine.begin() as conn:
        conn.execute(text(sql))


def load_matches(conn) -> list[dict[str, Any]]:
    rows = conn.execute(text("""
        select match_id, sofascore_event_id, home_team, away_team
        from matches_master
        where sofascore_event_id is not null
        order by sofascore_event_id
    """)).mappings().all()
    return [dict(row) for row in rows]


def graph_points(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict) or not isinstance(payload.get("graphPoints"), list):
        raise H8ImportError("graph payload missing graphPoints list")
    points = payload["graphPoints"]
    for index, point in enumerate(points):
        if not isinstance(point, dict):
            raise H8ImportError(f"graph point {index} is not an object")
        if point.get("minute") is None or point.get("value") is None:
            raise H8ImportError(f"graph point {index} missing minute/value")
    return points


def shotmap_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("shotmap"), list):
        items = payload["shotmap"]
    elif isinstance(payload, list):
        items = payload
    else:
        raise H8ImportError("shotmap payload missing shotmap list")
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise H8ImportError(f"shotmap item {index} is not an object")
    return items


def graph_row(match: dict[str, Any], point: dict[str, Any], point_index: int, raw_path: Path, raw_hash: str, imported_at: datetime) -> dict[str, Any]:
    return {
        "match_id": match["match_id"],
        "sofascore_event_id": int(match["sofascore_event_id"]),
        "point_index": point_index,
        "minute": to_int(point.get("minute")),
        "momentum_value": to_float(point.get("value")),
        "source_name": SOURCE_NAME,
        "artifact_name": GRAPH_ARTIFACT,
        "raw_file_path": str(raw_path),
        "raw_payload_hash": raw_hash,
        "imported_at": imported_at,
    }


def shotmap_row(match: dict[str, Any], item: dict[str, Any], shot_index: int, raw_path: Path, raw_hash: str, imported_at: datetime) -> dict[str, Any]:
    player = item.get("player") if isinstance(item.get("player"), dict) else {}
    is_home = item.get("isHome")
    if is_home is True:
        team_name = match.get("home_team")
    elif is_home is False:
        team_name = match.get("away_team")
    else:
        team_name = None
    team = item.get("team") if isinstance(item.get("team"), dict) else {}
    return {
        "sofascore_event_id": int(match["sofascore_event_id"]),
        "shot_index": shot_index,
        "minute": to_int(item.get("time") if item.get("time") is not None else item.get("minute")),
        "added_time": to_int(item.get("addedTime")),
        "time_seconds": to_int(item.get("timeSeconds")),
        "team_id": to_int(team.get("id")),
        "team_name": team.get("name") or team_name,
        "player_id": to_int(player.get("id")),
        "player_name": player.get("name"),
        "shot_type": item.get("shotType"),
        "goal_mouth_location": item.get("goalMouthLocation"),
        "xg": to_float(item.get("xg")),
        "xgot": to_float(item.get("xgot")),
        "player_coordinates_json": as_json(item.get("playerCoordinates")),
        "goal_mouth_coordinates_json": as_json(item.get("goalMouthCoordinates")),
        "draw_json": as_json(item.get("draw")),
        "source_name": SOURCE_NAME,
        "artifact_name": SHOTMAP_ARTIFACT,
        "raw_file_path": str(raw_path),
        "raw_payload_hash": raw_hash,
        "imported_at": imported_at,
    }


def upsert_graph_rows(conn, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    conn.execute(text("""
        insert into match_graph (
            match_id, sofascore_event_id, point_index, minute, momentum_value,
            source_name, artifact_name, raw_file_path, raw_payload_hash, imported_at
        ) values (
            :match_id, :sofascore_event_id, :point_index, :minute, :momentum_value,
            :source_name, :artifact_name, :raw_file_path, :raw_payload_hash, :imported_at
        )
        on conflict (sofascore_event_id, point_index) do update set
            match_id = excluded.match_id,
            minute = excluded.minute,
            momentum_value = excluded.momentum_value,
            source_name = excluded.source_name,
            artifact_name = excluded.artifact_name,
            raw_file_path = excluded.raw_file_path,
            raw_payload_hash = excluded.raw_payload_hash,
            imported_at = excluded.imported_at
    """), rows)


def upsert_shotmap_rows(conn, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    conn.execute(text("""
        insert into match_shotmap (
            sofascore_event_id, shot_index, minute, added_time, time_seconds,
            team_id, team_name, player_id, player_name, shot_type, goal_mouth_location,
            xg, xgot, player_coordinates_json, goal_mouth_coordinates_json, draw_json,
            source_name, artifact_name, raw_file_path, raw_payload_hash, imported_at
        ) values (
            :sofascore_event_id, :shot_index, :minute, :added_time, :time_seconds,
            :team_id, :team_name, :player_id, :player_name, :shot_type, :goal_mouth_location,
            :xg, :xgot, cast(:player_coordinates_json as jsonb), cast(:goal_mouth_coordinates_json as jsonb), cast(:draw_json as jsonb),
            :source_name, :artifact_name, :raw_file_path, :raw_payload_hash, :imported_at
        )
        on conflict (sofascore_event_id, shot_index) do update set
            minute = excluded.minute,
            added_time = excluded.added_time,
            time_seconds = excluded.time_seconds,
            team_id = excluded.team_id,
            team_name = excluded.team_name,
            player_id = excluded.player_id,
            player_name = excluded.player_name,
            shot_type = excluded.shot_type,
            goal_mouth_location = excluded.goal_mouth_location,
            xg = excluded.xg,
            xgot = excluded.xgot,
            player_coordinates_json = excluded.player_coordinates_json,
            goal_mouth_coordinates_json = excluded.goal_mouth_coordinates_json,
            draw_json = excluded.draw_json,
            source_name = excluded.source_name,
            artifact_name = excluded.artifact_name,
            raw_file_path = excluded.raw_file_path,
            raw_payload_hash = excluded.raw_payload_hash,
            imported_at = excluded.imported_at
    """), rows)


def import_source_status(conn, match: dict[str, Any], artifact_name: str, status: str, *, http_status: int | None = None, decision: str | None = None, reason: str | None = None, raw_file_path: str | None = None, raw_payload_hash: str | None = None, dry_run: bool = False) -> None:
    if dry_run:
        return
    conn.execute(text("""
        insert into match_source_status (
            sofascore_event_id, source_name, artifact_name, status, http_status,
            decision, reason, raw_file_path, raw_payload_hash, checked_at
        ) values (
            :sofascore_event_id, :source_name, :artifact_name, :status, :http_status,
            :decision, :reason, :raw_file_path, :raw_payload_hash, :checked_at
        )
        on conflict (sofascore_event_id, source_name, artifact_name) do update set
            status = excluded.status,
            http_status = excluded.http_status,
            decision = excluded.decision,
            reason = excluded.reason,
            raw_file_path = excluded.raw_file_path,
            raw_payload_hash = excluded.raw_payload_hash,
            checked_at = excluded.checked_at
    """), {
        "sofascore_event_id": int(match["sofascore_event_id"]),
        "source_name": SOURCE_NAME,
        "artifact_name": artifact_name,
        "status": status,
        "http_status": http_status,
        "decision": decision,
        "reason": reason,
        "raw_file_path": raw_file_path,
        "raw_payload_hash": raw_payload_hash,
        "checked_at": utc_now(),
    })


def import_graph(conn, matches: list[dict[str, Any]], raw_root: Path, dry_run: bool = False) -> dict[str, int]:
    summary = {"valid": 0, "known_missing": 0, "missing": 0, "invalid": 0, "points": 0}
    for match in matches:
        event_id = int(match["sofascore_event_id"])
        path = raw_root / str(event_id) / GRAPH_ARTIFACT
        if event_id == KNOWN_GRAPH_MISSING_EVENT_ID and not path.exists():
            summary["known_missing"] += 1
            import_source_status(
                conn, match, GRAPH_ARTIFACT, "known_missing",
                http_status=404,
                decision=KNOWN_GRAPH_MISSING_DECISION,
                reason=KNOWN_GRAPH_MISSING_REASON,
                dry_run=dry_run,
            )
            continue
        if not path.exists():
            summary["missing"] += 1
            import_source_status(conn, match, GRAPH_ARTIFACT, "missing", reason="graph.json not found", dry_run=dry_run)
            continue
        raw_hash = file_hash(path)
        try:
            payload = load_json(path)
            points = graph_points(payload)
        except Exception as error:
            summary["invalid"] += 1
            import_source_status(conn, match, GRAPH_ARTIFACT, "invalid_raw", reason=str(error), raw_file_path=str(path), raw_payload_hash=raw_hash, dry_run=dry_run)
            continue
        rows = [graph_row(match, point, index, path, raw_hash, utc_now()) for index, point in enumerate(points)]
        if not dry_run:
            upsert_graph_rows(conn, rows)
        import_source_status(conn, match, GRAPH_ARTIFACT, "imported", raw_file_path=str(path), raw_payload_hash=raw_hash, dry_run=dry_run)
        summary["valid"] += 1
        summary["points"] += len(rows)
    return summary


def import_shotmap(conn, matches: list[dict[str, Any]], raw_root: Path, dry_run: bool = False) -> dict[str, int]:
    summary = {"valid": 0, "missing": 0, "invalid": 0, "shots": 0}
    for match in matches:
        event_id = int(match["sofascore_event_id"])
        path = raw_root / str(event_id) / SHOTMAP_ARTIFACT
        if not path.exists():
            summary["missing"] += 1
            import_source_status(conn, match, SHOTMAP_ARTIFACT, "missing", reason="shotmap.json not found", dry_run=dry_run)
            continue
        raw_hash = file_hash(path)
        try:
            payload = load_json(path)
            items = shotmap_items(payload)
        except Exception as error:
            summary["invalid"] += 1
            import_source_status(conn, match, SHOTMAP_ARTIFACT, "invalid_raw", reason=str(error), raw_file_path=str(path), raw_payload_hash=raw_hash, dry_run=dry_run)
            continue
        rows = [shotmap_row(match, item, index, path, raw_hash, utc_now()) for index, item in enumerate(items)]
        if not dry_run:
            upsert_shotmap_rows(conn, rows)
        import_source_status(conn, match, SHOTMAP_ARTIFACT, "imported", raw_file_path=str(path), raw_payload_hash=raw_hash, dry_run=dry_run)
        summary["valid"] += 1
        summary["shots"] += len(rows)
    return summary


def print_summary(name: str, summary: dict[str, int]) -> None:
    print(f"\n{name.upper()} SUMMARY")
    for key, value in summary.items():
        print(f"{key}: {value}")


def main() -> None:
    args = parse_args()
    raw_root = resolve_raw_root(args.raw_root)
    if args.create_schema:
        if args.dry_run:
            print(f"DRY-RUN: would apply schema {SCHEMA_FILE}")
        else:
            apply_schema()
            print(f"Applied schema: {SCHEMA_FILE}")

    with engine.begin() as conn:
        matches = load_matches(conn)
        if args.limit is not None:
            matches = matches[:args.limit]
        print(f"Raw root: {raw_root}")
        print(f"Matches from matches_master: {len(matches)}")
        if args.dry_run:
            print("DRY-RUN: no database writes will be executed.")
        if args.graph or args.all:
            print_summary("graph", import_graph(conn, matches, raw_root, dry_run=args.dry_run))
        if args.shotmap or args.all:
            print_summary("shotmap", import_shotmap(conn, matches, raw_root, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
