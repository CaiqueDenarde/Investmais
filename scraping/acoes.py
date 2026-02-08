from playwright.sync_api import sync_playwright

URL_ACAO = "https://www.fundamentus.com.br/resultado.php"

def get_acoes():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu"
            ]
        )

        page = browser.new_page()

        # Vai direto para a página FINAL (sem submit JS)
        page.goto(URL_ACAO, wait_until="networkidle", timeout=120000)

        # Aguarda QUALQUER tabela existir
        page.wait_for_selector("table", timeout=120000)

        # Debug HTML (mantenha no Actions!)
        with open("debug_acoes.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        tabela = page.query_selector("table")
        rows = tabela.query_selector_all("tbody tr")
        headers = [th.inner_text().strip() for th in tabela.query_selector_all("thead th")]

        if headers:
            headers[0] = "Ação"

        dados = []
        for row in rows:
            cols = [td.inner_text().strip() for td in row.query_selector_all("td")]
            if len(cols) == len(headers):
                dados.append(dict(zip(headers, cols)))

        browser.close()
        return dados
