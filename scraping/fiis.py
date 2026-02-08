from playwright.sync_api import sync_playwright

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.fundamentus.com.br/"
}

URL_FII = "https://www.fundamentus.com.br/fii_resultado.php"

def get_fiis():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # ← modo headless
        page = browser.new_page()
        page.set_extra_http_headers(HEADERS)
        page.goto(URL_FII, timeout=60000)
        page.wait_for_selector("table")  # espera tabela carregar

        with open("debug_fiis.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        rows = page.query_selector_all("table tbody tr")
        col_headers = [th.inner_text().strip() for th in page.query_selector_all("table thead th")]
        if col_headers:
            col_headers[0] = "Fii"

        dados = []
        for row in rows:
            cols = [td.inner_text().strip() for td in row.query_selector_all("td")]
            if cols:
                dados.append(dict(zip(col_headers, cols)))

        browser.close()
        return dados
