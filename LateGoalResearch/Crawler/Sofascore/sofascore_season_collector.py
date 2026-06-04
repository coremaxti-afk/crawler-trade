import json
import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


# ==========================================
# CONFIGURAÇÃO
# ==========================================

UNIQUE_TOURNAMENT_ID = 17     # Premier League
SEASON_ID = 61627            # Premier League 24/25

OUTPUT_DIR = Path(
    f"data/raw/sofascore/premier_league_{SEASON_ID}"
)


# ==========================================
# PLAYWRIGHT
# ==========================================

def get_json(page, url):

    print(f"Coletando: {url}")

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
# SALVAR JSON
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
# MAIN
# ==========================================

def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        # ----------------------------------
        # ROUNDS
        # ----------------------------------

        rounds_url = (
            f"https://www.sofascore.com/api/v1/"
            f"unique-tournament/{UNIQUE_TOURNAMENT_ID}"
            f"/season/{SEASON_ID}/rounds"
        )

        rounds_data = get_json(
            page,
            rounds_url
        )

        save_json(
            rounds_data,
            OUTPUT_DIR / "rounds.json"
        )

        rounds = rounds_data["rounds"]

        print()
        print(f"Rodadas encontradas: {len(rounds)}")
        print()

        # ----------------------------------
        # EVENTS POR RODADA
        # ----------------------------------

        inventory = []

        for round_item in rounds:

            round_number = round_item["round"]

            events_url = (
                f"https://www.sofascore.com/api/v1/"
                f"unique-tournament/{UNIQUE_TOURNAMENT_ID}"
                f"/season/{SEASON_ID}"
                f"/events/round/{round_number}"
            )

            try:

                events_data = get_json(
                    page,
                    events_url
                )

                save_json(
                    events_data,
                    OUTPUT_DIR /
                    f"round_{round_number:02d}_events.json"
                )

                events = events_data.get(
                    "events",
                    []
                )

                print(
                    f"Rodada {round_number}: "
                    f"{len(events)} jogos"
                )

                for event in events:

                    inventory.append({

                        "event_id":
                            event["id"],

                        "round":
                            round_number,

                        "home_team":
                            event["homeTeam"]["name"],

                        "away_team":
                            event["awayTeam"]["name"]

                    })

                time.sleep(1)

            except Exception as e:

                print(
                    f"[ERRO] Rodada "
                    f"{round_number}: {e}"
                )

        save_json(
            inventory,
            OUTPUT_DIR / "inventory.json"
        )

        browser.close()

    print()
    print("=" * 50)
    print("FINALIZADO")
    print(f"Jogos encontrados: {len(inventory)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
