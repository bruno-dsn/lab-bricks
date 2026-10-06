import pytest
from lab.dados import COLUNAS, gerar_vendas
from lab.pipeline import tratar, indicadores


def pedido(**changes):
    return {"venda_id": "P1", "data_venda": "2026-01-01", "produto": "Caderno",
            "categoria": "Papelaria", "canal": "Site", "quantidade": "2",
            "preco_unitario": "10.25", "status": "concluida",
            "atualizado_em": "2026-01-01 10:00:00", **changes}


def test_contagens_e_reconciliacao_da_fonte():
    result = tratar(gerar_vendas())
    assert (len(result.bronze), len(result.silver), len(result.rejeitadas), len(result.substituidas)) == (727, 720, 6, 1)
    assert result.silver.venda_id.is_unique
    expected = result.silver.loc[result.silver.status.eq("concluida"), "valor_centavos"].sum()
    assert result.gold.receita_centavos.sum() == expected


def test_receita_e_ticket_excluem_cancelamentos():
    result = tratar([pedido(), pedido(venda_id="P2", quantidade="1", preco_unitario="3.10"),
                     pedido(venda_id="P3", status="cancelada", preco_unitario="999.99")])
    metrics = indicadores(result.silver)
    assert metrics == {"pedidos": 2, "receita": 23.6, "ticket_medio": 11.8}


def test_deduplicacao_independe_da_ordem_de_chegada():
    newer = pedido(quantidade="4", atualizado_em="2026-01-02 10:00:00")
    result = tratar([newer, pedido()])
    assert len(result.substituidas) == 1
    assert result.silver.iloc[0].valor_centavos == 4100


def test_versao_recente_invalida_nao_ressuscita_a_antiga():
    result = tratar([pedido(), pedido(quantidade="0", atualizado_em="2026-01-02 10:00:00")])
    assert result.silver.empty
    assert len(result.rejeitadas) == len(result.substituidas) == 1
    assert indicadores(result.silver)["receita"] == 0


@pytest.mark.parametrize("changes", [
    {"quantidade": "1.5"}, {"quantidade": "-1"}, {"quantidade": "1001"},
    {"preco_unitario": "NaN"}, {"preco_unitario": "10.999"}, {"preco_unitario": "0"},
    {"data_venda": "2026-02-30"}, {"produto": " "}, {"status": "pago"},
    {"atualizado_em": "invalido"}, {"venda_id": ""},
])
def test_contrato_rejeita_dados_invalidos(changes):
    result = tratar([pedido(**changes)])
    assert result.silver.empty
    assert len(result.rejeitadas) == 1


def test_gerador_e_reproduzivel():
    assert gerar_vendas() == gerar_vendas()
    assert gerar_vendas(seed=42) != gerar_vendas(seed=43)


@pytest.mark.parametrize("kwargs", [{"n": 2}, {"n": 2001}, {"seed": -1}, {"sujeira": "sim"}])
def test_limites_de_geracao(kwargs):
    with pytest.raises(ValueError):
        gerar_vendas(**kwargs)


@pytest.mark.parametrize("campo", COLUNAS)
def test_campo_nulo_vai_para_quarentena_sem_perder_a_bronze(campo):
    result = tratar([pedido(**{campo: None})])
    assert result.bronze.iloc[0][campo] is None
    assert result.silver.empty
    assert len(result.rejeitadas) == 1
    assert result.rejeitadas.iloc[0][campo] == ""


@pytest.mark.parametrize("rows", [None, [None], ["pedido"], [{"venda_id": "P1"}], [pedido(quantidade=2)]])
def test_formato_da_fonte_tem_erro_controlado(rows):
    with pytest.raises(ValueError):
        tratar(rows)
