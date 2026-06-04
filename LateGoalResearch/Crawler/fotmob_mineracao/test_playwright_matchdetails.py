from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://www.fotmob.com/api/data/matchDetails?matchId=4506263",
        wait_until="networkidle"
    )

    print(page.content()[:1000])

    input("Pressione ENTER para fechar...")

    browser.close()
