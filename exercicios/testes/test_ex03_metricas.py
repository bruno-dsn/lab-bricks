import numpy as np
import pytest
from sklearn.metrics import brier_score_loss, confusion_matrix, f1_score, precision_score, recall_score
from ex03_metricas import brier, custo, matriz, precision_recall_f1

RNG = np.random.default_rng(7)
Y = RNG.integers(0, 2, 200)
P = np.clip(Y * .35 + RNG.uniform(0, .65, 200), 0, 1)
PRED = (P >= .5).astype(int)


def test_matriz_confere_com_sklearn():
    esperado = tuple(int(v) for v in confusion_matrix(Y, PRED, labels=[0, 1]).ravel())
    assert matriz(Y, PRED) == esperado
    assert all(type(v) is int for v in matriz(Y, PRED))


def test_precision_recall_f1_conferem_com_sklearn():
    p, r, f = precision_recall_f1(Y, PRED)
    assert p == pytest.approx(precision_score(Y, PRED))
    assert r == pytest.approx(recall_score(Y, PRED))
    assert f == pytest.approx(f1_score(Y, PRED))


def test_denominador_zero_vira_zero():
    assert precision_recall_f1([0, 0, 1], [0, 0, 0]) == (0.0, 0.0, 0.0)


def test_brier_confere_com_sklearn():
    assert brier(Y, P) == pytest.approx(brier_score_loss(Y, P))


def test_custo_padrao_e_personalizado():
    assert custo(fp=3, fn=2) == 3 * 5 + 2 * 30
    assert custo(fp=3, fn=2, custo_fp=1, custo_fn=10) == 23
