# fiis.py
import os
import requests
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet
import time

# ======== Headers mais completos ========
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

# ======== Variáveis de ambiente ========
KEY = os.environ.get("ENCRYPTION_KEY")
ENCRYPTED_FII = os.environ.get("ENCRYPTED_FII")

if not all([KEY, ENCRYPTED_FII]):
    raise EnvironmentError(
        "As variáveis de ambiente ENCRYPTION_KEY e ENCRYPTED_FII precisam estar definidas."
    )

fernet = Fernet(KEY.encode())

# ======== Função para descriptografar URL ========
def decrypt_url(encrypted_url: str) -> str:
    return fernet.decrypt(encrypted_url.encode()).decode()


# ======== Função para obter FIIs com retry ========
def get_fiis(retries=3, delay=5):
    url = decrypt_url(ENCRYPTED_FII)
    last_exception = None

    for attempt in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            r.encoding = "ISO-8859-1"

            # ======== Debug: salva HTML recebido ========
            with open("debug_fiis.html", "w", encoding="ISO-8859-1") as f:
                f.write(r.text)

            soup = BeautifulSoup(r.text, "html.parser")
            table = soup.find("table")
            if table is None:
                raise Exception("Não encontrei nenhuma tabela na página de FIIs")

            thead = table.find("thead")
            if thead is None:
                raise Exception("Não encontrei o thead na tabela de FIIs")

            colunas = [th.get_text(strip=True) for th in thead.find_all("th")]
            if colunas:
                colunas[0] = "Fii"

            tbody = table.find("tbody")
            if tbody is None:
                raise Exception("Não encontrei tbody na tabela de FIIs")

            dados = []
            for tr in tbody.find_all("tr"):
                cols = [td.get_text(strip=True) for td in tr.find_all("td")]
                if cols:
                    dados.append(dict(zip(colunas, cols)))

            return dados

        except Exception as e:
            print(f"Tentativa {attempt+1}/{retries} falhou: {e}")
            last_exception = e
            time.sleep(delay)

    raise last_exception
