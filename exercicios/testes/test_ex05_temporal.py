import pandas as pd
import pytest
from ex05_temporal import criar_lag, dividir_por_datas, media_movel_passada


def quadro(dias=60, por_dia=2):
    datas = pd.date_range("2026-01-01", periods=dias).repeat(por_dia)
    return pd.DataFrame({"data": datas, "x": range(len(datas))})


def test_tamanhos_60_20_20_por_datas():
    treino, validacao, teste = dividir_por_datas(quadro())
    assert [len(treino), len(validacao), len(teste)] == [72, 24, 24]


def test_nenhuma_data_em_duas_partes_e_ordem_temporal():
    treino, validacao, teste = dividir_por_datas(quadro())
    assert treino.data.max() < validacao.data.min() <= validacao.data.max() < teste.data.min()
    assert len(set(treino.data) & set(validacao.data)) == 0


def test_poucas_datas_levantam_erro():
    with pytest.raises(ValueError):
        dividir_por_datas(quadro(dias=9))


def test_lag_usa_so_o_passado():
    s = pd.Series([10, 20, 30, 40.0])
    assert criar_lag(s, 1).tolist()[1:] == [10, 20, 30] and pd.isna(criar_lag(s, 1).iloc[0])


@pytest.mark.parametrize("k", [0, -1, 1.5, True])
def test_lag_invalido_e_vazamento(k):
    with pytest.raises(ValueError):
        criar_lag(pd.Series([1.0, 2.0, 3.0]), k)


def test_media_movel_nao_inclui_o_dia_atual():
    s = pd.Series([1.0, 2.0, 3.0, 4.0, 100.0])
    m = media_movel_passada(s, 2)
    assert m.iloc[2] == pytest.approx(1.5) and m.iloc[4] == pytest.approx(3.5)


def test_mudar_o_futuro_nao_muda_as_features_do_passado():
    s = pd.Series(range(30), dtype=float)
    alterado = s.copy()
    alterado.iloc[20:] *= 100
    pd.testing.assert_series_equal(criar_lag(s, 3).iloc[:20], criar_lag(alterado, 3).iloc[:20])
    pd.testing.assert_series_equal(media_movel_passada(s, 5).iloc[:21], media_movel_passada(alterado, 5).iloc[:21])
