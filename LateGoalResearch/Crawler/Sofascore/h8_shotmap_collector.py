"""Controlled SofaScore shotmap collector for H8.

Collects raw `shotmap.json` for already existing EPL match folders using a
single sequential Playwright session. It does not alter database, schema,
importers, datasets, features, models, or existing SofaScore collectors.
"""
from __future__ import annotations

import argparse
import json
import random
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

SCRIPT_DIR = Path(__file__).resolve().parent
LEAGUE_DIR = SCRIPT_DIR / "data" / "raw" / "sofascore" / "premier_league_61627"
INVENTORY_FILE = LEAGUE_DIR / "inventory.json"
MATCHES_DIR = LEAGUE_DIR / "matches"
COLLECTION_LOG_FILE = LEAGUE_DIR / "collection_log_shotmap.jsonl"
ENDPOINT_TEMPLATE = "https://www.sofascore.com/api/v1/event/{event_id}/shotmap"
SHOTMAP_FILENAME = "shotmap.json"
KNOWN_SKIPPED_EVENT_IDS = {"12436452"}
DEFAULT_LIMIT = 25
DEFAULT_REQUEST_DELAY_SECONDS = 10.0
DEFAULT_MATCH_DELAY_SECONDS = 20.0
DEFAULT_JITTER_SECONDS = 10.0
DEFAULT_BACKOFF_SECONDS = 120.0
DEFAULT_MAX_RETRIES = 1
REQUEST_TIMEOUT_MS = 60000
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


class HttpStatusError(Exception):
    def __init__(self, status_code: int):
        super().__init__(f"HTTP {status_code}")
        self.status_code = status_code


class OperationalBlock(Exception):
    """Raised when HTTP 403 requires immediate stop."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Controlled H8 shotmap collector for existing EPL matches.")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="Maximum matches to process in this run.")
    parser.add_argument("--start-index", type=int, default=1, help="1-based index in the inventory candidate list to start from.")
    parser.add_argument("--dry-run", action="store_true", help="List pending matches without HTTP requests.")
    parser.add_argument("--request-delay", type=float, default=DEFAULT_REQUEST_DELAY_SECONDS, help="Base delay before each request in seconds.")
    parser.add_argument("--match-delay", type=float, default=DEFAULT_MATCH_DELAY_SECONDS, help="Base delay after each match in seconds.")
    parser.add_argument("--jitter", type=float, default=DEFAULT_JITTER_SECONDS, help="Random jitter added to delays in seconds.")
    parser.add_argument("--backoff", type=float, default=DEFAULT_BACKOFF_SECONDS, help="Backoff in seconds for retryable failures.")
    parser.add_argument("--max-retries", type=int, default=DEFAULT_MAX_RETRIES, help="Retries for 429/5xx/timeouts.")
    parser.add_argument("--headed", action="store_true", help="Open a visible Chromium window for manual session warmup/debugging.")
    parser.add_argument("--manual-warmup", action="store_true", help="Pause after opening SofaScore before requests.")
    parser.add_argument("--warmup-url", default="https://www.sofascore.com/", help="Warmup URL opened before requests.")
    parser.add_argument("--storage-state", default=None, help="Optional storage_state JSON file to load/save browser session.")
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_inventory() -> list[dict[str, Any]]:
    payload = read_json(INVENTORY_FILE)
    if not isinstance(payload, list):
        raise RuntimeError(f"Inventory is not a list: {INVENTORY_FILE}")
    return payload


def row_event_id(row: dict[str, Any]) -> str:
    value = row.get("event_id") or row.get("id") or row.get("sofascore_event_id")
    return str(value).split(".")[0].strip() if value is not None else ""


def is_valid_json_file(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        payload = read_json(path)
    except (json.JSONDecodeError, OSError):
        return False
    return isinstance(payload, (dict, list))


def shotmap_items(payload: Any) -> list[Any]:
    if isinstance(payload, dict):
        value = payload.get("shotmap")
        return value if isinstance(value, list) else []
    if isinstance(payload, list):
        return payload
    return []


def payload_metadata(payload: Any) -> dict[str, Any]:
    items = shotmap_items(payload)
    metadata: dict[str, Any] = {
        "root_type": "dict" if isinstance(payload, dict) else "list" if isinstance(payload, list) else type(payload).__name__,
        "top_level_keys": sorted(payload.keys()) if isinstance(payload, dict) else [],
        "shots_count": len(items),
        "field_presence": {},
    }
    fields = (
        "minute",
        "time",
        "addedTime",
        "timeSeconds",
        "xg",
        "xgot",
        "player",
        "team",
        "shotType",
        "goalMouthLocation",
        "playerCoordinates",
        "goalMouthCoordinates",
        "draw",
    )
    if items:
        metadata["field_presence"] = {field: any(isinstance(item, dict) and field in item for item in items) for field in fields}
    return metadata


def shotmap_file_status(event_id: str) -> dict[str, Any]:
    path = MATCHES_DIR / event_id / SHOTMAP_FILENAME
    if not path.exists():
        return {"exists": False, "valid": False, "shots_count": 0, "error": "missing", "metadata": {}}
    try:
        payload = read_json(path)
    except (json.JSONDecodeError, OSError) as error:
        return {"exists": True, "valid": False, "shots_count": 0, "error": str(error), "metadata": {}}
    if not isinstance(payload, (dict, list)):
        return {"exists": True, "valid": False, "shots_count": 0, "error": "root is not dict/list", "metadata": {}}
    metadata = payload_metadata(payload)
    return {"exists": True, "valid": True, "shots_count": metadata["shots_count"], "error": None, "metadata": metadata}


def make_candidate(row: dict[str, Any]) -> dict[str, Any] | None:
    event_id = row_event_id(row)
    if not event_id or event_id in KNOWN_SKIPPED_EVENT_IDS:
        return None
    match_dir = MATCHES_DIR / event_id
    if not match_dir.exists():
        return None
    status = shotmap_file_status(event_id)
    return {
        "event_id": event_id,
        "round": row.get("round"),
        "home_team": row.get("home_team"),
        "away_team": row.get("away_team"),
        "url": ENDPOINT_TEMPLATE.format(event_id=event_id),
        "shotmap_exists": status["exists"],
        "shotmap_valid": status["valid"],
        "shots_count": status["shots_count"],
        "shotmap_error": status["error"],
    }


def selected_candidates(limit: int, start_index: int) -> list[dict[str, Any]]:
    if limit < 1:
        raise SystemExit("--limit must be >= 1")
    if start_index < 1:
        raise SystemExit("--start-index must be >= 1")
    candidates: list[dict[str, Any]] = []
    for row in load_inventory():
        candidate = make_candidate(row)
        if candidate is None:
            continue
        candidates.append(candidate)
    return candidates[start_index - 1:start_index - 1 + limit]


def print_candidates(candidates: list[dict[str, Any]]) -> None:
    print("H8 shotmap collection plan")
    print(f"Matches selected: {len(candidates)}")
    for index, item in enumerate(candidates, start=1):
        status = "pending"
        if item["shotmap_exists"] and not item["shotmap_valid"]:
            status = "invalid_existing_will_backup"
        print(
            f"[{index}] {item['event_id']} | round={item.get('round')} | "
            f"{item.get('home_team') or 'unknown_home'} x {item.get('away_team') or 'unknown_away'} | "
            f"shotmap={status} | shots={item['shots_count']}"
        )
        print(f"    {item['url']}")


def write_log(event_id: str, url: str, attempt: int | None, status_code: int | None, result: str, shots_count: int = 0, error: str | None = None, metadata: dict[str, Any] | None = None) -> None:
    COLLECTION_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": utc_now(),
        "event_id": event_id,
        "filename": SHOTMAP_FILENAME,
        "url": url,
        "attempt": attempt,
        "status_code": status_code,
        "result": result,
        "shots_count": shots_count,
        "error": error,
    }
    if metadata is not None:
        record["metadata"] = metadata
    with COLLECTION_LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False))
        file.write("\n")


def backup_invalid_shotmap(path: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_dir = path.parent / "_invalid_json_backup"
    backup_dir.mkdir(parents=True, exist_ok=True)
    target = backup_dir / f"{path.name}.{timestamp}.invalid"
    counter = 1
    while target.exists():
        target = backup_dir / f"{path.name}.{timestamp}.{counter}.invalid"
        counter += 1
    shutil.move(str(path), str(target))
    return target


def sleep_with_jitter(base_seconds: float, jitter_seconds: float) -> None:
    time.sleep(base_seconds + random.uniform(0, max(0.0, jitter_seconds)))


def extract_json_from_page(page: Any) -> Any:
    body = page.locator("body").inner_text(timeout=REQUEST_TIMEOUT_MS)
    return json.loads(body)


def fetch_shotmap(page: Any, url: str) -> tuple[int, Any]:
    response = page.goto(url, wait_until="networkidle", timeout=REQUEST_TIMEOUT_MS)
    if response is None:
        raise PlaywrightError("No response returned by page.goto")
    status_code = int(response.status)
    if status_code != 200:
        raise HttpStatusError(status_code)
    return status_code, extract_json_from_page(page)


def collect_one(page: Any, candidate: dict[str, Any], args: argparse.Namespace) -> str:
    event_id = candidate["event_id"]
    url = candidate["url"]
    output_path = MATCHES_DIR / event_id / SHOTMAP_FILENAME
    output_path.parent.mkdir(parents=True, exist_ok=True)

    status = shotmap_file_status(event_id)
    if status["valid"]:
        write_log(event_id, url, None, None, "skip_existing_valid", status["shots_count"], None, status["metadata"])
        return "skipped_valid_existing"
    if status["exists"] and not status["valid"]:
        backup_path = backup_invalid_shotmap(output_path)
        write_log(event_id, url, None, None, "backup_invalid_existing", 0, f"backup={backup_path}")

    for attempt in range(1, args.max_retries + 2):
        try:
            sleep_with_jitter(args.request_delay, args.jitter)
            status_code, payload = fetch_shotmap(page, url)
            if not isinstance(payload, (dict, list)):
                raise ValueError("shotmap payload root is not dict/list")
            metadata = payload_metadata(payload)
            with output_path.open("w", encoding="utf-8") as file:
                json.dump(payload, file, ensure_ascii=False, indent=2)
            write_log(event_id, url, attempt, status_code, "success", metadata["shots_count"], None, metadata)
            return "success"
        except HttpStatusError as error:
            if error.status_code == 403:
                write_log(event_id, url, attempt, error.status_code, "blocked_403", 0, str(error))
                raise OperationalBlock(f"HTTP 403 for event_id={event_id}") from error
            if error.status_code not in RETRYABLE_STATUS_CODES or attempt > args.max_retries:
                write_log(event_id, url, attempt, error.status_code, "failed", 0, str(error))
                return "failed"
            write_log(event_id, url, attempt, error.status_code, "retry", 0, str(error))
            time.sleep(args.backoff)
        except (PlaywrightTimeoutError, PlaywrightError, json.JSONDecodeError, OSError, ValueError) as error:
            if attempt > args.max_retries:
                write_log(event_id, url, attempt, None, "failed", 0, str(error))
                return "failed"
            write_log(event_id, url, attempt, None, "retry", 0, str(error))
            time.sleep(args.backoff)
    return "failed"


def warmup_context(page: Any, context: Any, args: argparse.Namespace) -> None:
    print(f"Opening warmup URL: {args.warmup_url}")
    page.goto(args.warmup_url, wait_until="domcontentloaded", timeout=REQUEST_TIMEOUT_MS)
    if args.manual_warmup:
        print("Manual warmup enabled.")
        input("Press ENTER here when the browser session is ready to continue...")
    if args.storage_state:
        context.storage_state(path=args.storage_state)
        print(f"Saved storage state: {args.storage_state}")


def execute_collection(candidates: list[dict[str, Any]], args: argparse.Namespace) -> None:
    processed = 0
    successes = 0
    skipped = 0
    failures = 0
    blocked = False

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=not args.headed)
        context_kwargs: dict[str, Any] = {}
        if args.storage_state and Path(args.storage_state).exists():
            context_kwargs["storage_state"] = args.storage_state
        context = browser.new_context(**context_kwargs)
        page = context.new_page()
        try:
            warmup_context(page, context, args)
            for index, candidate in enumerate(candidates, start=1):
                processed += 1
                print(f"[{index}/{len(candidates)}] collecting shotmap for {candidate['event_id']}")
                try:
                    result = collect_one(page, candidate, args)
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
                    sleep_with_jitter(args.match_delay, args.jitter)
        finally:
            context.close()
            browser.close()

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
    candidates = selected_candidates(args.limit, args.start_index)
    print_candidates(candidates)
    if args.dry_run:
        print("\nSAFE MODE: no HTTP requests were made.")
        return
    execute_collection(candidates, args)


if __name__ == "__main__":
    main()
