import pytest
from ex07_recuperacao import mrr, recall_em_k

RANK = [["a", "b", "c"], ["x", "a", "y"], ["p", "q", "r"], ["m", "n", "o"]]
ESPERADO = ["a", "a", "z", "o"]


def test_recall_em_k():
    assert recall_em_k(RANK, ESPERADO, 1) == pytest.approx(1 / 4)
    assert recall_em_k(RANK, ESPERADO, 2) == pytest.approx(2 / 4)
    assert recall_em_k(RANK, ESPERADO, 3) == pytest.approx(3 / 4)


def test_mrr_usa_posicao_do_primeiro_acerto():
    assert mrr(RANK, ESPERADO, 3) == pytest.approx((1 + 1 / 2 + 0 + 1 / 3) / 4)


def test_mrr_respeita_o_corte_k():
    assert mrr(RANK, ESPERADO, 1) == pytest.approx(1 / 4)
