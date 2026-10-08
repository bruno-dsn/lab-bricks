"""Solução de referência · Exercício 6."""
import numpy as np


def limiar_teorico(custo_fp, custo_fn):
    if custo_fp <= 0 or custo_fn <= 0:
        raise ValueError("Custos precisam ser positivos.")
    return custo_fp / (custo_fp + custo_fn)


def limiar_empirico(y, p, custo_fp=5, custo_fn=30, grade=None):
    y, p = np.asarray(y).astype(int), np.asarray(p, dtype=float)
    grade = np.round(np.arange(0.05, 0.951, 0.01), 2) if grade is None else np.asarray(grade, dtype=float)
    melhor = None
    for limiar in sorted(grade):
        alerta = p >= limiar
        total = int(((y == 0) & alerta).sum()) * custo_fp + int(((y == 1) & ~alerta).sum()) * custo_fn
        if melhor is None or total < melhor[1]:
            melhor = (float(limiar), total)
    return melhor
