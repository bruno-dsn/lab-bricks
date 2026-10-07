import numpy as np
import pandas as pd
import pytest

from lab.classificacao import gerar_entregas, FEATURES
from lab.ciclo_ml import COLUNAS_ENTRADA, juntar_no_instante, validar_entrada, dividir_por_datas, avaliar_ciclo


def casos_temporais():
    pedidos = pd.DataFrame({"pedido_id": ["P2", "P1", "P3"], "cliente_id": ["A", "A", "B"],
                            "previsto_em": ["2026-01-10T13:00:00Z", "2026-01-10T10:00:00Z", "2026-01-10T10:00:00Z"]})
    historico = pd.DataFrame({"cliente_id": ["A", "A"],
                              "disponivel_em": ["2026-01-09T09:00:00Z", "2026-01-10T12:00:00Z"],
                              "risco_historico": [.2, .8]})
    return pedidos, historico


def test_lookup_preserva_ordem_ausencia_e_nao_traz_futuro():
    pedidos, historico = casos_temporais()
    result = juntar_no_instante(pedidos, historico)
    assert result.pedido_id.tolist() == ["P2", "P1", "P3"]
    assert result.risco_historico.iloc[:2].tolist() == [.8, .2]
    assert pd.isna(result.risco_historico.iloc[2])
    known = result.dropna(subset="disponivel_em")
    assert (known.disponivel_em <= known.previsto_em).all()
    historico.loc[1, "disponivel_em"] = "2026-01-10T14:00:00Z"
    assert juntar_no_instante(pedidos, historico).risco_historico.iloc[0] == .2


def test_lookup_igualdade_de_instante_e_versao_ambigua():
    pedidos, historico = casos_temporais()
    historico.loc[1, "disponivel_em"] = "2026-01-10T10:00:00Z"
    assert juntar_no_instante(pedidos, historico).risco_historico.iloc[1] == .8
    with pytest.raises(ValueError, match="ambíguas"):
        juntar_no_instante(pedidos, pd.concat([historico, historico.iloc[[0]]]))


@pytest.mark.parametrize("erro", ["ausente", "extra", "negativa", "texto", "nan", "inf", "volumes_fracionados", "booleana", "coluna_duplicada"])
def test_contrato_rejeita_entradas_incompativeis(erro):
    frame = gerar_entregas().loc[:2, FEATURES].copy()
    if erro == "ausente": frame = frame.drop(columns="previsao_chuva")
    elif erro == "extra": frame["duracao_real_min"] = 50
    elif erro == "negativa": frame.loc[0, "distancia_km"] = -1
    elif erro == "texto": frame["distancia_km"] = "20"
    elif erro == "nan": frame.loc[0, "distancia_km"] = np.nan
    elif erro == "inf": frame.loc[0, "distancia_km"] = np.inf
    elif erro == "volumes_fracionados": frame = frame.astype(float); frame.loc[0, "volumes"] = 1.5
    elif erro == "booleana": frame["hora_pico"] = True
    elif erro == "coluna_duplicada": frame = pd.concat([frame, frame[["volumes"]]], axis=1)
    with pytest.raises(ValueError): validar_entrada(frame)


def test_contrato_normaliza_ordem_e_corte_nao_divide_datas():
    frame = gerar_entregas()
    assert FEATURES == COLUNAS_ENTRADA
    assert list(validar_entrada(frame[FEATURES[::-1]])) == FEATURES
    train, validation, test = dividir_por_datas(frame)
    assert [len(x) for x in [train, validation, test]] == [360, 120, 120]
    assert train.data.max() < validation.data.min() <= validation.data.max() < test.data.min()


def test_selecao_nao_usa_rotulos_do_teste_e_pipeline_nao_aprende_validacao():
    frame = gerar_entregas()
    model, board, selected, scored = avaliar_ciclo(frame)
    changed = frame.copy()
    _, _, holdout = dividir_por_datas(frame)
    changed.loc[holdout.index, "atrasou"] = 1 - changed.loc[holdout.index, "atrasou"]
    _, new_board, new_selected, _ = avaliar_ciclo(changed)
    pd.testing.assert_frame_equal(board, new_board)
    assert (selected["modelo"], selected["limiar"]) == (new_selected["modelo"], new_selected["limiar"])
    assert len(board) == 51 and len(scored) == 120
    assert selected["tp"] + selected["tn"] + selected["fp"] + selected["fn"] == 120
    if hasattr(model, "named_steps"):
        train, _, _ = dividir_por_datas(frame)
        np.testing.assert_allclose(model.named_steps["standardscaler"].mean_, train[FEATURES].mean())
