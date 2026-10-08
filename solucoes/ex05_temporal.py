"""Solução de referência · Exercício 5."""
import pandas as pd


def dividir_por_datas(frame, coluna="data"):
    datas = sorted(frame[coluna].unique())
    if len(datas) < 10:
        raise ValueError("Use pelo menos dez datas distintas.")
    corte1, corte2 = datas[int(len(datas) * .6)], datas[int(len(datas) * .8)]
    return (frame.loc[frame[coluna] < corte1].copy(),
            frame.loc[(frame[coluna] >= corte1) & (frame[coluna] < corte2)].copy(),
            frame.loc[frame[coluna] >= corte2].copy())


def criar_lag(serie, k):
    if type(k) is not int or k < 1:
        raise ValueError("k precisa ser um inteiro >= 1.")
    return serie.shift(k)


def media_movel_passada(serie, janela):
    return serie.shift(1).rolling(janela).mean()
