from playwright.sync_api import sync_playwright

MATCH_URL = "https://www.fotmob.com/pt-BR/matches/america-mg-vs-juventude/173cyl#5190548"

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto(
        MATCH_URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    page.wait_for_timeout(10000)

    print("Título:")
    print(page.title())

    print("\nURL atual:")
    print(page.url)

    input("\nPressione ENTER para fechar...")

    browser.close()
