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


def test_baseline_semanal_e_dia_da_semana_categorico():
    result, info = comparar(tratar(gerar_vendas()).gold)
    assert list(result.columns) == ["real", "baseline", "baseline_semanal", "baseline_media", "modelo"]
    assert info["mae_baseline_semanal"] == (result.real - result.baseline_semanal).abs().mean()
    assert result.baseline_media.nunique() == 1 and info["mae_baseline_media"] == (result.real - result.baseline_media).abs().mean()
    from lab.ml import montar_modelo, NUMERICAS
    df = preparar_features(tratar(gerar_vendas()).gold)
    model = montar_modelo().fit(df.iloc[:-14][["lag_1", "lag_7", "media_7", "dia_semana"]], df.iloc[:-14]["receita"])
    scaler = model.named_steps["columntransformer"].named_transformers_["num"]
    assert list(scaler.mean_.round(6)) == list(df.iloc[:-14][NUMERICAS].mean().round(6))
    assert model.named_steps["columntransformer"].named_transformers_["dia"].categories_[0].tolist() == list(range(7))
