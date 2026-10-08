import pandas as pd
import pytest
from ex02_join import receita_por_categoria

ITENS = pd.DataFrame({
    "pedido_id": ["P1", "P1", "P2", "P3"], "item_id": ["I1", "I2", "I3", "I4"],
    "produto_id": ["A", "B", "A", "B"], "quantidade": [2, 1, 3, 5], "preco_centavos": [1000, 500, 1000, 500]})
PEDIDOS = pd.DataFrame({"pedido_id": ["P1", "P2", "P3"], "status": ["concluido", "cancelado", "concluido"]})
PRODUTOS = pd.DataFrame({"produto_id": ["A", "B"], "categoria": ["Casa", "Jardim"]})


def test_receita_so_de_concluidos_ordenada():
    r = receita_por_categoria(ITENS, PEDIDOS, PRODUTOS)
    # Casa: P1 2*1000 = 2000 (P2 cancelado fica fora). Jardim: P1 500 + P3 2500 = 3000.
    assert r.to_dict() == {"Jardim": 3000, "Casa": 2000}
    assert list(r.index) == ["Jardim", "Casa"] and r.name == "receita_centavos"


def test_dimensao_duplicada_nao_multiplica_em_silencio():
    duplicado = pd.concat([PRODUTOS, PRODUTOS.iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError):
        receita_por_categoria(ITENS, PEDIDOS, duplicado)


def test_pedido_duplicado_levanta_erro():
    duplicado = pd.concat([PEDIDOS, PEDIDOS.iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError):
        receita_por_categoria(ITENS, duplicado, PRODUTOS)
