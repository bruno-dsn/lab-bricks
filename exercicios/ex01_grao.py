"""Exercício 1 · Grão: pedido, item e unidade são coisas diferentes.

`itens` tem uma linha por item, com as colunas:
pedido_id, item_id, quantidade, valor_centavos  (valor TOTAL da linha, já multiplicado pela quantidade).
"""
import pandas as pd


def contar_grao(itens: pd.DataFrame) -> dict:
    """Devolve {"pedidos": ..., "itens": ..., "unidades": ...} com inteiros do Python.

    pedidos  = pedidos distintos
    itens    = linhas de item distintas (item_id)
    unidades = soma de quantidade
    """
    raise NotImplementedError("Conte pedidos distintos, itens distintos e some as unidades.")


def ticket_medio(itens: pd.DataFrame) -> float:
    """Receita total em REAIS dividida pelos PEDIDOS distintos (não pelas linhas).

    Se `itens` estiver vazio, devolva 0.0.
    """
    raise NotImplementedError("Some valor_centavos, converta para reais e divida por pedidos distintos.")
