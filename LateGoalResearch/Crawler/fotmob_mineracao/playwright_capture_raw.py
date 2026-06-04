from playwright.sync_api import sync_playwright

MATCH_URL = "https://www.fotmob.com/pt-BR/matches/fulham-vs-manchester-united/3cqww9#4506263"

with sync_playwright() as p:

    ontext = p.chromium.launch_persistent_context(
    user_data_dir=r"C:\Users\ludim\AppData\Local\Microsoft\Edge\User Data",
    channel="msedge",
    headless=False
)

page = context.new_page()

    def handle_response(response):

        if "matchDetails" in response.url:

            print("\n================================================")
            print("MATCHDETAILS")
            print("================================================")

            print("URL:")
            print(response.url)

            print("\nSTATUS:")
            print(response.status)

            print("\nHEADERS:")
            print(response.headers)

    page.on(
        "response",
        handle_response
    )

    page.goto(
        MATCH_URL,
        wait_until="networkidle"
    )

    page.wait_for_timeout(20000)

    context.close()
