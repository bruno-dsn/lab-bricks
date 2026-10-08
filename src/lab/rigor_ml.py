"""Seleção, calibração e decisões em janelas temporais sem consumir o teste."""
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator
from .ciclo_ml import COLUNAS_ENTRADA, validar_entrada, montar_modelo, _medir


def janelas_temporais(frame, splits=3, gap=1, horizonte=1):
    if not isinstance(frame, pd.DataFrame) or not 100 <= len(frame) <= 1200 or 'data' not in frame:
        raise ValueError('Histórico precisa conter datas e de 100 a 1.200 linhas.')
    if any(type(x) is not int for x in (splits, gap, horizonte)) or not 2 <= splits <= 5 or not 1 <= horizonte <= gap <= 10:
        raise ValueError('Gap precisa cobrir o horizonte; ambos medidos em datas observadas.')
    data = frame.copy()
    data['data'] = pd.to_datetime(data.data, utc=True, errors='raise').dt.normalize()
    if data.data.isna().any():
        raise ValueError('Data ausente.')
    dates = sorted(data.data.unique())
    if len(dates) < 20:
        raise ValueError('Use ao menos 20 datas distintas.')
    cut = int(len(dates) * .8)
    development, final_test = dates[:cut], dates[cut:]
    windows = []
    try:
        for tr, va in TimeSeriesSplit(n_splits=splits, gap=gap).split(development):
            windows.append((data.loc[data.data.isin([development[i] for i in tr])].copy(),
                            data.loc[data.data.isin([development[i] for i in va])].copy()))
    except ValueError:
        raise ValueError('Datas insuficientes para estas janelas e gap.') from None
    # Também purga o fim do desenvolvimento antes de refazer o modelo final.
    refit = data.loc[data.data.isin(development[:-gap])].copy()
    test = data.loc[data.data.isin(final_test)].copy()
    return windows, refit, test


def _validar_rotulos(frame):
    validar_entrada(frame[COLUNAS_ENTRADA])
    if 'atrasou' not in frame or not frame.atrasou.isin([0, 1]).all():
        raise ValueError('Rótulo precisa ser binário e preenchido.')


def selecionar_temporal(frame, splits=3, gap=1, horizonte=1):
    _validar_rotulos(frame)
    windows, refit, test = janelas_temporais(frame, splits, gap, horizonte)
    rows = []
    for c in (.1, 1.):
        predictions, labels = [], []
        for train, validation in windows:
            if train.atrasou.nunique() != 2:
                raise ValueError('Cada treino precisa conter as duas classes.')
            model = montar_modelo(42, c).fit(train[COLUNAS_ENTRADA], train.atrasou)
            predictions.extend(model.predict_proba(validation[COLUNAS_ENTRADA])[:, 1])
            labels.extend(validation.atrasou)
        for threshold in np.linspace(.1, .9, 17):
            rows.append({'C': c, 'limiar': float(threshold), **_medir(pd.Series(labels), np.array(predictions), threshold)})
    board = pd.DataFrame(rows).sort_values(['custo', 'brier', 'C', 'limiar'], kind='mergesort').reset_index(drop=True)
    choice = board.iloc[0]
    model = montar_modelo(42, choice.C).fit(refit[COLUNAS_ENTRADA], refit.atrasou)
    probability = model.predict_proba(test[COLUNAS_ENTRADA])[:, 1]
    final = {'C': float(choice.C), 'limiar': float(choice.limiar), 'custo_validacao': int(choice.custo),
             'teste_inicio': str(test.data.min().date()), 'gap_datas': gap, **_medir(test.atrasou, probability, choice.limiar)}
    return model, board, final


def confiabilidade(labels, probability, bins=10):
    y, p = np.asarray(labels, dtype=float), np.asarray(probability, dtype=float)
    if y.ndim != 1 or p.shape != y.shape or not 1 <= len(y) <= 10_000 or not np.isin(y, [0, 1]).all() or not np.isfinite(p).all() or not ((p >= 0) & (p <= 1)).all():
        raise ValueError('Rótulos e probabilidades fora do contrato.')
    if type(bins) is not int or not 2 <= bins <= 20:
        raise ValueError('Use de 2 a 20 intervalos.')
    assignments = np.minimum((p * bins).astype(int), bins - 1)
    rows, ece = [], 0.
    for i in range(bins):
        mask = assignments == i
        if mask.any():
            avg, freq = float(p[mask].mean()), float(y[mask].mean())
            ece += mask.mean() * abs(avg - freq)
            rows.append({'intervalo': i, 'probabilidade_media': avg, 'frequencia_observada': freq, 'n': int(mask.sum())})
    return pd.DataFrame(rows), float(ece)


def comparar_calibracao(frame, horizonte=1):
    _validar_rotulos(frame)
    if type(horizonte) is not int or not 1 <= horizonte <= 5:
        raise ValueError('Horizonte precisa ser de 1 a 5 datas observadas.')
    data = frame.copy(); data['data'] = pd.to_datetime(data.data, utc=True, errors='raise').dt.normalize()
    dates = sorted(data.data.unique())
    if data.data.isna().any() or len(dates) < 40:
        raise ValueError('Calibração exige ao menos 40 datas.')
    a, b, c = [int(len(dates) * fraction) for fraction in (.5, .6, .8)]
    parts = [dates[:a-horizonte], dates[a:b-horizonte], dates[b:c-horizonte], dates[c:]]
    train, calibration, validation, test = [data.loc[data.data.isin(d)].copy() for d in parts]
    if any(part.empty or part.atrasou.nunique() != 2 for part in (train, calibration)):
        raise ValueError('Treino e calibração precisam conter duas classes e linhas suficientes.')
    base = montar_modelo().fit(train[COLUNAS_ENTRADA], train.atrasou)
    calibrated = CalibratedClassifierCV(FrozenEstimator(base), method='sigmoid').fit(calibration[COLUNAS_ENTRADA], calibration.atrasou)
    rows, curves = [], {}
    for name, model in [('base', base), ('sigmoid', calibrated)]:
        vp = model.predict_proba(validation[COLUNAS_ENTRADA])[:, 1]
        choice = min(((_medir(validation.atrasou, vp, t)['custo'], t) for t in np.linspace(.05, .9, 18)))
        tp = model.predict_proba(test[COLUNAS_ENTRADA])[:, 1]
        curve, ece = confiabilidade(test.atrasou, tp)
        curves[name] = curve
        rows.append({'modelo': name, 'limiar_empirico': float(choice[1]), 'limiar_teorico': 5/35,
                     'custo_validacao': int(choice[0]), 'ece_teste': ece,
                     'custo_teorico_teste': _medir(test.atrasou, tp, 5/35)['custo'], **_medir(test.atrasou, tp, choice[1])})
    return pd.DataFrame(rows), curves


def decidir_monitoramento(psi, brier_referencia, brier_atual, rotulos):
    if any(not isinstance(x, (int, float)) or isinstance(x, bool) or not np.isfinite(x) or x < 0 for x in (psi, brier_referencia, brier_atual)) or brier_referencia > 1 or brier_atual > 1 or type(rotulos) is not int or rotulos < 0:
        raise ValueError('Métricas de monitoramento inválidas.')
    if rotulos < 80:
        return 'Investigar qualidade e coletar rótulos; suporte insuficiente para avaliar desempenho.'
    if brier_atual - brier_referencia >= .02:
        return 'Treinar candidato e comparar temporalmente; promoção exige revisão humana.'
    if psi >= .2:
        return 'Investigar mudança de distribuição; PSI sozinho não decide retreinamento.'
    return 'Continuar monitorando; regras didáticas precisam de adaptação ao negócio.'
