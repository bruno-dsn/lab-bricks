"""Solução de referência · Exercício 3."""
import numpy as np


def matriz(y, pred):
    y, pred = np.asarray(y).astype(int), np.asarray(pred).astype(int)
    return (int(((y == 0) & (pred == 0)).sum()), int(((y == 0) & (pred == 1)).sum()),
            int(((y == 1) & (pred == 0)).sum()), int(((y == 1) & (pred == 1)).sum()))


def precision_recall_f1(y, pred):
    _, fp, fn, tp = matriz(y, pred)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


def brier(y, p):
    return float(np.mean((np.asarray(p, dtype=float) - np.asarray(y, dtype=float)) ** 2))


def custo(fp, fn, custo_fp=5, custo_fn=30):
    return fp * custo_fp + fn * custo_fn
