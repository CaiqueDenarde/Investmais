# fiis.py
import os
import requests
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet

HEADERS = {"User-Agent": "Mozilla/5.0"}

# ======== Configuração de criptografia ========
KEY = os.environ.get("ENCRYPTION_KEY")
ENCRYPTED_FII = os.environ.get("ENCRYPTED_FII")

if not all([KEY, ENCRYPTED_FII]):
    raise EnvironmentError(
        "As variáveis de ambiente ENCRYPTION_KEY e ENCRYPTED_FII precisam estar definidas."
    )

fernet = Fernet(KEY.encode())

def decrypt_url(encrypted_url: str) -> str:
    """
    Descriptografa a URL usando Fernet.
    """
    return fernet.decrypt(encrypted_url.encode()).decode()


# ======== Função principal ========
def get_fiis():
    """
    Retorna os dados completos dos FIIs do Fundamentus.
    """
    url = decrypt_url(ENCRYPTED_FII)
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.encoding = "ISO-8859-1"

    soup = BeautifulSoup(r.text, "html.parser")

    # pega a primeira tabela do body
    table = soup.find("table")
    if not table:
        raise Exception("Não encontrei nenhuma tabela na página de FIIs")

    # cabeçalhos
    thead = table.find("thead")
    if not thead:
        raise Exception("Não encontrei o thead na tabela de FIIs")

    colunas = [th.get_text(strip=True) for th in thead.find_all("th")]

    # renomeia a primeira coluna para 'Fii'
    if colunas:
        colunas[0] = "Fii"

    # linhas
    tbody = table.find("tbody")
    if not tbody:
        raise Exception("Não encontrei tbody na tabela de FIIs")

    dados = []
    for tr in tbody.find_all("tr"):
        cols = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cols:
            dados.append(dict(zip(colunas, cols)))

    return dados


# ======== Teste rápido ========
if __name__ == "__main__":
    try:
        fiis = get_fiis()
        print("Exemplo de FIIs:", fiis[:5])  # mostra os 5 primeiros registros
    except Exception as e:
        print("Erro ao buscar FIIs:", e)
