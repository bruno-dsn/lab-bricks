import pandas as pd
from lab.dados import gerar_vendas
from lab.pipeline import tratar
from lab.ml import preparar_features, comparar


def test_features_do_passado_nao_mudam_com_alteracoes_no_futuro():
    gold = tratar(gerar_vendas()).gold
    original = preparar_features(gold)
    alterado = gold.copy()
    alterado.loc[alterado.data_venda >= "2026-03-01", "receita"] *= 100
    novo = preparar_features(alterado)
    pd.testing.assert_frame_equal(original.loc[:"2026-02-28"], novo.loc[:"2026-02-28"])
    # A receita de 1º de março é o alvo, e não uma feature desse dia.
    for col in ["lag_1", "lag_7", "media_7", "dia_semana"]:
        assert original.loc["2026-03-01", col] == novo.loc["2026-03-01", col]


def test_teste_temporal_e_mae_calculado():
    result, info = comparar(tratar(gerar_vendas()).gold)
    assert len(result) == 14
    assert info["treino_fim"] < info["teste_inicio"]
    assert info["mae_baseline"] == (result.real - result.baseline).abs().mean()
    assert info["mae_modelo"] >= 0
