"""Exercício 5 · Tempo sem vazamento.

Duas habilidades: dividir por datas inteiras e criar features só com o passado.
"""
import pandas as pd


def dividir_por_datas(frame: pd.DataFrame, coluna: str = "data"):
    """Divide em (treino, validacao, teste) = 60%, 20%, 20% das DATAS distintas.

    * Uma data nunca pode aparecer em duas partes.
    * Com N datas ordenadas: corte1 = datas[int(N*0.6)], corte2 = datas[int(N*0.8)];
      treino < corte1 <= validacao < corte2 <= teste.
    * Se houver menos de 10 datas distintas, levante ValueError.
    """
    raise NotImplementedError


def criar_lag(serie: pd.Series, k: int) -> pd.Series:
    """Valor da série k posições atrás. k precisa ser inteiro >= 1; senão, ValueError.

    k = 0 devolveria o próprio alvo: isso é vazamento.
    """
    raise NotImplementedError


def media_movel_passada(serie: pd.Series, janela: int) -> pd.Series:
    """Média dos `janela` valores ANTERIORES (sem incluir o valor do próprio dia)."""
    raise NotImplementedError
