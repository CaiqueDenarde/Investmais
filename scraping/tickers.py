# tickers.py
import requests
from bs4 import BeautifulSoup
import os

# ======== Headers ========
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

# ======== URLs do Fundamentus ========
URL_ACAO = "https://www.fundamentus.com.br/resultado.php"
URL_FII = "https://www.fundamentus.com.br/fii_resultado.php"

# ======== Função interna para buscar tickers ========
def _get_tickers_from_url(url: str):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.encoding = "ISO-8859-1"
    r.raise_for_status()

    # ======== Salva HTML de debug ========
    filename = "debug_tickers.html"
    with open(filename, "w", encoding="ISO-8859-1") as f:
        f.write(r.text)
    print(f"HTML salvo para debug em {os.path.abspath(filename)}")

    soup = BeautifulSoup(r.text, "html.parser")
    tickers = []

    # Cada linha da tabela representa um ativo
    table = soup.find("table")
    if not table:
        print("⚠️ Nenhuma tabela encontrada na página.")
        return []

    tbody = table.find("tbody")
    if not tbody:
        print("⚠️ Nenhum tbody encontrado na tabela.")
        return []

    for row in tbody.find_all("tr"):
        cols = row.find_all("td")
        if cols:
            ticker = cols[0].get_text(strip=True)
            if ticker:
                tickers.append(ticker)

    return sorted(set(tickers))


# ======== Função pública ========
def get_all_tickers():
    """
    Retorna todos os tickers válidos, separados em AÇÕES e FIIs
    """
    return {
        "ACAO": _get_tickers_from_url(URL_ACAO),
        "FII": _get_tickers_from_url(URL_FII)
    }


# ======== Teste rápido ========
if __name__ == "__main__":
    tickers = get_all_tickers()
    print("ACAO:", tickers["ACAO"][:10], "...")  # mostra os 10 primeiros
    print("FII:", tickers["FII"][:10], "...")
