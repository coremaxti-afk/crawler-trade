from playwright.sync_api import sync_playwright

MATCH_URL = "https://www.fotmob.com/pt-BR/matches/fulham-vs-manchester-united/3cqww9#4506263"

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    with page.expect_response(
        lambda r: "matchDetails" in r.url,
        timeout=60000
    ) as response_info:

        page.goto(
            MATCH_URL,
            wait_until="domcontentloaded"
        )

    response = response_info.value

    print("MATCHDETAILS ENCONTRADO")
    print(response.url)

    try:

        print("Status:", response.status)

        headers = response.headers

        print(
            "Content-Type:",
            headers.get("content-type")
        )

        print("Headers OK")

    except Exception as e:

        print("Erro:", e)

    browser.close()
