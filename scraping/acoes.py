# acoes.py
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL_ACAO = "https://www.fundamentus.com.br/resultado.php"

def get_acoes():
    """
    Coleta todas as ações do Fundamentus usando Playwright.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(URL_ACAO)

        # Espera a tabela carregar
        page.wait_for_selector("table#resultado")

        html = page.content()

        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table", {"id": "resultado"})
        thead = table.find("thead")
        tbody = table.find("tbody")

        colunas = [th.get_text(strip=True) for th in thead.find_all("th")]
        if colunas:
            colunas[0] = "Ação"

        dados = []
        for tr in tbody.find_all("tr"):
            cols = [td.get_text(strip=True) for td in tr.find_all("td")]
            if cols:
                dados.append(dict(zip(colunas, cols)))

        browser.close()
        print(f"Quantidade de Ações Encontradas: {len(dados)}")
        return dados
