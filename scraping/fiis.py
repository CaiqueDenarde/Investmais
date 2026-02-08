from playwright.sync_api import sync_playwright

URL_FIIS = "https://www.fundamentus.com.br/fii_resultado.php"

def get_fiis():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL_FIIS, timeout=60000)

        page.wait_for_selector("xpath=/html/body/div[1]/div[2]/table", timeout=60000)

        table = page.query_selector("xpath=/html/body/div[1]/div[2]/table")

        headers = [th.inner_text().strip() for th in table.query_selector_all("thead th")]
        if headers:
            headers[0] = "FII"

        dados = []
        for row in table.query_selector_all("tbody tr"):
            cols = [td.inner_text().strip() for td in row.query_selector_all("td")]
            if cols:
                dados.append(dict(zip(headers, cols)))

        browser.close()
        return dados
