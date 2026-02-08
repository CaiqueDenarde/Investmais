# acoes.py
import os
import requests
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet

HEADERS = {"User-Agent": "Mozilla/5.0"}

# ======== Configuração de criptografia ========
KEY = os.environ.get("ENCRYPTION_KEY")
ENCRYPTED_ACAO = os.environ.get("ENCRYPTED_ACAO")

if not all([KEY, ENCRYPTED_ACAO]):
    raise EnvironmentError(
        "As variáveis de ambiente ENCRYPTION_KEY e ENCRYPTED_ACAO precisam estar definidas."
    )

fernet = Fernet(KEY.encode())

def decrypt_url(encrypted_url: str) -> str:
    """
    Descriptografa a URL usando Fernet.
    """
    return fernet.decrypt(encrypted_url.encode()).decode()


# ======== Função principal ========
def get_acoes():
    """
    Retorna os dados completos das ações do Fundamentus.
    """
    url = decrypt_url(ENCRYPTED_ACAO)
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.encoding = "ISO-8859-1"

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", {"id": "resultado"})  # tabela principal

    # pega os cabeçalhos e renomeia a primeira coluna
    colunas = [th.get_text(strip=True) for th in table.find("thead").find_all("th")]
    if colunas:
        colunas[0] = "Ação"  # renomeia a primeira coluna

    linhas = table.find("tbody").find_all("tr")

    dados = []
    for tr in linhas:
        cols = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cols:
            dados.append(dict(zip(colunas, cols)))

    return dados


# ======== Teste rápido ========
if __name__ == "__main__":
    try:
        acoes = get_acoes()
        print("Exemplo de ações:", acoes[:5])  # mostra os 5 primeiros registros
    except Exception as e:
        print("Erro ao buscar ações:", e)
