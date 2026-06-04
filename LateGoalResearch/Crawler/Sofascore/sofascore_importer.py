import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.database import engine

RAW_ROOT_CANDIDATES = [
    Path("data/raw/sofascore/premier_league_61627/matches"),
    Path(__file__).resolve().parent / "data/raw/sofascore/premier_league_61627/matches",
]
CORE_FILES = ("event.json", "statistics.json", "incidents.json")
FULL_FILES = CORE_FILES + ("lineups.json", "h2h.json")
KNOWN_SKIPPED_MATCH_IDS = {"12436452"}
LEAGUE_NAME = "Premier League"
SEASON_NAME = "2024/25"


class ImportErrorForMatch(Exception):
    pass


def parse_args():
    parser = argparse.ArgumentParser(description="Importa JSONs SofaScore EPL para PostgreSQL.")
    parser.add_argument("--dry-run", action="store_true", help="Classifica partidas sem gravar no banco.")
    parser.add_argument("--limit", type=int, default=None, help="Limita partidas importaveis processadas.")
    parser.add_argument("--raw-root", default=None, help="Diretorio matches/{event_id}. Opcional.")
    return parser.parse_args()


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def resolve_raw_root(raw_root_arg=None):
    candidates = [Path(raw_root_arg)] if raw_root_arg else RAW_ROOT_CANDIDATES
    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate
    checked = ", ".join(str(path) for path in candidates)
    raise FileNotFoundError(f"Diretorio raw nao encontrado. Verificado: {checked}")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def classify_match(match_dir):
    existing = {path.name for path in match_dir.iterdir() if path.is_file()}
    has_core = all(filename in existing for filename in CORE_FILES)
    has_full = all(filename in existing for filename in FULL_FILES)
    if has_full:
        return "full"
    if has_core:
        return "core"
    return "incomplete"


def discover_matches(raw_root):
    rows = []
    for match_dir in sorted((p for p in raw_root.iterdir() if p.is_dir()), key=lambda p: p.name):
        event_id = match_dir.name
        classification = classify_match(match_dir)
        if event_id in KNOWN_SKIPPED_MATCH_IDS:
            status = "known_skipped"
        elif classification in {"full", "core"}:
            status = "importable"
        else:
            status = "incomplete"
        rows.append({"event_id": event_id, "dir": match_dir, "classification": classification, "status": status})
    return rows


def safe_get(data, *keys):
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def parse_timestamp(value):
    if value is None:
        return None
    return datetime.fromtimestamp(value, tz=timezone.utc).replace(tzinfo=None)


def parse_event(event_payload, event_id):
    event = event_payload.get("event", event_payload)
    home_score = safe_get(event, "homeScore", "current")
    away_score = safe_get(event, "awayScore", "current")
    season = safe_get(event, "season", "year") or SEASON_NAME
    league = safe_get(event, "tournament", "uniqueTournament", "name") or safe_get(event, "tournament", "name") or LEAGUE_NAME
    return {
        "sofascore_event_id": int(event.get("id") or event_id),
        "league": league,
        "season": season,
        "match_date": parse_timestamp(event.get("startTimestamp")),
        "home_team": safe_get(event, "homeTeam", "name"),
        "away_team": safe_get(event, "awayTeam", "name"),
        "home_goals": home_score,
        "away_goals": away_score,
    }


def iter_stat_items(value):
    if isinstance(value, dict):
        if isinstance(value.get("statisticsItems"), list):
            for item in value["statisticsItems"]:
                yield item
        for child in value.values():
            yield from iter_stat_items(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_stat_items(child)


def numeric_value(value):
    if value is None:
        return None
    if isinstance(value, str):
        value = value.replace("%", "").strip()
        if value == "":
            return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def integer_value(value):
    number = numeric_value(value)
    if number is None:
        return None
    return int(round(number))


def extract_stat(stat_payload, keys):
    key_set = {key.lower() for key in keys}
    for item in iter_stat_items(stat_payload):
        item_key = str(item.get("key") or "").lower()
        item_name = str(item.get("name") or "").lower()
        if item_key in key_set or item_name in key_set:
            return numeric_value(item.get("homeValue") if "homeValue" in item else item.get("home")), numeric_value(item.get("awayValue") if "awayValue" in item else item.get("away"))
    return None, None


def parse_statistics(stat_payload, event_id, match_id):
    possession_home, possession_away = extract_stat(stat_payload, ["ballPossession", "Ball possession"])
    shots_home, shots_away = extract_stat(stat_payload, ["totalShots", "Total shots"])
    sot_home, sot_away = extract_stat(stat_payload, ["shotsOnGoal", "Shots on target"])
    corners_home, corners_away = extract_stat(stat_payload, ["cornerKicks", "Corner kicks"])
    big_home, big_away = extract_stat(stat_payload, ["bigChance", "Big chances"])
    xg_home, xg_away = extract_stat(stat_payload, ["expectedGoals", "Expected goals"])
    return {
        "sofascore_event_id": int(event_id),
        "match_id": match_id,
        "possession_home": possession_home,
        "possession_away": possession_away,
        "shots_home": integer_value(shots_home),
        "shots_away": integer_value(shots_away),
        "shots_on_target_home": integer_value(sot_home),
        "shots_on_target_away": integer_value(sot_away),
        "corners_home": integer_value(corners_home),
        "corners_away": integer_value(corners_away),
        "big_chances_home": integer_value(big_home),
        "big_chances_away": integer_value(big_away),
        "xg_home": xg_home,
        "xg_away": xg_away,
    }


def incident_player_name(incident):
    if incident.get("playerName"):
        return incident.get("playerName")
    for key in ("player", "playerIn", "playerOut"):
        value = incident.get(key)
        if isinstance(value, dict) and value.get("name"):
            return value.get("name")
    return None


def iter_incidents(incidents_payload):
    incidents = incidents_payload.get("incidents", incidents_payload)
    if isinstance(incidents, list):
        return incidents
    return []


def parse_incident(incident, event_id, match_id):
    return {
        "sofascore_event_id": int(event_id),
        "match_id": match_id,
        "minute": incident.get("time"),
        "incident_type": incident.get("incidentType"),
        "is_home": incident.get("isHome"),
        "player_name": incident_player_name(incident),
        "home_score": incident.get("homeScore"),
        "away_score": incident.get("awayScore"),
    }


def filter_columns(row, columns):
    return {key: value for key, value in row.items() if key in columns}


def table_columns(conn, table_name):
    rows = conn.execute(text("""
        select column_name
        from information_schema.columns
        where table_schema = 'public' and table_name = :table_name
    """), {"table_name": table_name}).scalars().all()
    return set(rows)


def insert_row(conn, table_name, row, columns):
    values = filter_columns(row, columns)
    if not values:
        raise ImportErrorForMatch(f"Nenhuma coluna compativel para {table_name}")
    names = list(values.keys())
    sql = text(f"insert into {table_name} ({', '.join(names)}) values ({', '.join(':' + name for name in names)})")
    conn.execute(sql, values)


def update_row(conn, table_name, row, columns, where_column, where_value):
    values = filter_columns(row, columns)
    values = {key: value for key, value in values.items() if key != where_column}
    if not values:
        return
    values["where_value"] = where_value
    assignments = ", ".join(f"{key} = :{key}" for key in values if key != "where_value")
    conn.execute(text(f"update {table_name} set {assignments} where {where_column} = :where_value"), values)


def upsert_match(conn, row, columns):
    event_id = row["sofascore_event_id"]
    existing = conn.execute(
        text("select match_id from matches_master where sofascore_event_id = :event_id order by match_id limit 1"),
        {"event_id": event_id},
    ).scalar_one_or_none()
    if existing is not None:
        update_row(conn, "matches_master", row, columns, "sofascore_event_id", event_id)
        return existing, "updated"

    values = filter_columns(row, columns)
    names = list(values.keys())
    sql = text(
        f"insert into matches_master ({', '.join(names)}) values ({', '.join(':' + name for name in names)}) returning match_id"
    )
    match_id = conn.execute(sql, values).scalar_one()
    return match_id, "inserted"


def import_match(conn, match_info, columns):
    event_id = match_info["event_id"]
    match_dir = match_info["dir"]
    event_payload = load_json(match_dir / "event.json")
    stat_payload = load_json(match_dir / "statistics.json")
    incidents_payload = load_json(match_dir / "incidents.json")

    match_row = parse_event(event_payload, event_id)
    match_id, match_action = upsert_match(conn, match_row, columns["matches_master"])

    conn.execute(
        text("delete from match_statistics where sofascore_event_id = :event_id or match_id = :match_id"),
        {"event_id": int(event_id), "match_id": match_id},
    )
    insert_row(conn, "match_statistics", parse_statistics(stat_payload, event_id, match_id), columns["match_statistics"])

    conn.execute(
        text("delete from match_incidents where sofascore_event_id = :event_id or match_id = :match_id"),
        {"event_id": int(event_id), "match_id": match_id},
    )
    incident_count = 0
    for incident in iter_incidents(incidents_payload):
        insert_row(conn, "match_incidents", parse_incident(incident, event_id, match_id), columns["match_incidents"])
        incident_count += 1

    return {"match_action": match_action, "incidents": incident_count}


def print_classification_summary(matches):
    counts = {
        "full": sum(1 for row in matches if row["classification"] == "full" and row["status"] != "known_skipped"),
        "core": sum(1 for row in matches if row["classification"] == "core" and row["status"] != "known_skipped"),
        "incomplete": sum(1 for row in matches if row["status"] == "incomplete"),
        "known_skipped": sum(1 for row in matches if row["status"] == "known_skipped"),
        "importable": sum(1 for row in matches if row["status"] == "importable"),
        "missing": 0,
    }
    print("RESUMO CLASSIFICACAO")
    for key in ("full", "core", "importable", "known_skipped", "incomplete", "missing"):
        print(f"{key}: {counts[key]}")
    return counts


def main():
    args = parse_args()
    raw_root = resolve_raw_root(args.raw_root)
    matches = discover_matches(raw_root)
    print(f"Raw root: {raw_root}")
    counts = print_classification_summary(matches)

    if args.dry_run:
        print("DRY-RUN: nenhuma gravacao executada.")
        return

    importable = [row for row in matches if row["status"] == "importable"]
    if args.limit is not None:
        importable = importable[:args.limit]

    summary = {"processed": 0, "inserted": 0, "updated": 0, "failed": 0, "known_skipped": counts["known_skipped"]}

    with engine.begin() as conn:
        columns = {
            "matches_master": table_columns(conn, "matches_master"),
            "match_statistics": table_columns(conn, "match_statistics"),
            "match_incidents": table_columns(conn, "match_incidents"),
        }

    for row in importable:
        event_id = row["event_id"]
        try:
            with engine.begin() as conn:
                result = import_match(conn, row, columns)
            summary["processed"] += 1
            summary[result["match_action"]] += 1
            print(f"[OK] {event_id} | {row['classification']} | {result['match_action']} | incidents={result['incidents']}")
        except Exception as error:
            summary["failed"] += 1
            print(f"[ERRO] {event_id} | {row['classification']} | {error}")

    print("\nRESUMO IMPORTACAO")
    print(f"processed: {summary['processed']}")
    print(f"inserted: {summary['inserted']}")
    print(f"updated: {summary['updated']}")
    print(f"failed: {summary['failed']}")
    print(f"known_skipped: {summary['known_skipped']}")
    print(f"finished_at: {utc_now()}")


if __name__ == "__main__":
    main()
