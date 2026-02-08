from playwright.sync_api import sync_playwright

URL_ACOES = "https://www.fundamentus.com.br/resultado.php"

def get_acoes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # abre a página
        page.goto(URL_ACOES, timeout=120000)

        # espera a tabela renderizada via JS
        xpath_tabela = "/html/body/div[1]/div[2]/table"
        page.wait_for_selector(f"xpath={xpath_tabela}", timeout=120000)

        table = page.query_selector(f"xpath={xpath_tabela}")

        # pega os headers
        headers = [th.inner_text().strip() for th in table.query_selector_all("thead th")]
        if headers:
            headers[0] = "Ação"

        # coleta dados
        dados = []
        for row in table.query_selector_all("tbody tr"):
            cols = [td.inner_text().strip() for td in row.query_selector_all("td")]
            if cols:
                dados.append(dict(zip(headers, cols)))

        browser.close()
        return dados
