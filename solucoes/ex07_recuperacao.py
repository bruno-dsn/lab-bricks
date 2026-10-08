"""Solução de referência · Exercício 7."""


def recall_em_k(rankings, esperados, k):
    return sum(e in r[:k] for r, e in zip(rankings, esperados)) / len(esperados)


def mrr(rankings, esperados, k=5):
    total = 0.0
    for r, e in zip(rankings, esperados):
        top = list(r[:k])
        total += 1 / (top.index(e) + 1) if e in top else 0.0
    return total / len(esperados)
