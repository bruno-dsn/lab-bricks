import numpy as np
import pytest
from lab.estabilidade import intervalo_bootstrap, limiar_teorico, repetir_selecao, resumir


def test_limiar_teorico_do_caso_de_entregas():
    assert limiar_teorico() == pytest.approx(5 / 35)
    assert limiar_teorico(1, 1) == .5
    for fp, fn in [(0, 1), (-1, 3), (True, 2)]:
        with pytest.raises(ValueError):
            limiar_teorico(fp, fn)


def test_repeticao_e_deterministica_e_coerente():
    a, b = repetir_selecao(6), repetir_selecao(6)
    assert a.equals(b) and len(a) == 6
    assert a.modelo.isin(["baseline", "logistica_C_0.1", "logistica_C_1"]).all()
    assert (a.margem_validacao >= 0).all() and a.limiar.between(.1, .9).all()
    resumo = resumir(a)
    assert sum(resumo["escolhas"].values()) == 6
    assert resumo["limiar_min"] <= resumo["limiar_mediana"] <= resumo["limiar_max"]
    assert resumo["limiar_teorico"] == pytest.approx(1 / 7)


def test_selecao_vence_nunca_alertar_com_folga_e_escolha_exata_oscila():
    frame = repetir_selecao(20)
    resumo = resumir(frame)
    assert resumo["ganho_ic95"][0] > 0, "O modelo deveria ganhar de 'nunca alertar' com folga neste cenário."
    # O ponto da aula: os dois candidatos logísticos quase empatam, então o vencedor oscila entre amostras.
    assert len([m for m, n in resumo["escolhas"].items() if n >= 3]) >= 2
    assert abs(resumo["limiar_mediana"] - 1 / 7) < .08


def test_bootstrap_cobre_a_media_e_valida_entradas():
    values = np.arange(100.)
    low, high = intervalo_bootstrap(values)
    assert low < values.mean() < high
    assert intervalo_bootstrap(values, seed=1) == intervalo_bootstrap(values, seed=1)
    for bad in ([1.0], [1.0, np.nan], [[1, 2], [3, 4]]):
        with pytest.raises(ValueError):
            intervalo_bootstrap(bad)
    with pytest.raises(ValueError):
        intervalo_bootstrap(values, repeticoes=10)


@pytest.mark.parametrize("amostras", [4, 61, 10.0, True])
def test_repeticao_rejeita_quantidade_invalida(amostras):
    with pytest.raises(ValueError):
        repetir_selecao(amostras)
