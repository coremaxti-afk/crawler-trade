"""Controlled API-Football free-plan sweep.

Experimental Data Acquisition script. It saves raw JSON only and does not touch
PostgreSQL, importers, datasets, features, models, or SofaScore collectors.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import time
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://v3.football.api-sports.io"
ABSOLUTE_REQUEST_LIMIT = 100
DEFAULT_REQUEST_BUDGET = 95
DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_SLEEP_SECONDS = 1.0
DEFAULT_OUTPUT_ROOT = Path("data/raw/api_football/sweeps")
DEFAULT_DOCS_ROOT = Path("docs/03_SOURCES/API_FOOTBALL")
API_KEY_ENV_NAMES = ("API_FOOTBALL_KEY", "APIFOOTBALL_API_KEY", "API_SPORTS_KEY")

ENDPOINTS = [
    ("fixture", "fixture.json", "/fixtures", {"id": "{fixture_id}"}),
    ("fixture_events", "fixture_events.json", "/fixtures/events", {"fixture": "{fixture_id}"}),
    ("fixture_statistics", "fixture_statistics.json", "/fixtures/statistics", {"fixture": "{fixture_id}"}),
    ("fixture_lineups", "fixture_lineups.json", "/fixtures/lineups", {"fixture": "{fixture_id}"}),
    ("fixture_players", "fixture_players.json", "/fixtures/players", {"fixture": "{fixture_id}"}),
    ("predictions", "predictions.json", "/predictions", {"fixture": "{fixture_id}"}),
    ("injuries", "injuries.json", "/injuries", {"fixture": "{fixture_id}"}),
    ("odds", "odds.json", "/odds", {"fixture": "{fixture_id}"}),
    ("live_odds", "live_odds.json", "/odds/live", {"fixture": "{fixture_id}"}),
    ("head_to_head", "head_to_head.json", "/fixtures/headtohead", {"h2h": "{home_team_id}-{away_team_id}"}),
]

PAID_MARKERS = ("plan", "subscription", "upgrade", "paid", "not allowed", "permission")
BLOCKED_MARKERS = ("rate limit", "limit reached", "forbidden", "unauthorized", "invalid api key")


class RequestBudgetExceeded(Exception):
    pass


class ApiLimitReached(Exception):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Controlled API-Football free-plan coverage sweep.")
    parser.add_argument("--sweep-date", default=date.today().strftime("%Y%m%d"))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--docs-root", default=str(DEFAULT_DOCS_ROOT))
    parser.add_argument("--request-budget", type=int, default=DEFAULT_REQUEST_BUDGET)
    parser.add_argument("--max-fixtures", type=int, default=5)
    parser.add_argument("--include-live", action="store_true")
    parser.add_argument("--sleep-seconds", type=float, default=DEFAULT_SLEEP_SECONDS)
    parser.add_argument("--timeout-seconds", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def api_key() -> str:
    for name in API_KEY_ENV_NAMES:
        value = os.environ.get(name)
        if value:
            return value
    raise RuntimeError("Set API_FOOTBALL_KEY, APIFOOTBALL_API_KEY or API_SPORTS_KEY.")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_url(path: str, params: dict[str, Any]) -> str:
    return f"{BASE_URL}{path}?{urlencode(params)}"


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


def items(payload: Any) -> list[Any]:
    if not isinstance(payload, dict):
        return []
    response = payload.get("response")
    if isinstance(response, list):
        return response
    if response in (None, {}, ""):
        return []
    return [response]


def non_empty(value: Any) -> bool:
    if value in (None, "", [], {}):
        return False
    if isinstance(value, list):
        return any(non_empty(item) for item in value)
    if isinstance(value, dict):
        return any(non_empty(item) for item in value.values())
    return True


def error_text(payload: Any) -> str:
    errors = payload.get("errors") if isinstance(payload, dict) else None
    if not errors:
        return ""
    if isinstance(errors, dict):
        return " ".join(str(value) for value in errors.values())
    return str(errors)


def classify(endpoint: str, status_code: int | None, payload: Any) -> str:
    if status_code in (401, 403, 429):
        return "bloqueado"
    if status_code is None or status_code in (404, 410):
        return "indisponivel"
    if status_code < 200 or status_code >= 300 or not isinstance(payload, dict):
        return "erro"
    errors = error_text(payload).lower()
    if errors:
        if any(marker in errors for marker in PAID_MARKERS):
            return "limitado_plano"
        if any(marker in errors for marker in BLOCKED_MARKERS):
            return "bloqueado"
        return "indisponivel"
    response_items = items(payload)
    if payload.get("results") == 0 or not response_items:
        return "vazio"
    if endpoint == "fixture_statistics":
        filled = 0
        total = 0
        for team_record in response_items:
            for stat in team_record.get("statistics", []) if isinstance(team_record, dict) else []:
                total += 1
                filled += 1 if non_empty(stat.get("value")) else 0
        if filled == 0:
            return "vazio"
        return "util" if total and filled / total >= 0.35 else "util_parcial"
    if endpoint == "fixture_players":
        return "util" if any(non_empty(team.get("players")) for team in response_items if isinstance(team, dict)) else "vazio"
    if endpoint == "fixture_lineups":
        return "util" if any(non_empty(team.get("startXI")) for team in response_items if isinstance(team, dict)) else "vazio"
    return "util" if non_empty(response_items) else "vazio"


def enforce_budget(state: dict[str, Any]) -> None:
    if state["count"] >= state["budget"]:
        raise RequestBudgetExceeded(f"Request budget reached: {state['count']}/{state['budget']}")
    if state.get("daily_remaining") is not None and state["daily_remaining"] <= 0:
        raise ApiLimitReached("Daily API request remaining header reached zero.")
    if state.get("short_remaining") is not None and state["short_remaining"] <= 0:
        wait = state.get("rate_limit_sleep_seconds", 65)
        print(f"Short rate window exhausted; sleeping {wait}s before next request.")
        time.sleep(wait)
        state["short_remaining"] = None


def request_json(path: str, params: dict[str, Any], key: str, state: dict[str, Any], log_file: Path, phase: str, endpoint: str | None = None, fixture_id: str | None = None, output_file: str | None = None) -> tuple[int | None, Any, str]:
    enforce_budget(state)
    url = build_url(path, params)
    state["count"] += 1
    request_number = state["count"]
    req = Request(url, headers={"x-apisports-key": key, "Accept": "application/json"}, method="GET")
    status_code = None
    headers: dict[str, str] = {}
    payload: Any = {}
    err = None
    try:
        with urlopen(req, timeout=state["timeout_seconds"]) as response:
            status_code = int(response.status)
            headers = dict(response.headers.items())
            payload = json.loads(response.read().decode("utf-8") or "{}")
    except HTTPError as exc:
        status_code = int(exc.code)
        headers = dict(exc.headers.items()) if exc.headers else {}
        raw = exc.read().decode("utf-8")
        try:
            payload = json.loads(raw) if raw else {"error": raw}
        except json.JSONDecodeError:
            payload = {"error": raw}
        err = str(exc)
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        payload = {"error": str(exc)}
        err = str(exc)

    for header, target in (("x-ratelimit-requests-remaining", "daily_remaining"), ("x-ratelimit-remaining", "short_remaining")):
        try:
            state[target] = int(headers[header]) if header in headers else None
        except ValueError:
            state[target] = None

    classification = classify(endpoint or phase, status_code, payload)
    append_jsonl(log_file, {
        "timestamp": utc_now(),
        "request_number": request_number,
        "phase": phase,
        "fixture_id": fixture_id,
        "endpoint": endpoint,
        "output_file": output_file,
        "url": url,
        "status_code": status_code,
        "classification": classification,
        "api_requests_limit": headers.get("x-ratelimit-requests-limit"),
        "api_requests_remaining": headers.get("x-ratelimit-requests-remaining"),
        "api_rate_limit_limit": headers.get("x-ratelimit-limit"),
        "api_rate_limit_remaining": headers.get("x-ratelimit-remaining"),
        "error": err,
    })
    if classification == "bloqueado":
        raise ApiLimitReached(f"Blocked/limited response at request {request_number}: {url}")
    return status_code, payload, url


def fixture_meta(item: dict[str, Any]) -> dict[str, Any]:
    fixture = item.get("fixture", {})
    league = item.get("league", {})
    teams = item.get("teams", {})
    goals = item.get("goals", {})
    status = fixture.get("status", {})
    return {
        "fixture_id": str(fixture.get("id")),
        "date": fixture.get("date"),
        "status_short": status.get("short"),
        "league": league.get("name"),
        "country": league.get("country"),
        "season": league.get("season"),
        "home_team_id": teams.get("home", {}).get("id"),
        "away_team_id": teams.get("away", {}).get("id"),
        "home_team": teams.get("home", {}).get("name"),
        "away_team": teams.get("away", {}).get("name"),
        "home_goals": goals.get("home"),
        "away_goals": goals.get("away"),
    }


def choose_fixtures(discovered: list[dict[str, Any]], max_fixtures: int) -> list[dict[str, Any]]:
    candidates = [item for item in discovered if item.get("fixture_id") and item.get("status_short") in {"FT", "AET", "PEN"}]
    candidates.sort(key=lambda item: (item.get("league") or "", item.get("date") or ""))
    selected = []
    seen = set()
    for item in candidates:
        key = (item.get("country"), item.get("league"))
        if key in seen:
            continue
        selected.append(item)
        seen.add(key)
        if len(selected) >= max_fixtures:
            return selected
    for item in candidates:
        if item not in selected:
            selected.append(item)
        if len(selected) >= max_fixtures:
            break
    return selected


def discover(key: str, output_dir: Path, log_file: Path, state: dict[str, Any], max_fixtures: int, sleep_seconds: float) -> list[dict[str, Any]]:
    discovery_dir = output_dir / "discovery"
    selected_file = discovery_dir / "selected_fixtures.json"
    if selected_file.exists():
        return json.loads(selected_file.read_text(encoding="utf-8"))[:max_fixtures]
    found = []
    today = date.today()
    for offset in range(4):
        day = (today - timedelta(days=offset)).isoformat()
        _, payload, _ = request_json("/fixtures", {"date": day, "status": "FT"}, key, state, log_file, "discovery", endpoint="discovery_fixtures_ft")
        save_json(discovery_dir / f"fixtures_{day}_FT.json", payload)
        found.extend(fixture_meta(item) for item in items(payload) if isinstance(item, dict))
        if len(choose_fixtures(found, max_fixtures)) >= max_fixtures:
            break
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)
    selected = choose_fixtures(found, max_fixtures)
    save_json(selected_file, selected)
    return selected


def render(template: dict[str, str], fixture: dict[str, Any]) -> dict[str, str]:
    return {key: value.format(**fixture) for key, value in template.items()}


def endpoint_available(name: str, fixture: dict[str, Any]) -> bool:
    if name != "head_to_head":
        return True
    return bool(fixture.get("home_team_id") and fixture.get("away_team_id"))


def collect_fixture(key: str, output_dir: Path, log_file: Path, state: dict[str, Any], fixture: dict[str, Any], sleep_seconds: float) -> list[dict[str, Any]]:
    fixture_id = fixture["fixture_id"]
    fixture_dir = output_dir / "fixtures" / fixture_id
    results = []
    for name, filename, path, params_template in ENDPOINTS:
        filepath = fixture_dir / filename
        if filepath.exists():
            payload = json.loads(filepath.read_text(encoding="utf-8"))
            results.append({"fixture_id": fixture_id, "endpoint": name, "classification": classify(name, 200, payload), "status_code": 200})
            continue
        if not endpoint_available(name, fixture):
            results.append({"fixture_id": fixture_id, "endpoint": name, "classification": "indisponivel", "status_code": None})
            continue
        params = render(params_template, fixture)
        status_code, payload, _ = request_json(path, params, key, state, log_file, "endpoint", endpoint=name, fixture_id=fixture_id, output_file=str(filepath.relative_to(output_dir)))
        save_json(filepath, payload)
        results.append({"fixture_id": fixture_id, "endpoint": name, "classification": classify(name, status_code, payload), "status_code": status_code})
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)
    return results


def write_coverage(path: Path, fixtures: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    by_key = {(row["fixture_id"], row["endpoint"]): row["classification"] for row in results}
    endpoint_names = [endpoint[0] for endpoint in ENDPOINTS]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["fixture_id", "league", "country", "season", "date", "status", "score"] + endpoint_names)
        for fixture in fixtures:
            writer.writerow([
                fixture.get("fixture_id"), fixture.get("league"), fixture.get("country"), fixture.get("season"),
                fixture.get("date"), fixture.get("status_short"), f"{fixture.get('home_goals')}-{fixture.get('away_goals')}",
                *[by_key.get((fixture["fixture_id"], endpoint), "nao_testado") for endpoint in endpoint_names],
            ])


def write_summary(path: Path, output_dir: Path, sweep_date: str, request_count: int, fixtures: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    by_endpoint = defaultdict(list)
    for result in results:
        by_endpoint[result["endpoint"]].append(result["classification"])
    lines = [
        f"# API-Football Free Plan Sweep - {sweep_date}", "",
        "## Requests", "", f"- Total de requests consumidos: {request_count}", f"- Limite absoluto: {ABSOLUTE_REQUEST_LIMIT}", "",
        "## Fixtures Testadas", "", "| Fixture | Liga | Pais | Temporada | Data | Status | Placar |", "|---|---|---|---:|---|---|---|",
    ]
    for fixture in fixtures:
        score = f"{fixture.get('home_team')} {fixture.get('home_goals')} x {fixture.get('away_goals')} {fixture.get('away_team')}"
        lines.append(f"| {fixture.get('fixture_id')} | {fixture.get('league')} | {fixture.get('country')} | {fixture.get('season')} | {fixture.get('date')} | {fixture.get('status_short')} | {score} |")
    lines.extend(["", "## Matriz de Cobertura", "", f"- `{output_dir / 'coverage_matrix.csv'}`", "", "## Endpoints", ""])
    for endpoint, classes in by_endpoint.items():
        lines.append(f"- `{endpoint}`: {dict(Counter(classes))}")
    lines.extend(["", "## Restricoes Respeitadas", "", "- Nenhum banco/schema/importer/dataset/feature/modelagem/SofaScore foi alterado.", "- Spikes anteriores nao foram sobrescritos."])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run() -> None:
    args = parse_args()
    budget = min(args.request_budget, ABSOLUTE_REQUEST_LIMIT - 5)
    output_dir = Path(args.output_root) / f"free_plan_{args.sweep_date}"
    report_path = Path(args.docs_root) / f"API_FOOTBALL_FREE_PLAN_SWEEP_{args.sweep_date}.md"
    log_file = output_dir / "request_log.jsonl"
    if args.dry_run:
        print(f"DRY RUN output={output_dir} report={report_path} budget={budget}")
        return
    key = api_key()
    previous = len(log_file.read_text(encoding="utf-8").splitlines()) if log_file.exists() else 0
    state = {"count": previous, "budget": budget, "timeout_seconds": args.timeout_seconds, "daily_remaining": None, "short_remaining": None, "rate_limit_sleep_seconds": 65}
    output_dir.mkdir(parents=True, exist_ok=True)
    fixtures = discover(key, output_dir, log_file, state, args.max_fixtures, args.sleep_seconds)
    results = []
    stop_reason = None
    try:
        for fixture in fixtures:
            results.extend(collect_fixture(key, output_dir, log_file, state, fixture, args.sleep_seconds))
    except (ApiLimitReached, RequestBudgetExceeded) as exc:
        stop_reason = str(exc)
        print(f"STOPPED: {stop_reason}")
    write_coverage(output_dir / "coverage_matrix.csv", fixtures, results)
    write_summary(report_path, output_dir, args.sweep_date, state["count"], fixtures, results)
    if stop_reason:
        with report_path.open("a", encoding="utf-8") as file:
            file.write(f"\n## Encerramento Antecipado\n\n- Motivo: {stop_reason}\n")
    print("API-Football free-plan sweep complete")
    print(f"requests_consumed={state['count']}")
    print(f"fixtures_tested={len(fixtures)}")
    print(f"output_dir={output_dir}")
    print(f"coverage_matrix={output_dir / 'coverage_matrix.csv'}")
    print(f"request_log={log_file}")
    print(f"report={report_path}")


if __name__ == "__main__":
    run()
