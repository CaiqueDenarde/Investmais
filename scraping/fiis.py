import requests
from bs4 import BeautifulSoup

URL = "http://www.fundamentus.com.br/fii_resultado.php"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://www.fundamentus.com.br",
    "Referer": "http://www.fundamentus.com.br/fii_resultado.php",
}

def get_fiis():
    session = requests.Session()
    session.headers.update(HEADERS)

    resp = session.post(URL, timeout=60)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table")

    if not table:
        raise Exception("Tabela de FIIs não encontrada")

    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    headers[0] = "Fii"

    dados = []
    for row in table.find("tbody").find_all("tr"):
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if len(cols) == len(headers):
            dados.append(dict(zip(headers, cols)))

    return dados
