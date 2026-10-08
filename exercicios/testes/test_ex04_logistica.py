import numpy as np
import pytest
from sklearn.linear_model import LogisticRegression
from ex04_logistica import prever_proba, sigmoide, treinar_logistica


def dados():
    rng = np.random.default_rng(3)
    X = rng.normal(size=(400, 3))
    z = 1.5 * X[:, 0] - 2.0 * X[:, 1] + 0.3 * X[:, 2] + 0.4
    y = rng.binomial(1, 1 / (1 + np.exp(-z)))
    return (X - X.mean(0)) / X.std(0), y


def test_sigmoide_estavel_e_correta():
    assert sigmoide(np.array([0.0]))[0] == pytest.approx(0.5)
    extremos = sigmoide(np.array([-1000.0, 1000.0]))
    assert np.isfinite(extremos).all() and extremos[0] == pytest.approx(0, abs=1e-12) and extremos[1] == pytest.approx(1)


def test_probabilidades_ficam_entre_zero_e_um():
    X, y = dados()
    w, b = treinar_logistica(X, y)
    p = prever_proba(X, w, b)
    assert p.shape == (400,) and ((p >= 0) & (p <= 1)).all()


def test_perda_diminui_em_relacao_ao_inicio():
    X, y = dados()
    w, b = treinar_logistica(X, y)

    def logloss(p):
        p = np.clip(p, 1e-12, 1 - 1e-12)
        return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
    assert logloss(prever_proba(X, w, b)) < logloss(np.full(len(y), .5)) - 0.05


def test_aproxima_a_logistica_do_sklearn_sem_regularizacao():
    X, y = dados()
    w, b = treinar_logistica(X, y, taxa=0.5, passos=5000)
    ref = LogisticRegression(C=1e8, max_iter=5000).fit(X, y)
    diferenca = np.abs(prever_proba(X, w, b) - ref.predict_proba(X)[:, 1]).max()
    assert diferenca < 0.03, f"Diferença máxima de probabilidade {diferenca:.3f}; revise o sinal do gradiente e o intercepto."


def test_l2_encolhe_os_pesos():
    X, y = dados()
    sem, _ = treinar_logistica(X, y, l2=0.0)
    com, _ = treinar_logistica(X, y, l2=0.5)
    assert np.linalg.norm(com) < np.linalg.norm(sem)
