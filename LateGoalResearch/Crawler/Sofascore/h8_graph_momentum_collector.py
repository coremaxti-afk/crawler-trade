"""Controlled SofaScore graph/momentum spike collector for H8.

Default behavior is safe: no HTTP request is made unless --execute is passed.
Use --list-pending or --dry-run to inspect the 5-match spike plan.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SCRIPT_PATH = Path(__file__).resolve()
SCRIPT_DIR = SCRIPT_PATH.parent
LATE_GOAL_ROOT = SCRIPT_PATH.parents[2]

LEAGUE_DIR = SCRIPT_DIR / "data" / "raw" / "sofascore" / "premier_league_61627"
MATCHES_DIR = LEAGUE_DIR / "matches"
COLLECTION_LOG_FILE = LEAGUE_DIR / "collection_log_graph.jsonl"
DATASET_V1_PATH = LATE_GOAL_ROOT / "data" / "processed" / "datasets" / "late_goal_dataset_v1.csv"

ENDPOINT_TEMPLATE = "https://www.sofascore.com/api/v1/event/{event_id}/graph"
GRAPH_FILENAME = "graph.json"
CORE_FILES = ("event.json", "statistics.json", "incidents.json")
KNOWN_SKIPPED_EVENT_IDS = {"12436452"}
DEFAULT_LIMIT = 5
DEFAULT_LATE_GOAL_TARGET_COUNT = 3
DEFAULT_NO_LATE_GOAL_TARGET_COUNT = 2
DEFAULT_DELAY_MIN_SECONDS = 10.0
DEFAULT_DELAY_MAX_SECONDS = 15.0
DEFAULT_JITTER_SECONDS = 10.0
DEFAULT_BACKOFF_SECONDS = 120.0
DEFAULT_MAX_RETRIES = 1
REQUEST_TIMEOUT_SECONDS = 45
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


class OperationalBlock(Exception):
    """Raised when HTTP 403 requires immediate stop."""


class GraphPayloadError(Exception):
    """Raised when graph payload does not match the expected contract."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Controlled H8 graph/momentum collector for 5 existing EPL matches."
    )
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="Maximum matches to process. Hard-capped at 5.")
    parser.add_argument("--event-ids", nargs="*", default=None, help="Optional explicit SofaScore event ids. Max 5.")
    parser.add_argument("--list-pending", action="store_true", help="List selected matches and graph.json status without requests.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be collected without requests.")
    parser.add_argument("--execute", action="store_true", help="Actually perform HTTP requests. Not used by Codex environment.")
    parser.add_argument("--delay-min", type=float, default=DEFAULT_DELAY_MIN_SECONDS, help="Minimum delay between requests.")
    parser.add_argument("--delay-max", type=float, default=DEFAULT_DELAY_MAX_SECONDS, help="Maximum delay between requests.")
    parser.add_argument("--jitter", type=float, default=DEFAULT_JITTER_SECONDS, help="Additional random jitter in seconds.")
    parser.add_argument("--backoff", type=float, default=DEFAULT_BACKOFF_SECONDS, help="Backoff before the single retry.")
    parser.add_argument("--max-retries", type=int, default=DEFAULT_MAX_RETRIES, help="Retry count for retryable failures.")
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json_file(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate_graph_payload(payload: Any) -> tuple[bool, int, str | None]:
    if not isinstance(payload, dict):
        return False, 0, "root is not an object"
    if "graphPoints" not in payload:
        return False, 0, "missing graphPoints"
    points = payload["graphPoints"]
    if not isinstance(points, list):
        return False, 0, "graphPoints is not a list"
    for index, item in enumerate(points):
        if not isinstance(item, dict):
            return False, len(points), f"graphPoints[{index}] is not an object"
        if "minute" not in item or "value" not in item:
            return False, len(points), f"graphPoints[{index}] missing minute or value"
        if not is_number(item["minute"]):
            return False, len(points), f"graphPoints[{index}].minute is not numeric"
        if not is_number(item["value"]):
            return False, len(points), f"graphPoints[{index}].value is not numeric"
    return True, len(points), None


def graph_file_status(event_id: str) -> dict[str, Any]:
    path = MATCHES_DIR / event_id / GRAPH_FILENAME
    if not path.exists():
        return {"exists": False, "valid": False, "graph_points_count": 0, "error": "missing"}
    try:
        payload = read_json_file(path)
    except (json.JSONDecodeError, OSError) as error:
        return {"exists": True, "valid": False, "graph_points_count": 0, "error": str(error)}
    valid, count, error = validate_graph_payload(payload)
    return {"exists": True, "valid": valid, "graph_points_count": count, "error": error}


def has_core_files(event_id: str) -> bool:
    match_dir = MATCHES_DIR / event_id
    return all((match_dir / name).exists() for name in CORE_FILES)


def load_dataset_rows() -> list[dict[str, str]]:
    if not DATASET_V1_PATH.exists():
        raise FileNotFoundError(f"Dataset V1 not found: {DATASET_V1_PATH}")
    with DATASET_V1_PATH.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def row_event_id(row: dict[str, str]) -> str:
    value = row.get("sofascore_event_id") or row.get("event_id") or ""
    return value.split(".")[0].strip()


def select_rows_by_event_ids(event_ids: list[str]) -> list[dict[str, Any]]:
    rows = load_dataset_rows()
    by_event = {row_event_id(row): row for row in rows}
    selected = []
    for event_id in event_ids[:DEFAULT_LIMIT]:
        row = by_event.get(str(event_id), {})
        selected.append(make_candidate(event_id=str(event_id), row=row, reason="explicit_event_id"))
    return selected


def make_candidate(event_id: str, row: dict[str, str], reason: str) -> dict[str, Any]:
    target = row.get("target_late_goal_75")
    status = graph_file_status(event_id)
    return {
        "event_id": event_id,
        "match_id": row.get("match_id"),
        "match_date": row.get("match_date"),
        "home_team": row.get("home_team"),
        "away_team": row.get("away_team"),
        "target_late_goal_75": None if target in (None, "") else int(float(target)),
        "has_core_files": has_core_files(event_id),
        "graph_exists": status["exists"],
        "graph_valid": status["valid"],
        "graph_points_count": status["graph_points_count"],
        "graph_error": status["error"],
        "url": ENDPOINT_TEMPLATE.format(event_id=event_id),
        "reason": reason,
    }


def auto_select_candidates(limit: int) -> list[dict[str, Any]]:
    rows = sorted(load_dataset_rows(), key=lambda row: (row.get("match_date", ""), row.get("match_id", "")))
    selected: list[dict[str, Any]] = []
    target_counts = {1: 0, 0: 0}
    desired = {1: DEFAULT_LATE_GOAL_TARGET_COUNT, 0: DEFAULT_NO_LATE_GOAL_TARGET_COUNT}

    for target_value in (1, 0):
        for row in rows:
            event_id = row_event_id(row)
            if not event_id or event_id in KNOWN_SKIPPED_EVENT_IDS:
                continue
            try:
                row_target = int(float(row.get("target_late_goal_75", "")))
            except ValueError:
                continue
            if row_target != target_value:
                continue
            if not has_core_files(event_id):
                continue
            if any(item["event_id"] == event_id for item in selected):
                continue
            selected.append(make_candidate(event_id=event_id, row=row, reason="auto_selected_core_complete"))
            target_counts[target_value] += 1
            if target_counts[target_value] >= desired[target_value]:
                break

    return selected[:limit]


def selected_candidates(args: argparse.Namespace) -> list[dict[str, Any]]:
    limit = min(args.limit or DEFAULT_LIMIT, DEFAULT_LIMIT)
    if args.event_ids:
        return select_rows_by_event_ids(args.event_ids)[:limit]
    return auto_select_candidates(limit)


def print_candidates(candidates: list[dict[str, Any]]) -> None:
    print("H8 graph/momentum spike plan")
    print(f"Matches selected: {len(candidates)}")
    for index, item in enumerate(candidates, start=1):
        status = "valid_existing" if item["graph_valid"] else "pending"
        if item["graph_exists"] and not item["graph_valid"]:
            status = "invalid_existing_will_backup_on_execute"
        print(
            f"[{index}] {item['event_id']} | {item.get('match_date') or 'unknown_date'} | "
            f"{item.get('home_team') or 'unknown_home'} x {item.get('away_team') or 'unknown_away'} | "
            f"late_goal={item['target_late_goal_75']} | core={item['has_core_files']} | graph={status} | "
            f"points={item['graph_points_count']}"
        )
        print(f"    {item['url']}")


def write_log(event_id: str, url: str, status_code: int | None, result: str, graph_points_count: int = 0, error: str | None = None) -> None:
    COLLECTION_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": utc_now(),
        "event_id": event_id,
        "url": url,
        "status_code": status_code,
        "result": result,
        "graph_points_count": graph_points_count,
        "error": error,
    }
    with COLLECTION_LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False))
        file.write("\n")


def backup_invalid_graph(path: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_dir = path.parent / "_invalid_graph_backup"
    backup_dir.mkdir(parents=True, exist_ok=True)
    target = backup_dir / f"{path.name}.{timestamp}.invalid"
    counter = 1
    while target.exists():
        target = backup_dir / f"{path.name}.{timestamp}.{counter}.invalid"
        counter += 1
    shutil.move(str(path), str(target))
    return target


def sleep_between_requests(args: argparse.Namespace) -> None:
    base = random.uniform(args.delay_min, args.delay_max)
    jitter = random.uniform(0, max(0.0, args.jitter))
    time.sleep(base + jitter)


def fetch_graph(event_id: str, url: str) -> tuple[int, Any]:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            status_code = int(response.status)
            body = response.read().decode("utf-8")
            return status_code, json.loads(body)
    except HTTPError as error:
        raise error
    except URLError as error:
        raise error


def collect_one(candidate: dict[str, Any], args: argparse.Namespace) -> str:
    event_id = candidate["event_id"]
    url = candidate["url"]
    output_path = MATCHES_DIR / event_id / GRAPH_FILENAME
    output_path.parent.mkdir(parents=True, exist_ok=True)

    status = graph_file_status(event_id)
    if status["valid"]:
        write_log(event_id, url, None, "skip_existing_valid", status["graph_points_count"], None)
        return "skipped_valid_existing"
    if status["exists"] and not status["valid"]:
        backup_path = backup_invalid_graph(output_path)
        write_log(event_id, url, None, "backup_invalid_existing", 0, f"backup={backup_path}")

    last_error = None
    for attempt in range(args.max_retries + 1):
        try:
            status_code, payload = fetch_graph(event_id, url)
            valid, count, validation_error = validate_graph_payload(payload)
            if not valid:
                raise GraphPayloadError(validation_error or "invalid graph payload")
            with output_path.open("w", encoding="utf-8") as file:
                json.dump(payload, file, ensure_ascii=False, indent=2)
            write_log(event_id, url, status_code, "success", count, None)
            return "success"
        except HTTPError as error:
            status_code = int(error.code)
            if status_code == 403:
                write_log(event_id, url, status_code, "blocked_403", 0, str(error))
                raise OperationalBlock(f"HTTP 403 for event_id={event_id}") from error
            last_error = error
            if status_code not in RETRYABLE_STATUS_CODES or attempt >= args.max_retries:
                write_log(event_id, url, status_code, "failed", 0, str(error))
                return "failed"
        except (URLError, json.JSONDecodeError, GraphPayloadError, OSError) as error:
            last_error = error
            if attempt >= args.max_retries:
                write_log(event_id, url, None, "failed", 0, str(error))
                return "failed"
        write_log(event_id, url, None, "retry", 0, str(last_error))
        time.sleep(args.backoff)
    return "failed"


def execute_collection(candidates: list[dict[str, Any]], args: argparse.Namespace) -> None:
    processed = 0
    successes = 0
    failures = 0
    skipped = 0
    blocked = False
    for index, candidate in enumerate(candidates, start=1):
        if processed >= DEFAULT_LIMIT:
            break
        processed += 1
        print(f"[{index}/{len(candidates)}] collecting graph for {candidate['event_id']}")
        try:
            result = collect_one(candidate, args)
        except OperationalBlock as error:
            blocked = True
            print(f"BLOCKED: {error}")
            break
        if result == "success":
            successes += 1
        elif result.startswith("skipped"):
            skipped += 1
        else:
            failures += 1
        if index < len(candidates):
            sleep_between_requests(args)
    print("\nFINAL SUMMARY")
    print(f"processed={processed}")
    print(f"successes={successes}")
    print(f"skipped={skipped}")
    print(f"failures={failures}")
    print(f"blocked_403={blocked}")
    print(f"log={COLLECTION_LOG_FILE}")
    if blocked:
        raise SystemExit(1)


def main() -> None:
    args = parse_args()
    candidates = selected_candidates(args)
    if len(candidates) > DEFAULT_LIMIT:
        raise SystemExit("Refusing to process more than 5 matches.")
    print_candidates(candidates)
    if args.list_pending or args.dry_run or not args.execute:
        print("\nSAFE MODE: no HTTP requests were made. Pass --execute manually in the authorized local 5G environment to collect.")
        return
    execute_collection(candidates, args)


if __name__ == "__main__":
    main()
