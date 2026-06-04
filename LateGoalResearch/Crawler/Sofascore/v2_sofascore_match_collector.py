import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


# ==========================================
# CONFIG
# ==========================================

LEAGUE_DIR = Path(
    "data/raw/sofascore/premier_league_61627"
)

INVENTORY_FILE = LEAGUE_DIR / "inventory.json"

MATCHES_DIR = LEAGUE_DIR / "matches"

MAX_MATCHES = None

DELAY_SECONDS = 2


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
# GET JSON
# ==========================================

def get_json(page, url):

    response = page.goto(
        url,
        wait_until="networkidle",
        timeout=60000
    )

    if response is None:
        raise Exception("Sem resposta")

    if response.status != 200:
        raise Exception(
            f"HTTP {response.status}"
        )

    body = page.locator("body").inner_text()

    return json.loads(body)


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
# COLLECT MATCH
# ==========================================

def collect_match(page, event_id):

    match_dir = MATCHES_DIR / str(event_id)

    event_file = match_dir / "event.json"

    if event_file.exists():

        print(
            f"[SKIP] {event_id}"
        )

        return

    match_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    endpoints = {
        "event.json":
            f"https://www.sofascore.com/api/v1/event/{event_id}",

        "statistics.json":
            f"https://www.sofascore.com/api/v1/event/{event_id}/statistics",

        "incidents.json":
            f"https://www.sofascore.com/api/v1/event/{event_id}/incidents",

        "lineups.json":
            f"https://www.sofascore.com/api/v1/event/{event_id}/lineups",

        "h2h.json":
            f"https://www.sofascore.com/api/v1/event/{event_id}/h2h",
    }

    for filename, url in endpoints.items():

        try:

            data = get_json(
                page,
                url
            )

            save_json(
                data,
                match_dir / filename
            )

        except Exception as e:

            print(
                f"[ERRO] {event_id} | {filename} | {e}"
            )


# ==========================================
# MAIN
# ==========================================

def main():

    inventory = load_inventory()

    if MAX_MATCHES is not None:

        inventory = inventory[:MAX_MATCHES]

    total = len(inventory)

    MATCHES_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        for idx, match in enumerate(
            inventory,
            start=1
        ):

            event_id = match["event_id"]

            home_team = match["home_team"]

            away_team = match["away_team"]

            print(
                f"\n[{idx}/{total}] "
                f"{home_team} x {away_team}"
            )

            collect_match(
                page,
                event_id
            )

            time.sleep(
                DELAY_SECONDS
            )

        browser.close()

    print("\nFINALIZADO")


if __name__ == "__main__":
    main()
