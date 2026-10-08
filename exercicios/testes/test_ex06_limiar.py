import numpy as np
import pytest
from ex06_limiar import limiar_empirico, limiar_teorico


def test_limiar_teorico():
    assert limiar_teorico(5, 30) == pytest.approx(1 / 7)
    assert limiar_teorico(1, 1) == pytest.approx(0.5)


@pytest.mark.parametrize("fp,fn", [(0, 1), (1, 0), (-1, 5)])
def test_limiar_teorico_rejeita_custos_invalidos(fp, fn):
    with pytest.raises(ValueError):
        limiar_teorico(fp, fn)


def test_empirico_com_probabilidades_calibradas_chega_perto_do_teorico():
    rng = np.random.default_rng(11)
    p = rng.uniform(0, 1, 40_000)
    y = rng.binomial(1, p)
    limiar, custo = limiar_empirico(y, p)
    assert abs(limiar - 5 / 35) < 0.05, f"Esperava algo perto de {5/35:.3f}, obtive {limiar:.2f}."
    assert custo > 0


def test_empate_escolhe_o_menor_limiar():
    y, p = np.array([0, 0, 0]), np.array([0.2, 0.2, 0.2])
    limiar, custo = limiar_empirico(y, p, grade=[0.1, 0.5, 0.9])
    assert (limiar, custo) == (0.5, 0)  # 0.1 gera 3 falsos positivos; 0.5 e 0.9 empatam em 0, vence o menor


def test_custo_confere_com_contagem_manual():
    y, p = np.array([1, 1, 0, 0]), np.array([0.9, 0.2, 0.8, 0.1])
    assert limiar_empirico(y, p, grade=[0.5]) == (0.5, 1 * 5 + 1 * 30)
