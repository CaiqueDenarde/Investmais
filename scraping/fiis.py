# fiis.py
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL_FII = "https://www.fundamentus.com.br/fii_resultado.php"

def get_fiis():
    """
    Coleta todos os FIIs do Fundamentus usando Playwright.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(URL_FII)

        # Espera a primeira tabela carregar
        page.wait_for_selector("table")

        html = page.content()

        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table")
        thead = table.find("thead")
        tbody = table.find("tbody")

        colunas = [th.get_text(strip=True) for th in thead.find_all("th")]
        if colunas:
            colunas[0] = "Fii"

        dados = []
        for tr in tbody.find_all("tr"):
            cols = [td.get_text(strip=True) for td in tr.find_all("td")]
            if cols:
                dados.append(dict(zip(colunas, cols)))

        browser.close()
        print(f"Quantidade de FIIs Encontrados: {len(dados)}")
        return dados
