import argparse
import json
import random
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


# ==========================================
# CONFIG
# ==========================================

LEAGUE_DIR = Path(
    "data/raw/sofascore/premier_league_61627"
)

INVENTORY_FILE = LEAGUE_DIR / "inventory.json"

MATCHES_DIR = LEAGUE_DIR / "matches"

COLLECTION_LOG_FILE = LEAGUE_DIR / "collection_log_v3.jsonl"

MAX_MATCHES = None

DEFAULT_START_INDEX = 138

DEFAULT_ENDPOINT_DELAY_SECONDS = 3.0

DEFAULT_MATCH_DELAY_SECONDS = 8.0

DEFAULT_JITTER_SECONDS = 2.0

DEFAULT_MAX_RETRIES = 3

DEFAULT_BACKOFF_SECONDS = 5.0

REQUEST_TIMEOUT_MS = 60000

EXPECTED_ENDPOINTS = [
    (
        "event.json",
        "https://www.sofascore.com/api/v1/event/{event_id}",
    ),
    (
        "statistics.json",
        "https://www.sofascore.com/api/v1/event/{event_id}/statistics",
    ),
    (
        "incidents.json",
        "https://www.sofascore.com/api/v1/event/{event_id}/incidents",
    ),
]

RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


class OperationalBlock(Exception):
    pass


class HttpStatusError(Exception):
    def __init__(self, status_code):
        super().__init__(f"HTTP {status_code}")
        self.status_code = status_code


# ==========================================
# CLI
# ==========================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Coleta essencial e retomavel de partidas SofaScore (3 endpoints core)."
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=MAX_MATCHES,
        help="Limita a quantidade de partidas processadas neste lote.",
    )

    parser.add_argument(
        "--start-index",
        type=int,
        default=DEFAULT_START_INDEX,
        help="Indice 1-based da primeira partida do inventory a processar.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Lista endpoints pendentes sem fazer requests.",
    )

    parser.add_argument(
        "--list-pending",
        action="store_true",
        help="Alias de --dry-run.",
    )

    parser.add_argument(
        "--endpoint-delay",
        type=float,
        default=DEFAULT_ENDPOINT_DELAY_SECONDS,
        help="Delay base entre endpoints, em segundos.",
    )

    parser.add_argument(
        "--match-delay",
        type=float,
        default=DEFAULT_MATCH_DELAY_SECONDS,
        help="Delay base entre partidas, em segundos.",
    )

    parser.add_argument(
        "--jitter",
        type=float,
        default=DEFAULT_JITTER_SECONDS,
        help="Jitter aleatorio maximo somado aos delays, em segundos.",
    )

    parser.add_argument(
        "--max-retries",
        type=int,
        default=DEFAULT_MAX_RETRIES,
        help="Tentativas para 429, 5xx, timeout e falhas temporarias.",
    )

    parser.add_argument(
        "--backoff",
        type=float,
        default=DEFAULT_BACKOFF_SECONDS,
        help="Backoff exponencial base, em segundos.",
    )

    return parser.parse_args()


# ==========================================
# LOAD INVENTORY
# ==========================================

def load_inventory():

    with open(
        INVENTORY_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ==========================================
# LOGGING
# ==========================================

def utc_now():
    return datetime.now(timezone.utc).isoformat()


def write_log(
    event_id,
    filename,
    url,
    attempt,
    result,
    status_code=None,
    error=None,
):
    COLLECTION_LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    record = {
        "timestamp": utc_now(),
        "event_id": event_id,
        "filename": filename,
        "url": url,
        "attempt": attempt,
        "status_code": status_code,
        "result": result,
    }

    if error:
        record["error"] = str(error)

    with open(
        COLLECTION_LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:
        f.write(
            json.dumps(
                record,
                ensure_ascii=False,
            )
        )
        f.write("\n")


# ==========================================
# JSON FILES
# ==========================================

def is_valid_json(filepath):
    try:
        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as f:
            json.load(f)
        return True
    except (json.JSONDecodeError, OSError):
        return False


def quarantine_invalid_json(filepath):
    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ"
    )
    quarantine_dir = filepath.parent / "_invalid_json_backup"
    quarantine_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    target = quarantine_dir / f"{filepath.name}.{timestamp}.invalid"
    counter = 1

    while target.exists():
        target = quarantine_dir / f"{filepath.name}.{timestamp}.{counter}.invalid"
        counter += 1

    shutil.move(
        str(filepath),
        str(target),
    )

    return target


# ==========================================
# GET JSON
# ==========================================

def get_json(page, url):

    response = page.goto(
        url,
        wait_until="networkidle",
        timeout=REQUEST_TIMEOUT_MS
    )

    if response is None:
        raise PlaywrightError("Sem resposta")

    if response.status != 200:
        raise HttpStatusError(response.status)

    body = page.locator("body").inner_text()

    return json.loads(body)


def is_retryable_error(error):
    if isinstance(error, HttpStatusError):
        return error.status_code in RETRYABLE_STATUS_CODES

    return isinstance(
        error,
        (
            PlaywrightTimeoutError,
            PlaywrightError,
            json.JSONDecodeError,
        )
    )


def sleep_with_jitter(base_seconds, jitter_seconds):
    delay = max(0, base_seconds)

    if jitter_seconds > 0:
        delay += random.uniform(
            0,
            jitter_seconds,
        )

    if delay > 0:
        time.sleep(delay)


def fetch_json_with_retry(
    page,
    event_id,
    filename,
    url,
    max_retries,
    backoff_seconds,
    jitter_seconds,
):
    for attempt in range(1, max_retries + 2):
        try:
            data = get_json(
                page,
                url,
            )

            write_log(
                event_id=event_id,
                filename=filename,
                url=url,
                attempt=attempt,
                result="success",
                status_code=200,
            )

            return data

        except HttpStatusError as error:
            if error.status_code == 403:
                write_log(
                    event_id=event_id,
                    filename=filename,
                    url=url,
                    attempt=attempt,
                    result="blocked",
                    status_code=error.status_code,
                    error=error,
                )
                raise OperationalBlock(
                    f"HTTP 403 em {event_id} | {filename}"
                ) from error

            if not is_retryable_error(error) or attempt > max_retries:
                write_log(
                    event_id=event_id,
                    filename=filename,
                    url=url,
                    attempt=attempt,
                    result="failed",
                    status_code=error.status_code,
                    error=error,
                )
                raise

            write_log(
                event_id=event_id,
                filename=filename,
                url=url,
                attempt=attempt,
                result="retry",
                status_code=error.status_code,
                error=error,
            )

        except (
            PlaywrightTimeoutError,
            PlaywrightError,
            json.JSONDecodeError,
        ) as error:
            if not is_retryable_error(error) or attempt > max_retries:
                write_log(
                    event_id=event_id,
                    filename=filename,
                    url=url,
                    attempt=attempt,
                    result="failed",
                    error=error,
                )
                raise

            write_log(
                event_id=event_id,
                filename=filename,
                url=url,
                attempt=attempt,
                result="retry",
                error=error,
            )

        backoff_delay = backoff_seconds * (2 ** (attempt - 1))
        sleep_with_jitter(
            backoff_delay,
            jitter_seconds,
        )

    raise RuntimeError(
        f"Falha inesperada em {event_id} | {filename}"
    )


# ==========================================
# SAVE JSON
# ==========================================

def save_json(data, filepath):

    filepath.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


# ==========================================
# ENDPOINT CHECKPOINT
# ==========================================

def endpoint_items(event_id):
    for filename, url_template in EXPECTED_ENDPOINTS:
        yield filename, url_template.format(
            event_id=event_id,
        )


def get_pending_endpoints(event_id, dry_run=False):
    match_dir = MATCHES_DIR / str(event_id)
    pending = []

    for filename, url in endpoint_items(event_id):
        filepath = match_dir / filename

        if filepath.exists() and is_valid_json(filepath):
            if not dry_run:
                write_log(
                    event_id=event_id,
                    filename=filename,
                    url=url,
                    attempt=0,
                    result="skip_existing",
                    status_code=None,
                )
            continue

        pending.append(
            (
                filename,
                url,
                filepath,
                filepath.exists(),
            )
        )

    return pending


# ==========================================
# COLLECT MATCH
# ==========================================

def collect_match(page, event_id, args):

    match_dir = MATCHES_DIR / str(event_id)
    match_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    pending = get_pending_endpoints(
        event_id,
    )

    if not pending:
        print(
            f"[SKIP] {event_id} | partida completa"
        )
        return {
            "success": 0,
            "skipped": len(EXPECTED_ENDPOINTS),
            "failed": 0,
        }

    summary = {
        "success": 0,
        "skipped": len(EXPECTED_ENDPOINTS) - len(pending),
        "failed": 0,
    }

    for index, (filename, url, filepath, existed) in enumerate(
        pending,
        start=1,
    ):
        if existed:
            quarantine_path = quarantine_invalid_json(filepath)
            write_log(
                event_id=event_id,
                filename=filename,
                url=url,
                attempt=0,
                result="invalid_existing_json",
                error=f"preserved_as={quarantine_path}",
            )
            print(
                f"[INVALID] {event_id} | {filename} | preservado em {quarantine_path}"
            )

        try:
            data = fetch_json_with_retry(
                page=page,
                event_id=event_id,
                filename=filename,
                url=url,
                max_retries=args.max_retries,
                backoff_seconds=args.backoff,
                jitter_seconds=args.jitter,
            )

            save_json(
                data,
                filepath,
            )

            summary["success"] += 1
            print(
                f"[OK] {event_id} | {filename}"
            )

        except OperationalBlock:
            raise

        except Exception as error:
            summary["failed"] += 1
            print(
                f"[ERRO] {event_id} | {filename} | {error}"
            )

        if index < len(pending):
            sleep_with_jitter(
                args.endpoint_delay,
                args.jitter,
            )

    return summary


# ==========================================
# DRY RUN
# ==========================================

def list_pending(inventory, start_index=1):
    total_pending = 0
    complete_matches = 0

    for idx, match in enumerate(
        inventory,
        start=start_index,
    ):
        event_id = match["event_id"]
        home_team = match.get("home_team", "")
        away_team = match.get("away_team", "")
        pending = get_pending_endpoints(
            event_id,
            dry_run=True,
        )

        if not pending:
            complete_matches += 1
            print(
                f"[{idx}] {event_id} | {home_team} x {away_team} | completo"
            )
            continue

        total_pending += len(pending)
        pending_names = ", ".join(
            filename for filename, _, _, _ in pending
        )
        print(
            f"[{idx}] {event_id} | {home_team} x {away_team} | pendente: {pending_names}"
        )

    print(
        "\nRESUMO DRY-RUN"
    )
    print(
        f"Partidas analisadas: {len(inventory)}"
    )
    print(
        f"Partidas completas: {complete_matches}"
    )
    print(
        f"Endpoints pendentes: {total_pending}"
    )


# ==========================================
# MAIN
# ==========================================

def main():
    args = parse_args()

    inventory = load_inventory()

    start_index = max(1, args.start_index)
    start_offset = start_index - 1
    inventory = inventory[start_offset:]

    if args.limit is not None:
        inventory = inventory[:args.limit]

    total = len(inventory)
    last_index = start_index + total - 1

    MATCHES_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if args.dry_run or args.list_pending:
        list_pending(
            inventory,
            start_index=start_index,
        )
        return

    total_success = 0
    total_skipped = 0
    total_failed = 0
    blocked = False

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        try:
            for idx, match in enumerate(
                inventory,
                start=start_index
            ):
                event_id = match["event_id"]

                home_team = match["home_team"]

                away_team = match["away_team"]

                print(
                    f"\n[{idx}/{last_index}] "
                    f"{home_team} x {away_team}"
                )

                try:
                    summary = collect_match(
                        page,
                        event_id,
                        args,
                    )
                except OperationalBlock as error:
                    blocked = True
                    print(
                        f"[BLOQUEADO] {error}"
                    )
                    break

                total_success += summary["success"]
                total_skipped += summary["skipped"]
                total_failed += summary["failed"]

                if idx < last_index:
                    sleep_with_jitter(
                        args.match_delay,
                        args.jitter,
                    )

        finally:
            browser.close()

    print("\nRESUMO FINAL")
    print(
        f"Partidas planejadas: {total}"
    )
    print(
        f"Endpoints coletados: {total_success}"
    )
    print(
        f"Endpoints pulados: {total_skipped}"
    )
    print(
        f"Endpoints falhos: {total_failed}"
    )
    print(
        f"Bloqueio operacional: {blocked}"
    )
    print(
        f"Log: {COLLECTION_LOG_FILE}"
    )

    if blocked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
