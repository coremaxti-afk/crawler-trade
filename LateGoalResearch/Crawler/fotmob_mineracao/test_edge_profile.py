from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    context = p.chromium.launch_persistent_context(
        user_data_dir=r"C:\Users\ludim\AppData\Local\Microsoft\Edge\User Data",
        channel="msedge",
        headless=False
    )

    page = context.new_page()

    page.goto(
        "https://www.fotmob.com/pt-BR/matches/fulham-vs-manchester-united/3cqww9#4506263",
        wait_until="networkidle"
    )

    print("Página carregada.")

    input("Pressione ENTER para fechar...")

    context.close()
