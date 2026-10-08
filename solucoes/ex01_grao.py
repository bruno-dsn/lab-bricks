"""Solução de referência · Exercício 1."""
import pandas as pd


def contar_grao(itens: pd.DataFrame) -> dict:
    return {"pedidos": int(itens["pedido_id"].nunique()), "itens": int(itens["item_id"].nunique()),
            "unidades": int(itens["quantidade"].sum())}


def ticket_medio(itens: pd.DataFrame) -> float:
    pedidos = itens["pedido_id"].nunique()
    if pedidos == 0:
        return 0.0
    return float(itens["valor_centavos"].sum()) / 100 / pedidos
