from playwright.sync_api import sync_playwright

URL_FII = "https://www.fundamentus.com.br/fii_resultado.php"

def get_fiis():
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
        page.goto(URL_FII, wait_until="networkidle", timeout=120000)

        page.wait_for_selector("table", timeout=120000)

        with open("debug_fiis.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        tabela = page.query_selector("table")
        rows = tabela.query_selector_all("tbody tr")
        headers = [th.inner_text().strip() for th in tabela.query_selector_all("thead th")]

        if headers:
            headers[0] = "Fii"

        dados = []
        for row in rows:
            cols = [td.inner_text().strip() for td in row.query_selector_all("td")]
            if len(cols) == len(headers):
                dados.append(dict(zip(headers, cols)))

        browser.close()
        return dados
