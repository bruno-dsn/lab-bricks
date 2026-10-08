"""Exercício 4 · Regressão logística com gradiente descendente (só NumPy).

Ideia: p = sigmoid(X @ w + b). Minimize a perda log-loss
  L = -mean( y*log(p) + (1-y)*log(1-p) ) + 0.5 * l2 * sum(w**2)
O gradiente em w é  X.T @ (p - y) / n + l2 * w   e em b é  mean(p - y).
Assuma que X já está padronizado.
"""
import numpy as np


def sigmoide(z):
    """Sigmoide estável: não pode gerar overflow para z muito grande ou muito pequeno."""
    raise NotImplementedError


def prever_proba(X, w, b):
    raise NotImplementedError


def treinar_logistica(X, y, taxa=0.5, passos=3000, l2=0.0):
    """Devolve (w, b) depois de `passos` atualizações de gradiente descendente, começando em zero."""
    raise NotImplementedError
