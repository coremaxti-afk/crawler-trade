import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


# ==========================================
# CONFIG
# ==========================================

EVENT_ID = 12436870

OUTPUT_DIR = Path(
    f"data/raw/sofascore/matches/{EVENT_ID}"
)


# ==========================================
# PLAYWRIGHT
# ==========================================

def get_json(page, url):

    print(f"\nColetando: {url}")

    response = page.goto(
        url,
        wait_until="networkidle",
        timeout=60000
    )

    if response is None:
        raise Exception("Sem resposta")

    print("Status:", response.status)

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

    print(f"[OK] {filepath}")


# ==========================================
# MAIN
# ==========================================

def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    endpoints = {
        "event.json":
            f"https://www.sofascore.com/api/v1/event/{EVENT_ID}",

        "statistics.json":
            f"https://www.sofascore.com/api/v1/event/{EVENT_ID}/statistics",

        "incidents.json":
            f"https://www.sofascore.com/api/v1/event/{EVENT_ID}/incidents",

        "lineups.json":
            f"https://www.sofascore.com/api/v1/event/{EVENT_ID}/lineups",

        "h2h.json":
            f"https://www.sofascore.com/api/v1/event/{EVENT_ID}/h2h",
    }

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        for filename, url in endpoints.items():

            try:

                data = get_json(
                    page,
                    url
                )

                save_json(
                    data,
                    OUTPUT_DIR / filename
                )

                time.sleep(1)

            except Exception as e:

                print(
                    f"[ERRO] {filename}: {e}"
                )

        browser.close()

    print("\nFINALIZADO")


if __name__ == "__main__":
    main()
