# fiis.py
import requests
from bs4 import BeautifulSoup
import time
import os

# ======== Headers completos ========
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

# ======== URL do Fundamentus para FIIs ========
URL_FIIS = "https://www.fundamentus.com.br/fii_resultado.php"

# ======== Função para obter FIIs com retry e debug ========
def get_fiis(retries=3, delay=5):
    last_exception = None

    for attempt in range(retries):
        try:
            print(f"Buscando FIIs... tentativa {attempt+1}")
            r = requests.get(URL_FIIS, headers=HEADERS, timeout=20)
            r.encoding = "ISO-8859-1"

            # ======== Salva HTML para debug ========
            debug_file = os.path.join(os.path.dirname(__file__), "debug_fiis.html")
            with open(debug_file, "w", encoding="ISO-8859-1") as f:
                f.write(r.text)
            print(f"HTML salvo em {debug_file}")

            soup = BeautifulSoup(r.text, "html.parser")
            table = soup.find("table")
            
            if table is None:
                print("⚠️ Aviso: Nenhuma tabela encontrada no HTML recebido.")
                return []  # Retorna lista vazia

            thead = table.find("thead")
            tbody = table.find("tbody")
            if thead is None or tbody is None:
                print("⚠️ Aviso: Estrutura da tabela incompleta (thead/tbody).")
                return []

            colunas = [th.get_text(strip=True) for th in thead.find_all("th")]
            if colunas:
                colunas[0] = "Fii"

            dados = []
            for tr in tbody.find_all("tr"):
                cols = [td.get_text(strip=True) for td in tr.find_all("td")]
                if cols:
                    dados.append(dict(zip(colunas, cols)))

            print(f"Quantidade de FIIs Encontrados: {len(dados)}")
            return dados

        except Exception as e:
            print(f"Tentativa {attempt+1}/{retries} falhou: {e}")
            last_exception = e
            time.sleep(delay)

    print("❌ Falha ao buscar FIIs após várias tentativas.")
    raise last_exception


# ======== Teste rápido ========
if __name__ == "__main__":
    try:
        fiis = get_fiis()
        if fiis:
            print("Exemplo de FIIs:", fiis[:5])
        else:
            print("Nenhum dado de FIIs foi retornado. Verifique debug_fiis.html")
    except Exception as e:
        print("Erro crítico ao buscar FIIs:", e)
