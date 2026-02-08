import requests
from bs4 import BeautifulSoup

URL = "http://www.fundamentus.com.br/resultado.php"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://www.fundamentus.com.br",
    "Referer": "http://www.fundamentus.com.br/resultado.php",
}

# Payload padrão do formulário (pode ficar vazio)
PAYLOAD = {
    "pl_min": "",
    "pl_max": "",
    "pvp_min": "",
    "pvp_max": "",
    "psr_min": "",
    "psr_max": "",
    "divy_min": "",
    "divy_max": "",
    "pativos_min": "",
    "pativos_max": "",
    "pcapgiro_min": "",
    "pcapgiro_max": "",
    "pebit_min": "",
    "pebit_max": "",
    "fgrah_min": "",
    "fgrah_max": "",
    "firma_ebit_min": "",
    "firma_ebit_max": "",
    "margemebit_min": "",
    "margemebit_max": "",
    "margemliq_min": "",
    "margemliq_max": "",
    "liqcorr_min": "",
    "liqcorr_max": "",
    "roic_min": "",
    "roic_max": "",
    "roe_min": "",
    "roe_max": "",
    "liq_min": "",
    "liq_max": "",
    "patrim_min": "",
    "patrim_max": "",
    "divbruta_min": "",
    "divbruta_max": "",
    "tx_cresc_rec_min": "",
    "tx_cresc_rec_max": "",
    "setor": "0",
    "negociada": "ON",
    "ordem": "1",
    "x": "28",
    "y": "16",
}

def get_acoes():
    session = requests.Session()
    session.headers.update(HEADERS)

    resp = session.post(URL, data=PAYLOAD, timeout=60)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table")

    if not table:
        raise Exception("Tabela de ações não encontrada")

    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    headers[0] = "Ação"

    dados = []
    for row in table.find("tbody").find_all("tr"):
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if len(cols) == len(headers):
            dados.append(dict(zip(headers, cols)))

    return dados
