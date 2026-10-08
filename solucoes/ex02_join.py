"""Solução de referência · Exercício 2."""
import pandas as pd


def receita_por_categoria(itens, pedidos, produtos):
    if produtos["produto_id"].duplicated().any():
        raise ValueError("produto_id repetido em produtos: o JOIN multiplicaria linhas.")
    if pedidos["pedido_id"].duplicated().any():
        raise ValueError("pedido_id repetido em pedidos: o JOIN multiplicaria linhas.")
    base = itens.merge(pedidos[["pedido_id", "status"]], on="pedido_id", how="inner")
    base = base.loc[base["status"].eq("concluido")].merge(produtos[["produto_id", "categoria"]], on="produto_id", how="inner")
    base = base.assign(receita_centavos=base["quantidade"] * base["preco_centavos"])
    return base.groupby("categoria")["receita_centavos"].sum().sort_values(ascending=False).rename("receita_centavos")
