"""Exercício 2 · JOIN que não multiplica a receita.

itens:    pedido_id, item_id, produto_id, quantidade, preco_centavos
pedidos:  pedido_id, status            ("concluido" ou "cancelado")
produtos: produto_id, categoria
"""
import pandas as pd


def receita_por_categoria(itens: pd.DataFrame, pedidos: pd.DataFrame, produtos: pd.DataFrame) -> pd.Series:
    """Receita em centavos por categoria, só de pedidos concluídos.

    receita da linha = quantidade * preco_centavos
    Regras:
      * Se `produtos` tiver produto_id repetido, levante ValueError (o JOIN multiplicaria linhas).
      * Se `pedidos` tiver pedido_id repetido, levante ValueError pelo mesmo motivo.
      * Devolva uma Series indexada por categoria, de nome "receita_centavos", ordenada do maior para o menor.
    """
    raise NotImplementedError("Valide as chaves das dimensões, faça os merges e agregue.")
