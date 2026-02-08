# tickers.py
from acoes import get_acoes
from fiis import get_fiis

def get_all_tickers():
    """
    Retorna todos os tickers válidos, separados em AÇÕES e FIIs.
    """
    acoes = get_acoes()
    fiis = get_fiis()

    tickers_acao = sorted({item["Papel"] for item in acoes})
    tickers_fii = sorted({item["Papel"] for item in fiis})

    return {
        "ACAO": tickers_acao,
        "FII": tickers_fii
    }
