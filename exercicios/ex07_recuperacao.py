"""Exercício 7 · Medir uma busca: recall@k e MRR.

`rankings` é uma lista de listas de ids, do mais para o menos relevante.
`esperados` é uma lista com o id correto de cada pergunta (mesma ordem).
"""


def recall_em_k(rankings, esperados, k: int) -> float:
    """Fração de perguntas cujo id esperado aparece entre os k primeiros do ranking."""
    raise NotImplementedError


def mrr(rankings, esperados, k: int = 5) -> float:
    """Média de 1/posição (começando em 1) do id esperado; 0 se estiver fora do top-k."""
    raise NotImplementedError
