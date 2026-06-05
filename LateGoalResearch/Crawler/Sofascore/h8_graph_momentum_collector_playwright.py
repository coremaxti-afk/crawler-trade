"""Playwright-based H8 graph/momentum collector with optional manual warmup.

This collector is intentionally isolated from v2/v3 and from the urllib H8 collector.
It keeps a 20-match cap, checkpoint, validation, logging, and 403 stop rules.
"""
from __future__ import annotations

import argparse
import json
import random
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

SCRIPT_PATH = Path(__file__).resolve()
SCRIPT_DIR = SCRIPT_PATH.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import h8_graph_momentum_collector as base  # noqa: E402

COLLECTION_LOG_FILE = base.LEAGUE_DIR / "collection_log_graph_playwright.jsonl"
MAX_LIMIT = 20
DEFAULT_LIMIT = 20
DEFAULT_LATE_GOAL_TARGET_COUNT = 10
DEFAULT_NO_LATE_GOAL_TARGET_COUNT = 10
REQUEST_TIMEOUT_MS = 60000
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


class HttpStatusError(Exception):
    def __init__(self, status_code: int):
        super().__init__(f"HTTP {status_code}")
        self.status_code = status_code


class OperationalBlock(Exception):
    """Raised when HTTP 403 requires immediate stop."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Playwright H8 graph/momentum collector with manual warmup support."
    )
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="Maximum matches to process. Hard-capped at 20.")
    parser.add_argument("--event-ids", nargs="*", default=None, help="Optional explicit SofaScore event ids. Max 20.")
    parser.add_argument("--list-pending", action="store_true", help="List selected matches without requests.")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without requests.")
    parser.add_argument("--execute", action="store_true", help="Actually perform browser requests.")
    parser.add_argument("--headed", action="store_true", help="Open a visible Chromium window for manual session warmup.")
    parser.add_argument("--manual-warmup", action="store_true", help="Pause after opening SofaScore so user can accept cookies or inspect session.")
    parser.add_argument("--warmup-url", default="https://www.sofascore.com/", help="URL opened before API requests.")
    parser.add_argument("--storage-state", default=None, help="Optional storage_state JSON file to load/save browser session.")
    parser.add_argument("--delay-min", type=float, default=base.DEFAULT_DELAY_MIN_SECONDS)
    parser.add_argument("--delay-max", type=float, default=base.DEFAULT_DELAY_MAX_SECONDS)
    parser.add_argument("--jitter", type=float, default=base.DEFAULT_JITTER_SECONDS)
    parser.add_argument("--backoff", type=float, default=base.DEFAULT_BACKOFF_SECONDS)
    parser.add_argument("--max-retries", type=int, default=base.DEFAULT_MAX_RETRIES)
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


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
    base_delay = random.uniform(args.delay_min, args.delay_max)
    jitter = random.uniform(0, max(0.0, args.jitter))
    time.sleep(base_delay + jitter)


def extract_json_from_page(page: Any) -> Any:
    body = page.locator("body").inner_text(timeout=REQUEST_TIMEOUT_MS)
    return json.loads(body)


def fetch_graph_with_playwright(page: Any, url: str) -> tuple[int, Any]:
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
    output_path = base.MATCHES_DIR / event_id / base.GRAPH_FILENAME
    output_path.parent.mkdir(parents=True, exist_ok=True)

    status = base.graph_file_status(event_id)
    if status["valid"]:
        write_log(event_id, url, None, "skip_existing_valid", status["graph_points_count"], None)
        return "skipped_valid_existing"
    if status["exists"] and not status["valid"]:
        backup_path = backup_invalid_graph(output_path)
        write_log(event_id, url, None, "backup_invalid_existing", 0, f"backup={backup_path}")

    last_error: Exception | None = None
    for attempt in range(args.max_retries + 1):
        try:
            status_code, payload = fetch_graph_with_playwright(page, url)
            valid, count, validation_error = base.validate_graph_payload(payload)
            if not valid:
                raise base.GraphPayloadError(validation_error or "invalid graph payload")
            with output_path.open("w", encoding="utf-8") as file:
                json.dump(payload, file, ensure_ascii=False, indent=2)
            write_log(event_id, url, status_code, "success", count, None)
            return "success"
        except HttpStatusError as error:
            if error.status_code == 403:
                write_log(event_id, url, error.status_code, "blocked_403", 0, str(error))
                raise OperationalBlock(f"HTTP 403 for event_id={event_id}") from error
            last_error = error
            if error.status_code not in RETRYABLE_STATUS_CODES or attempt >= args.max_retries:
                write_log(event_id, url, error.status_code, "failed", 0, str(error))
                return "failed"
        except (PlaywrightTimeoutError, PlaywrightError, json.JSONDecodeError, base.GraphPayloadError, OSError) as error:
            last_error = error
            if attempt >= args.max_retries:
                write_log(event_id, url, None, "failed", 0, str(error))
                return "failed"
        write_log(event_id, url, None, "retry", 0, str(last_error))
        time.sleep(args.backoff)
    return "failed"


def warmup_context(page: Any, context: Any, args: argparse.Namespace) -> None:
    print(f"Opening warmup URL: {args.warmup_url}")
    page.goto(args.warmup_url, wait_until="domcontentloaded", timeout=REQUEST_TIMEOUT_MS)
    if args.manual_warmup:
        print("Manual warmup enabled.")
        print("Use the visible browser to accept cookies or open the graph endpoint manually if needed.")
        input("Press ENTER here when the browser session is ready to continue...")
    if args.storage_state:
        context.storage_state(path=args.storage_state)
        print(f"Saved storage state: {args.storage_state}")


def select_rows_by_event_ids(event_ids: list[str]) -> list[dict[str, Any]]:
    rows = base.load_dataset_rows()
    by_event = {base.row_event_id(row): row for row in rows}
    selected = []
    for event_id in event_ids[:MAX_LIMIT]:
        row = by_event.get(str(event_id), {})
        selected.append(base.make_candidate(event_id=str(event_id), row=row, reason="explicit_event_id"))
    return selected


def auto_select_candidates(limit: int) -> list[dict[str, Any]]:
    rows = sorted(base.load_dataset_rows(), key=lambda row: (row.get("match_date", ""), row.get("match_id", "")))
    selected: list[dict[str, Any]] = []
    desired = {
        1: min(DEFAULT_LATE_GOAL_TARGET_COUNT, (limit + 1) // 2),
        0: min(DEFAULT_NO_LATE_GOAL_TARGET_COUNT, limit // 2),
    }
    target_counts = {1: 0, 0: 0}

    for target_value in (1, 0):
        for row in rows:
            event_id = base.row_event_id(row)
            if not event_id or event_id in base.KNOWN_SKIPPED_EVENT_IDS:
                continue
            try:
                row_target = int(float(row.get("target_late_goal_75", "")))
            except ValueError:
                continue
            if row_target != target_value:
                continue
            if not base.has_core_files(event_id):
                continue
            if any(item["event_id"] == event_id for item in selected):
                continue
            selected.append(base.make_candidate(event_id=event_id, row=row, reason="auto_selected_core_complete_playwright_20"))
            target_counts[target_value] += 1
            if target_counts[target_value] >= desired[target_value]:
                break

    if len(selected) < limit:
        for row in rows:
            event_id = base.row_event_id(row)
            if not event_id or event_id in base.KNOWN_SKIPPED_EVENT_IDS:
                continue
            if not base.has_core_files(event_id):
                continue
            if any(item["event_id"] == event_id for item in selected):
                continue
            selected.append(base.make_candidate(event_id=event_id, row=row, reason="auto_selected_core_complete_fill"))
            if len(selected) >= limit:
                break
    return selected[:limit]


def selected_candidates(args: argparse.Namespace) -> list[dict[str, Any]]:
    limit = min(args.limit or DEFAULT_LIMIT, MAX_LIMIT)
    if args.event_ids:
        return select_rows_by_event_ids(args.event_ids)[:limit]
    return auto_select_candidates(limit)


def execute_collection(candidates: list[dict[str, Any]], args: argparse.Namespace) -> None:
    processed = 0
    successes = 0
    failures = 0
    skipped = 0
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
                if processed >= MAX_LIMIT:
                    break
                processed += 1
                print(f"[{index}/{len(candidates)}] collecting graph for {candidate['event_id']}")
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
                    sleep_between_requests(args)
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
    candidates = selected_candidates(args)
    if len(candidates) > MAX_LIMIT:
        raise SystemExit("Refusing to process more than 20 matches.")
    base.print_candidates(candidates)
    if args.list_pending or args.dry_run or not args.execute:
        print("\nSAFE MODE: no HTTP requests were made. Pass --execute in an authorized local browser session to collect.")
        return
    execute_collection(candidates, args)


if __name__ == "__main__":
    main()
