from playwright.sync_api import sync_playwright
import json
from pathlib import Path

EVENT_ID = 14023951

ENDPOINTS = {
    "event": "",
    "statistics": "/statistics",
    "incidents": "/incidents",
    "lineups": "/lineups",
    "h2h": "/h2h",
}


def fetch_json(page, url):
    page.goto(url, wait_until="networkidle")
    content = page.locator("body").inner_text()
    return json.loads(content)


def save_json(event_id, filename, data):
    folder = Path(f"data/raw/sofascore/{event_id}")
    folder.mkdir(parents=True, exist_ok=True)

    filepath = folder / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"[OK] {filepath}")


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    for name, suffix in ENDPOINTS.items():

        url = (
            f"https://www.sofascore.com/api/v1/event/"
            f"{EVENT_ID}{suffix}"
        )

        print(f"Coletando: {url}")

        data = fetch_json(page, url)

        save_json(
            EVENT_ID,
            f"{name}.json",
            data
        )

    browser.close()

print("Coleta finalizada.")
