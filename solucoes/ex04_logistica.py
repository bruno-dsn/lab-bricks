"""Solução de referência · Exercício 4."""
import numpy as np


def sigmoide(z):
    z = np.asarray(z, dtype=float)
    out = np.empty_like(z)
    pos = z >= 0
    out[pos] = 1 / (1 + np.exp(-z[pos]))
    e = np.exp(z[~pos])
    out[~pos] = e / (1 + e)
    return out


def prever_proba(X, w, b):
    return sigmoide(np.asarray(X, dtype=float) @ w + b)


def treinar_logistica(X, y, taxa=0.5, passos=3000, l2=0.0):
    X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
    n, d = X.shape
    w, b = np.zeros(d), 0.0
    for _ in range(passos):
        erro = prever_proba(X, w, b) - y
        w -= taxa * (X.T @ erro / n + l2 * w)
        b -= taxa * erro.mean()
    return w, b
