from playwright.sync_api import sync_playwright
import json

EVENT_ID = 14023951

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        f"https://www.sofascore.com/api/v1/event/14023951/lineups",
        wait_until="networkidle"
    )

    print(page.locator("body").inner_text()[:1000])

    browser.close()
