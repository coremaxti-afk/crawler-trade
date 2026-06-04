import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


BASE_URL = "https://v3.football.api-sports.io"
DEFAULT_OUTPUT_ROOT = Path("data/raw/api_football/spikes")
DEFAULT_REQUEST_BUDGET = 100
DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_SLEEP_SECONDS = 1.0
API_KEY_ENV_NAMES = (
    "API_FOOTBALL_KEY",
    "APIFOOTBALL_API_KEY",
    "API_SPORTS_KEY",
)

ENDPOINTS = [
    {
        "name": "fixture",
        "path": "/fixtures",
        "params": {"id": "{fixture_id}"},
        "description": "Fixture metadata, score, teams, league and status.",
    },
    {
        "name": "fixture_statistics",
        "path": "/fixtures/statistics",
        "params": {"fixture": "{fixture_id}"},
        "description": "Aggregated team match statistics.",
    },
    {
        "name": "fixture_events",
        "path": "/fixtures/events",
        "params": {"fixture": "{fixture_id}"},
        "description": "Match timeline events.",
    },
    {
        "name": "fixture_lineups",
        "path": "/fixtures/lineups",
        "params": {"fixture": "{fixture_id}"},
        "description": "Lineups, formations and player positions.",
    },
    {
        "name": "fixture_players",
        "path": "/fixtures/players",
        "params": {"fixture": "{fixture_id}"},
        "description": "Player statistics for the fixture.",
    },
    {
        "name": "predictions",
        "path": "/predictions",
        "params": {"fixture": "{fixture_id}"},
        "description": "Pre-match predictions and comparative metrics.",
    },
    {
        "name": "injuries",
        "path": "/injuries",
        "params": {"fixture": "{fixture_id}"},
        "description": "Injuries and suspensions linked to the fixture.",
    },
    {
        "name": "odds",
        "path": "/odds",
        "params": {"fixture": "{fixture_id}"},
        "description": "Pre-match odds, if available in the current plan.",
    },
    {
        "name": "live_odds",
        "path": "/odds/live",
        "params": {"fixture": "{fixture_id}"},
        "description": "Live odds, usually only useful for live fixtures.",
    },
]

DERIVED_ENDPOINTS = [
    {
        "name": "head_to_head",
        "path": "/fixtures/headtohead",
        "params": {"h2h": "{home_team_id}-{away_team_id}"},
        "description": "Head-to-head history derived from fixture teams.",
        "requires": ("home_team_id", "away_team_id"),
    },
]


class RequestBudgetExceeded(Exception):
    pass


def parse_args():
    parser = argparse.ArgumentParser(
        description="Controlled one-fixture API-Football endpoint spike."
    )
    parser.add_argument(
        "--fixture-id",
        required=True,
        help="API-Football fixture id to inspect.",
    )
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help="Root directory for raw spike output.",
    )
    parser.add_argument(
        "--request-budget",
        type=int,
        default=DEFAULT_REQUEST_BUDGET,
        help="Hard request budget for this run. Default: 100.",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=DEFAULT_SLEEP_SECONDS,
        help="Small delay between requests.",
    )
    return parser.parse_args()


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def get_api_key():
    for env_name in API_KEY_ENV_NAMES:
        value = os.environ.get(env_name)
        if value:
            return value

    names = ", ".join(API_KEY_ENV_NAMES)
    raise RuntimeError(
        f"API key not found. Set one of these environment variables: {names}"
    )


def render_params(params, fixture_id, derived_context):
    rendered = {}
    context = {"fixture_id": fixture_id}
    context.update(derived_context)

    for key, value in params.items():
        rendered[key] = value.format(**context)

    return rendered


def build_url(path, params):
    query = urlencode(params)
    return f"{BASE_URL}{path}?{query}"


def is_valid_json_file(filepath):
    if not filepath.exists():
        return False

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            json.load(f)
        return True
    except (json.JSONDecodeError, OSError):
        return False


def save_json(filepath, data):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def append_log(log_file, record):
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False))
        f.write("\n")


def normalize_errors(payload):
    errors = payload.get("errors") if isinstance(payload, dict) else None

    if not errors:
        return ""

    if isinstance(errors, dict):
        return " ".join(str(value) for value in errors.values())

    return str(errors)


def classify_payload(status_code, payload):
    if status_code in (401, 403, 429):
        return "blocked"

    if status_code < 200 or status_code >= 300:
        return "unavailable"

    if not isinstance(payload, dict):
        return "unavailable"

    errors_text = normalize_errors(payload).lower()

    if errors_text:
        paid_markers = (
            "plan",
            "subscription",
            "upgrade",
            "paid",
            "not allowed",
            "permission",
        )
        blocked_markers = (
            "rate limit",
            "limit reached",
            "invalid api key",
            "forbidden",
            "unauthorized",
        )

        if any(marker in errors_text for marker in paid_markers):
            return "paid"

        if any(marker in errors_text for marker in blocked_markers):
            return "blocked"

        return "unavailable"

    results = payload.get("results")
    response = payload.get("response")

    if results == 0:
        return "empty"

    if response in (None, [], {}):
        return "empty"

    return "useful"


def request_json(endpoint, params, api_key, timeout_seconds):
    url = build_url(endpoint["path"], params)
    request = Request(
        url,
        headers={
            "x-apisports-key": api_key,
            "Accept": "application/json",
        },
        method="GET",
    )

    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8")
            payload = json.loads(raw) if raw else {}
            headers = dict(response.headers.items())
            return response.status, headers, payload, None, url

    except HTTPError as error:
        raw = error.read().decode("utf-8")
        try:
            payload = json.loads(raw) if raw else {"error": raw}
        except json.JSONDecodeError:
            payload = {"error": raw}
        headers = dict(error.headers.items()) if error.headers else {}
        return error.code, headers, payload, str(error), url

    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        payload = {"error": str(error)}
        return None, {}, payload, str(error), url


def extract_fixture_team_ids(payload):
    try:
        response = payload.get("response", [])
        if not response:
            return {}

        teams = response[0].get("teams", {})
        home_id = teams.get("home", {}).get("id")
        away_id = teams.get("away", {}).get("id")

        context = {}
        if home_id and away_id:
            context["home_team_id"] = home_id
            context["away_team_id"] = away_id
        return context
    except (AttributeError, IndexError):
        return {}


def endpoint_is_available(endpoint, derived_context):
    required = endpoint.get("requires", ())
    return all(key in derived_context for key in required)


def run_endpoint(
    endpoint,
    fixture_id,
    output_dir,
    log_file,
    api_key,
    request_state,
    derived_context,
):
    filename = f"{endpoint['name']}.json"
    filepath = output_dir / filename
    params = render_params(endpoint["params"], fixture_id, derived_context)
    url = build_url(endpoint["path"], params)

    if is_valid_json_file(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            payload = json.load(f)
        classification = classify_payload(200, payload)
        return {
            "endpoint": endpoint["name"],
            "filename": filename,
            "url": url,
            "status_code": 200,
            "classification": classification,
            "result": "skip_existing",
            "requests_consumed": request_state["count"],
        }, payload

    if request_state["count"] >= request_state["budget"]:
        raise RequestBudgetExceeded(
            f"Request budget reached before {endpoint['name']}"
        )

    request_state["count"] += 1
    attempt = request_state["count"]

    status_code, headers, payload, error, final_url = request_json(
        endpoint=endpoint,
        params=params,
        api_key=api_key,
        timeout_seconds=request_state["timeout_seconds"],
    )
    classification = classify_payload(status_code or 0, payload)
    result = "success" if error is None and status_code == 200 else classification

    save_json(filepath, payload)

    log_record = {
        "timestamp": utc_now(),
        "fixture_id": fixture_id,
        "endpoint": endpoint["name"],
        "filename": filename,
        "url": final_url,
        "attempt": 1,
        "request_number": attempt,
        "status_code": status_code,
        "result": result,
        "classification": classification,
        "api_requests_limit": headers.get("x-ratelimit-requests-limit"),
        "api_requests_remaining": headers.get("x-ratelimit-requests-remaining"),
        "api_rate_limit_limit": headers.get("x-ratelimit-limit"),
        "api_rate_limit_remaining": headers.get("x-ratelimit-remaining"),
    }

    if error:
        log_record["error"] = error

    append_log(log_file, log_record)

    return {
        "endpoint": endpoint["name"],
        "filename": filename,
        "url": final_url,
        "status_code": status_code,
        "classification": classification,
        "result": result,
        "requests_consumed": request_state["count"],
    }, payload


def summarize_results(fixture_id, output_dir, request_count, endpoint_results):
    grouped = {
        "useful": [],
        "empty": [],
        "blocked": [],
        "unavailable": [],
        "paid": [],
        "skipped": [],
    }

    for item in endpoint_results:
        if item["result"] == "skip_existing":
            grouped["skipped"].append(item)
        else:
            grouped.setdefault(item["classification"], []).append(item)

    lines = [
        f"# API-Football Fixture Spike - {fixture_id}",
        "",
        "## Scope",
        "",
        "- One fixture only.",
        "- Raw JSON only.",
        "- No database/importer/features/modeling changes.",
        "- SofaScore is not replaced by this spike.",
        "",
        "## Requests",
        "",
        f"Requests consumed in this run: {request_count}",
        f"Request budget: {DEFAULT_REQUEST_BUDGET}",
        "",
        "## Endpoints Tested",
        "",
        "| Endpoint | Status | Classification | File |",
        "|---|---:|---|---|",
    ]

    for item in endpoint_results:
        status = item["status_code"] if item["status_code"] is not None else "n/a"
        lines.append(
            f"| {item['endpoint']} | {status} | {item['classification']} | {item['filename']} |"
        )

    sections = [
        ("Useful Endpoints", "useful"),
        ("Empty Endpoints", "empty"),
        ("Blocked Endpoints", "blocked"),
        ("Unavailable Endpoints", "unavailable"),
        ("Paid/Plan-Limited Endpoints", "paid"),
        ("Skipped Existing Raw JSON", "skipped"),
    ]

    for title, key in sections:
        lines.extend(["", f"## {title}", ""])
        values = grouped.get(key, [])
        if not values:
            lines.append("- None")
        else:
            for item in values:
                lines.append(f"- {item['endpoint']} -> {item['filename']}")

    useful_names = [item["endpoint"] for item in grouped.get("useful", [])]
    lines.extend([
        "",
        "## Potential SofaScore Complement/Substitution",
        "",
    ])

    if not useful_names:
        lines.append(
            "No useful endpoint was confirmed in this run. API-Football cannot be evaluated as a SofaScore complement from this fixture alone."
        )
    else:
        lines.append(
            "Potential complement confirmed for this fixture through: " + ", ".join(useful_names) + "."
        )
        lines.append(
            "This is only an empirical spike; it does not officially replace SofaScore."
        )

    summary_path = output_dir / "summary.md"
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    args = parse_args()
    fixture_id = str(args.fixture_id)
    api_key = get_api_key()
    output_dir = Path(args.output_root) / f"fixture_{fixture_id}"
    log_file = output_dir / "request_log.jsonl"
    output_dir.mkdir(parents=True, exist_ok=True)

    request_state = {
        "count": 0,
        "budget": min(args.request_budget, DEFAULT_REQUEST_BUDGET),
        "timeout_seconds": DEFAULT_TIMEOUT_SECONDS,
    }
    derived_context = {}
    endpoint_results = []

    for endpoint in ENDPOINTS:
        result, payload = run_endpoint(
            endpoint=endpoint,
            fixture_id=fixture_id,
            output_dir=output_dir,
            log_file=log_file,
            api_key=api_key,
            request_state=request_state,
            derived_context=derived_context,
        )
        endpoint_results.append(result)

        if endpoint["name"] == "fixture":
            derived_context.update(extract_fixture_team_ids(payload))

        if args.sleep_seconds > 0:
            time.sleep(args.sleep_seconds)

    for endpoint in DERIVED_ENDPOINTS:
        if not endpoint_is_available(endpoint, derived_context):
            endpoint_results.append({
                "endpoint": endpoint["name"],
                "filename": f"{endpoint['name']}.json",
                "url": "not requested - missing derived fixture context",
                "status_code": None,
                "classification": "unavailable",
                "result": "missing_context",
                "requests_consumed": request_state["count"],
            })
            continue

        result, _ = run_endpoint(
            endpoint=endpoint,
            fixture_id=fixture_id,
            output_dir=output_dir,
            log_file=log_file,
            api_key=api_key,
            request_state=request_state,
            derived_context=derived_context,
        )
        endpoint_results.append(result)

        if args.sleep_seconds > 0:
            time.sleep(args.sleep_seconds)

    summarize_results(
        fixture_id=fixture_id,
        output_dir=output_dir,
        request_count=request_state["count"],
        endpoint_results=endpoint_results,
    )

    print(f"Fixture: {fixture_id}")
    print(f"Requests consumed: {request_state['count']}")
    print(f"Output: {output_dir}")
    print(f"Log: {log_file}")
    print(f"Summary: {output_dir / 'summary.md'}")


if __name__ == "__main__":
    main()
