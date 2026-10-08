import pandas as pd
import pytest
from ex01_grao import contar_grao, ticket_medio

ITENS = pd.DataFrame({
    "pedido_id": ["P1", "P1", "P1", "P2"], "item_id": ["I1", "I2", "I3", "I4"],
    "quantidade": [2, 2, 2, 1], "valor_centavos": [2000, 3000, 1000, 5000]})


def test_pedido_com_tres_itens_de_duas_unidades():
    um = ITENS.iloc[:3]
    assert contar_grao(um) == {"pedidos": 1, "itens": 3, "unidades": 6}


def test_contagem_completa_e_tipos_inteiros():
    resultado = contar_grao(ITENS)
    assert resultado == {"pedidos": 2, "itens": 4, "unidades": 7}
    assert all(type(v) is int for v in resultado.values()), "Devolva int do Python, não tipos do NumPy."


def test_ticket_divide_por_pedidos_e_nao_por_linhas():
    # receita 110,00 / 2 pedidos = 55,00. Dividir por 4 linhas daria 27,50.
    assert ticket_medio(ITENS) == pytest.approx(55.0)


def test_ticket_de_tabela_vazia():
    assert ticket_medio(ITENS.iloc[0:0]) == 0.0
