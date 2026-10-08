"""Referência: cortes por datas, implementados sem TimeSeriesSplit."""
import pandas as pd


def dividir_datas(datas, splits=3, gap=1, horizonte=1):
    if any(type(x) is not int for x in (splits,gap,horizonte)) or not 2 <= splits <= 5 or not 1 <= horizonte <= gap <= 10:
        raise ValueError('Cortes inválidos.')
    dates=sorted(set(pd.to_datetime(datas,utc=True).normalize()))
    if len(dates)<20 or any(pd.isna(d) for d in dates):
        raise ValueError('Datas insuficientes ou ausentes.')
    cut=int(len(dates)*.8);dev=dates[:cut];test=dates[cut:]
    size=len(dev)//(splits+1);start=len(dev)-splits*size
    if start-gap<1:raise ValueError('Gap consome o treino.')
    windows=[(dev[:position-gap],dev[position:position+size]) for position in range(start,len(dev),size)]
    return windows,dev[:-gap],test
