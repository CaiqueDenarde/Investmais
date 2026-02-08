# tickers.py
import os
import requests
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet

HEADERS = {"User-Agent": "Mozilla/5.0"}

# ======== Configuração de criptografia ========
KEY = os.environ.get("ENCRYPTION_KEY")
ENCRYPTED_ACAO = os.environ.get("ENCRYPTED_ACAO")
ENCRYPTED_FII = os.environ.get("ENCRYPTED_FII")

if not all([KEY, ENCRYPTED_ACAO, ENCRYPTED_FII]):
    raise EnvironmentError(
        "Variáveis de ambiente ENCRYPTION_KEY, ENCRYPTED_ACAO e ENCRYPTED_FII não estão definidas."
    )

fernet = Fernet(KEY.encode())

def decrypt_url(encrypted_url: str) -> str:
    """
    Descriptografa a URL usando Fernet.
    """
    return fernet.decrypt(encrypted_url.encode()).decode()

# ======== Função para buscar tickers ========
def _get_tickers_from_url(encrypted_url: str):
    url = decrypt_url(encrypted_url)
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    tickers = []

    for row in soup.select("table tbody tr"):
        cols = row.find_all("td")
        if cols:
            ticker = cols[0].get_text(strip=True)
            if ticker:
                tickers.append(ticker)

    return sorted(set(tickers))

# ======== Função pública ========
def get_all_tickers():
    """
    Retorna todos os tickers válidos,
    separados em AÇÕES e FIIs
    """
    return {
        "ACAO": _get_tickers_from_url(ENCRYPTED_ACAO),
        "FII": _get_tickers_from_url(ENCRYPTED_FII)
    }

# ======== Teste rápido ========
if __name__ == "__main__":
    tickers = get_all_tickers()
    print("ACAO:", tickers["ACAO"][:10], "...")  # mostra os 10 primeiros
    print("FII:", tickers["FII"][:10], "...")
