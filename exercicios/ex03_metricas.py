"""Exercício 3 · Métricas à mão (sem sklearn.metrics).

Use só NumPy. `y` são rótulos 0/1; `pred` são previsões 0/1; `p` são probabilidades.
"""
import numpy as np


def matriz(y, pred) -> tuple:
    """Devolve (tn, fp, fn, tp) como inteiros."""
    raise NotImplementedError


def precision_recall_f1(y, pred) -> tuple:
    """Devolve (precision, recall, f1). Quando o denominador for zero, o valor é 0.0."""
    raise NotImplementedError


def brier(y, p) -> float:
    """Erro quadrático médio entre a probabilidade e o rótulo."""
    raise NotImplementedError


def custo(fp: int, fn: int, custo_fp: float = 5, custo_fn: float = 30) -> float:
    """Custo total dos erros."""
    raise NotImplementedError
