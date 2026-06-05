"""Controlled SofaScore endpoint discovery for one already collected EPL match.

Experimental Data Acquisition only. Probes a small explicit endpoint list for a
single event_id and saves raw responses under
`data/raw/sofascore/endpoint_discovery/{event_id}/`.
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

BASE_URL = "https://www.sofascore.com/api/v1/event/{event_id}/{suffix}"
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_LEAGUE_DIR = SCRIPT_DIR / "data/raw/sofascore/premier_league_61627"
DEFAULT_OUTPUT_ROOT = SCRIPT_DIR / "data/raw/sofascore/endpoint_discovery"
REQUEST_TIMEOUT_MS = 60000
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
CORE_REQUIRED_FILES = ("event.json", "incidents.json", "statistics.json", "graph.json")

ENDPOINT_CANDIDATES = [
    ("graph", "graph"),
    ("shotmap", "shotmap"),
    ("statistics", "statistics"),
    ("statistics_overall", "statistics/overall"),
    ("statistics_period_1", "statistics/period/1"),
    ("statistics_period_2", "statistics/period/2"),
    ("incidents", "incidents"),
    ("lineups", "lineups"),
    ("lineups_confirmed", "lineups/confirmed"),
    ("player_statistics", "player-statistics"),
    ("players_statistics", "players/statistics"),
    ("heatmap", "heatmap"),
    ("average_positions", "average-positions"),
    ("momentum", "momentum"),
    ("attack_momentum", "attack-momentum"),
    ("win_probability", "win-probability"),
    ("votes", "votes"),
    ("details", "details"),
    ("best_players", "best-players"),
    ("managers", "managers"),
]


class HttpStatusError(Exception):
    def __init__(self, status_code: int, body: str = ""):
        super().__init__(f"HTTP {status_code}")
        self.status_code = status_code
        self.body = body


class OperationalBlock(Exception):
    """Raised when HTTP 403 requires immediate stop."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Controlled SofaScore endpoint discovery for one EPL event.")
    parser.add_argument("--event-id", default=None, help="Optional SofaScore event id. If omitted, one local importable match is selected.")
    parser.add_argument("--limit-endpoints", type=int, default=20)
    parser.add_argument("--request-delay", type=float, default=10.0)
    parser.add_argument("--jitter", type=float, default=10.0)
    parser.add_argument("--backoff", type=float, default=120.0)
    parser.add_argument("--max-retries", type=int, default=1)
    parser.add_argument("--league-dir", default=str(DEFAULT_LEAGUE_DIR))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--manual-warmup", action="store_true")
    parser.add_argument("--warmup-url", default="https://www.sofascore.com/")
    parser.add_argument("--dry-run", action="store_true", help="Select match and list endpoints without HTTP requests.")
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def is_valid_json(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        load_json(path)
        return True
    except (json.JSONDecodeError, OSError):
        return False


def graph_is_valid(path: Path) -> bool:
    if not is_valid_json(path):
        return False
    payload = load_json(path)
    points = payload.get("graphPoints") if isinstance(payload, dict) else None
    return isinstance(points, list) and bool(points)


def match_has_required_files(match_dir: Path) -> bool:
    for filename in CORE_REQUIRED_FILES:
        path = match_dir / filename
        if filename == "graph.json":
            if not graph_is_valid(path):
                return False
        elif not is_valid_json(path):
            return False
    return True


def row_event_id(row: Any) -> str | None:
    if isinstance(row, dict):
        value = row.get("event_id") or row.get("id") or row.get("sofascore_event_id")
        return str(value) if value is not None else None
    return None


def select_event_id(league_dir: Path, explicit_event_id: str | None) -> str:
    matches_dir = league_dir / "matches"
    if explicit_event_id:
        match_dir = matches_dir / str(explicit_event_id)
        if not match_has_required_files(match_dir):
            raise SystemExit(f"Event {explicit_event_id} is missing one of: {', '.join(CORE_REQUIRED_FILES)}")
        return str(explicit_event_id)
    inventory_file = league_dir / "inventory.json"
    if inventory_file.exists():
        inventory = load_json(inventory_file)
        if isinstance(inventory, list):
            for row in inventory:
                event_id = row_event_id(row)
                if event_id and match_has_required_files(matches_dir / event_id):
                    return event_id
    for match_dir in sorted(matches_dir.iterdir() if matches_dir.exists() else []):
        if match_dir.is_dir() and match_has_required_files(match_dir):
            return match_dir.name
    raise SystemExit("No local match found with event.json, incidents.json, statistics.json and valid graph.json.")


def event_label(league_dir: Path, event_id: str) -> dict[str, Any]:
    event_path = league_dir / "matches" / event_id / "event.json"
    if not event_path.exists():
        return {"event_id": event_id}
    payload = load_json(event_path)
    event = payload.get("event", payload) if isinstance(payload, dict) else {}
    home = event.get("homeTeam", {}) if isinstance(event, dict) else {}
    away = event.get("awayTeam", {}) if isinstance(event, dict) else {}
    return {
        "event_id": event_id,
        "home_team": home.get("name"),
        "away_team": away.get("name"),
        "start_timestamp": event.get("startTimestamp") if isinstance(event, dict) else None,
        "status": event.get("status", {}).get("description") if isinstance(event, dict) else None,
    }


def endpoint_url(event_id: str, suffix: str) -> str:
    return BASE_URL.format(event_id=event_id, suffix=suffix)


def output_paths(output_root: Path, event_id: str) -> dict[str, Path]:
    root = output_root / event_id
    return {
        "root": root,
        "responses": root / "responses",
        "errors": root / "errors",
        "log": root / "request_log.jsonl",
        "summary": root / "summary.md",
    }


def write_log(log_file: Path, record: dict[str, Any]) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False))
        file.write("\n")


def backup_invalid(path: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_dir = path.parent / "_invalid_backup"
    backup_dir.mkdir(parents=True, exist_ok=True)
    target = backup_dir / f"{path.name}.{stamp}.invalid"
    counter = 1
    while target.exists():
        target = backup_dir / f"{path.name}.{stamp}.{counter}.invalid"
        counter += 1
    shutil.move(str(path), str(target))
    return target


def contains_key(value: Any, names: set[str]) -> bool:
    if isinstance(value, dict):
        if any(key in names for key in value.keys()):
            return True
        return any(contains_key(item, names) for item in value.values())
    if isinstance(value, list):
        return any(contains_key(item, names) for item in value)
    return False


def classify_payload(status_code: int | None, payload: Any) -> str:
    if status_code == 403:
        return "blocked_403"
    if status_code in (404, 410):
        return "not_found"
    if status_code is None:
        return "error"
    if status_code < 200 or status_code >= 300:
        return "error"
    if isinstance(payload, dict):
        if payload in ({}, {"error": ""}):
            return "empty"
        return "useful" if any(value not in (None, "", [], {}) for value in payload.values()) else "empty"
    if isinstance(payload, list):
        return "useful" if payload else "empty"
    if isinstance(payload, str):
        return "non_json" if payload.strip() else "empty"
    return "unknown"


def payload_summary(payload: Any) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    if isinstance(payload, dict):
        summary["root_type"] = "object"
        summary["keys"] = sorted(payload.keys())[:30]
        if isinstance(payload.get("graphPoints"), list):
            summary["graph_points_count"] = len(payload["graphPoints"])
        for key in ("incidents", "events", "shotmap", "statistics", "players", "lineups", "votes"):
            if isinstance(payload.get(key), list):
                summary[f"{key}_count"] = len(payload[key])
        summary["has_minute_like_field"] = contains_key(payload, {"minute", "time", "elapsed"})
    elif isinstance(payload, list):
        summary["root_type"] = "array"
        summary["items_count"] = len(payload)
        summary["has_minute_like_field"] = contains_key(payload, {"minute", "time", "elapsed"})
    elif isinstance(payload, str):
        summary["root_type"] = "text"
        summary["text_length"] = len(payload)
    else:
        summary["root_type"] = type(payload).__name__
    return summary


def compact_summary(summary: Any) -> str:
    if not isinstance(summary, dict):
        return ""
    parts = []
    for key in ("root_type", "graph_points_count", "items_count", "incidents_count", "shotmap_count", "statistics_count", "players_count", "lineups_count", "has_minute_like_field", "text_length"):
        if key in summary:
            parts.append(f"{key}={summary[key]}")
    if "keys" in summary:
        parts.append("keys=" + ",".join(summary["keys"][:8]))
    return "; ".join(parts)


def sleep_between(args: argparse.Namespace) -> None:
    time.sleep(args.request_delay + random.uniform(0, max(0.0, args.jitter)))


def fetch_with_playwright(page: Any, url: str) -> tuple[int, str | None, Any]:
    response = page.goto(url, wait_until="networkidle", timeout=REQUEST_TIMEOUT_MS)
    if response is None:
        raise RuntimeError("No response returned by page.goto")
    status_code = int(response.status)
    content_type = response.headers.get("content-type")
    body = page.locator("body").inner_text(timeout=REQUEST_TIMEOUT_MS)
    if status_code != 200:
        raise HttpStatusError(status_code, body)
    try:
        return status_code, content_type, json.loads(body)
    except json.JSONDecodeError:
        return status_code, content_type, body


def safe_parse_json(text: str) -> Any:
    try:
        return json.loads(text) if text else {}
    except json.JSONDecodeError:
        return {"text": text}


def save_response(paths: dict[str, Path], endpoint_name: str, status_code: int | None, payload: Any, error: str | None = None) -> str:
    if error is not None or (status_code is not None and status_code >= 400):
        target = paths["errors"] / f"{endpoint_name}.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps({"status_code": status_code, "error": error, "payload": payload}, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(target)
    if isinstance(payload, (dict, list)):
        target = paths["responses"] / f"{endpoint_name}.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and is_valid_json(target):
            return str(target)
        if target.exists() and not is_valid_json(target):
            backup_invalid(target)
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(target)
    target = paths["responses"] / f"{endpoint_name}.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.read_text(encoding="utf-8", errors="ignore").strip():
        return str(target)
    target.write_text(str(payload), encoding="utf-8")
    return str(target)


def collect_endpoint(page: Any, event_id: str, endpoint_name: str, suffix: str, paths: dict[str, Path], args: argparse.Namespace) -> dict[str, Any]:
    url = endpoint_url(event_id, suffix)
    existing_json = paths["responses"] / f"{endpoint_name}.json"
    existing_txt = paths["responses"] / f"{endpoint_name}.txt"
    if is_valid_json(existing_json):
        payload = load_json(existing_json)
        record = {"timestamp": utc_now(), "event_id": event_id, "endpoint": endpoint_name, "suffix": suffix, "url": url, "status_code": None, "result": "skip_existing_valid", "classification": classify_payload(200, payload), "saved_path": str(existing_json), "payload_summary": payload_summary(payload)}
        write_log(paths["log"], record)
        return record
    if existing_txt.exists() and existing_txt.read_text(encoding="utf-8", errors="ignore").strip():
        record = {"timestamp": utc_now(), "event_id": event_id, "endpoint": endpoint_name, "suffix": suffix, "url": url, "status_code": None, "result": "skip_existing_text", "classification": "non_json", "saved_path": str(existing_txt), "payload_summary": {"root_type": "text"}}
        write_log(paths["log"], record)
        return record

    last_error: Exception | None = None
    for attempt in range(1, args.max_retries + 2):
        try:
            status_code, content_type, payload = fetch_with_playwright(page, url)
            saved_path = save_response(paths, endpoint_name, status_code, payload)
            record = {"timestamp": utc_now(), "event_id": event_id, "endpoint": endpoint_name, "suffix": suffix, "url": url, "attempt": attempt, "status_code": status_code, "result": "success", "classification": classify_payload(status_code, payload), "content_type": content_type, "saved_path": saved_path, "payload_summary": payload_summary(payload)}
            write_log(paths["log"], record)
            return record
        except HttpStatusError as error:
            payload = safe_parse_json(error.body)
            saved_path = save_response(paths, endpoint_name, error.status_code, payload, str(error))
            record = {"timestamp": utc_now(), "event_id": event_id, "endpoint": endpoint_name, "suffix": suffix, "url": url, "attempt": attempt, "status_code": error.status_code, "result": "blocked_403" if error.status_code == 403 else "failed", "classification": classify_payload(error.status_code, payload), "saved_path": saved_path, "error": str(error)}
            write_log(paths["log"], record)
            if error.status_code == 403:
                raise OperationalBlock(f"HTTP 403 at endpoint {endpoint_name}") from error
            return record
        except Exception as error:
            last_error = error
            if attempt <= args.max_retries:
                write_log(paths["log"], {"timestamp": utc_now(), "event_id": event_id, "endpoint": endpoint_name, "suffix": suffix, "url": url, "attempt": attempt, "status_code": None, "result": "retry", "classification": "error", "error": str(error)})
                time.sleep(args.backoff)
                continue
            saved_path = save_response(paths, endpoint_name, None, {}, str(last_error))
            record = {"timestamp": utc_now(), "event_id": event_id, "endpoint": endpoint_name, "suffix": suffix, "url": url, "attempt": attempt, "status_code": None, "result": "failed", "classification": "error", "saved_path": saved_path, "error": str(last_error)}
            write_log(paths["log"], record)
            return record
    raise RuntimeError("unreachable")


def write_summary(paths: dict[str, Path], match_info: dict[str, Any], records: list[dict[str, Any]], blocked: bool) -> None:
    groups: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        groups.setdefault(record.get("classification", "unknown"), []).append(record)
    lines = [
        f"# SofaScore Endpoint Discovery - {match_info.get('event_id')}", "", "## Escopo", "",
        "Discovery controlado em uma unica partida da Premier League ja coletada localmente.", "",
        "Nao altera banco, schema, importers, datasets, features, baselines, modelagem ou coletores existentes.", "",
        "## Partida", "", f"- event_id: `{match_info.get('event_id')}`", f"- home_team: {match_info.get('home_team')}", f"- away_team: {match_info.get('away_team')}", f"- status: {match_info.get('status')}", "",
        "## Resultado Geral", "", f"- Endpoints planejados/testados: {len(records)}", f"- HTTP 403: {'sim' if blocked else 'nao'}", "",
        "## Matriz de Endpoints", "", "| Endpoint | Status | Classificacao | Resumo | Arquivo |", "|---|---:|---|---|---|",
    ]
    for record in records:
        status = record.get("status_code") if record.get("status_code") is not None else "n/a"
        lines.append(f"| `{record.get('endpoint')}` | {status} | {record.get('classification')} | {compact_summary(record.get('payload_summary', {}))} | `{record.get('saved_path', '')}` |")
    for title, key in [("Endpoints uteis", "useful"), ("Endpoints vazios", "empty"), ("Endpoints inexistentes/404", "not_found"), ("Endpoints com texto nao JSON", "non_json"), ("Endpoints com erro", "error"), ("Endpoints bloqueados", "blocked_403")]:
        lines.extend(["", f"## {title}", ""])
        rows = groups.get(key, [])
        if not rows:
            lines.append("- Nenhum")
        else:
            for row in rows:
                lines.append(f"- `{row.get('endpoint')}` -> {compact_summary(row.get('payload_summary', {}))}")
    lines.extend(["", "## Interpretacao Inicial", "", "Endpoints com `has_minute_like_field=true`, listas temporais ou chaves como `graphPoints`, `incidents` ou `shotmap` devem ser revisados pelo Data Acquisition/CTO antes de qualquer decisao arquitetural.", "", "Este discovery nao promove nenhum endpoint a fonte oficial e nao autoriza importer, feature engineering ou dataset H8.", "", "## Restricoes Respeitadas", "", "- Apenas 1 event_id foi usado.", "- Lista fixa de ate 20 endpoints candidatos.", "- Sem brute force ou variacoes infinitas.", "- Sem paralelismo.", "- Sem rotacao de IP ou bypass agressivo.", "- Sem sobrescrever JSON valido existente."])
    paths["summary"].parent.mkdir(parents=True, exist_ok=True)
    paths["summary"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    if args.limit_endpoints < 1:
        raise SystemExit("--limit-endpoints must be >= 1")
    league_dir = Path(args.league_dir)
    output_root = Path(args.output_root)
    event_id = select_event_id(league_dir, args.event_id)
    match_info = event_label(league_dir, event_id)
    endpoints = ENDPOINT_CANDIDATES[: min(args.limit_endpoints, len(ENDPOINT_CANDIDATES))]
    paths = output_paths(output_root, event_id)
    print(f"Selected event_id={event_id}")
    print(f"Match={match_info.get('home_team')} x {match_info.get('away_team')}")
    print(f"Endpoints selected={len(endpoints)}")
    print(f"Output={paths['root']}")
    if args.dry_run:
        for name, suffix in endpoints:
            print(f"- {name}: {endpoint_url(event_id, suffix)}")
        print("SAFE MODE: no HTTP requests were made.")
        return

    from playwright.sync_api import sync_playwright

    records: list[dict[str, Any]] = []
    blocked = False
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=not args.headed)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(args.warmup_url, wait_until="domcontentloaded", timeout=REQUEST_TIMEOUT_MS)
            if args.manual_warmup:
                input("Manual warmup enabled. Press ENTER when the browser session is ready...")
            for index, (endpoint_name, suffix) in enumerate(endpoints, start=1):
                print(f"[{index}/{len(endpoints)}] {endpoint_name}")
                try:
                    records.append(collect_endpoint(page, event_id, endpoint_name, suffix, paths, args))
                except OperationalBlock as error:
                    blocked = True
                    print(f"BLOCKED: {error}")
                    break
                if index < len(endpoints):
                    sleep_between(args)
        finally:
            context.close()
            browser.close()
    write_summary(paths, match_info, records, blocked)
    print("\nFINAL SUMMARY")
    print(f"event_id={event_id}")
    print(f"processed={len(records)}")
    print(f"blocked_403={blocked}")
    print(f"log={paths['log']}")
    print(f"summary={paths['summary']}")
    if blocked:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
