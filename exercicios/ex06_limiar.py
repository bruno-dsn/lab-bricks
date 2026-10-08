"""Exercício 6 · O limiar vem do custo da decisão.

Alertar quando p * custo_fn >= (1 - p) * custo_fp  =>  p >= custo_fp / (custo_fp + custo_fn).
"""
import numpy as np


def limiar_teorico(custo_fp: float, custo_fn: float) -> float:
    """Limiar ótimo se as probabilidades forem calibradas. Custos precisam ser > 0, senão ValueError."""
    raise NotImplementedError


def limiar_empirico(y, p, custo_fp: float = 5, custo_fn: float = 30, grade=None):
    """Procura o limiar de menor custo numa grade e devolve (limiar, custo).

    * Padrão da grade: np.round(np.arange(0.05, 0.951, 0.01), 2)
    * Alerta quando p >= limiar.
    * Em empate de custo, escolha o MENOR limiar.
    """
    raise NotImplementedError
