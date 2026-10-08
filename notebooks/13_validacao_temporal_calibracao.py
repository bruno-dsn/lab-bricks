# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # Desenvolvimento, gap e calibração
# MAGIC 
# MAGIC Dados sintéticos. Pacote de referência: scikit-learn 1.8.0. As versões reais do workspace precisam entrar no registro. A célula de instalação reinicia o Python.

# COMMAND ----------

# MAGIC %pip install scikit-learn==1.8.0

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

"""Classificação com corte temporal, baseline e custo ilustrativo de decisão."""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

FEATURES = ["distancia_km", "volumes", "hora_pico", "previsao_chuva", "dia_semana"]
NUMERICAS = [f for f in FEATURES if f != "dia_semana"]


def montar_modelo(seed=42, C=1.0):
    """Logística com dia da semana categórico; o scaler só vê as features numéricas."""
    pre = ColumnTransformer([
        ("num", StandardScaler(), NUMERICAS),
        ("dia", OneHotEncoder(categories=[list(range(7))], sparse_output=False), ["dia_semana"]),
    ])
    return make_pipeline(pre, LogisticRegression(C=C, random_state=seed, max_iter=300))


def gerar_entregas(n=600, seed=42):
    if type(n) is not int or not 360 <= n <= 1200 or type(seed) is not int or not 0 <= seed <= 1000:
        raise ValueError("Use de 360 a 1.200 entregas e uma semente entre 0 e 1000.")
    rng = np.random.default_rng(seed)
    days = np.arange(n) * 60 // n
    distance = rng.uniform(1, 45, n)
    volumes = rng.integers(1, 8, n)
    peak, rain = rng.binomial(1, .4, n), rng.binomial(1, .25, n)
    score = -4.4 + distance * .07 + volumes * .12 + peak * .9 + rain * 1.2
    probability = 1 / (1 + np.exp(-score))
    late = rng.binomial(1, probability)
    return pd.DataFrame({"data": pd.Timestamp("2026-01-01") + pd.to_timedelta(days, unit="D"), "distancia_km": distance.round(2), "volumes": volumes, "hora_pico": peak, "previsao_chuva": rain, "dia_semana": (days + 3) % 7, "atrasou": late, "duracao_real_min": (distance * 2 + 15 + late * 30 + rng.uniform(0, 5, n)).round(2)})


def avaliar_entregas(n=600, seed=42, threshold=.5):
    if not isinstance(threshold, (int, float)) or isinstance(threshold, bool) or not .1 <= threshold <= .9:
        raise ValueError("Limiar deve ficar entre 0,1 e 0,9.")
    frame = gerar_entregas(n, seed)
    dates = sorted(frame["data"].unique())
    cutoff = dates[int(len(dates) * .8)]
    train, test = frame.loc[frame["data"] < cutoff], frame.loc[frame["data"] >= cutoff]
    model = montar_modelo(seed)
    model.fit(train[FEATURES], train["atrasou"])
    baseline = DummyClassifier(strategy="prior").fit(train[FEATURES], train["atrasou"])
    probability = model.predict_proba(test[FEATURES])[:, 1]
    base_probability = baseline.predict_proba(test[FEATURES])[:, 1]
    predicted = (probability >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(test["atrasou"], predicted, labels=[0, 1]).ravel()
    metrics = {"precision": precision_score(test["atrasou"], predicted, zero_division=0), "recall": recall_score(test["atrasou"], predicted, zero_division=0), "f1": f1_score(test["atrasou"], predicted, zero_division=0), "auc": roc_auc_score(test["atrasou"], probability) if test["atrasou"].nunique() == 2 else None, "brier": brier_score_loss(test["atrasou"], probability), "brier_baseline": brier_score_loss(test["atrasou"], base_probability), "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp), "custo_ilustrativo": int(fp) * 5 + int(fn) * 30, "treino_fim": str(train["data"].max().date()), "teste_inicio": str(test["data"].min().date()), "treino": len(train), "teste": len(test)}
    predictions = test.copy()
    predictions["probabilidade"] = probability
    predictions["alerta"] = predicted
    return predictions, metrics, train


def psi(reference, current, bins=8):
    """PSI com cortes fixados na referência. Indicador exploratório, não teste causal."""
    if type(bins) is not int or not 2 <= bins <= 20:
        raise ValueError("Número de faixas inválido.")
    a, b = np.asarray(reference, dtype=float), np.asarray(current, dtype=float)
    if a.ndim != 1 or b.ndim != 1 or not len(a) or not len(b) or max(len(a), len(b)) > 10_000 or not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("Use vetores finitos e não vazios.")
    cuts = np.unique(np.quantile(a, np.linspace(0, 1, bins + 1)))
    if len(cuts) < 2:
        # Uma faixa estreita isola a referência constante de valores deslocados.
        width = max(abs(a[0]), 1.0) * 1e-6
        cuts = np.array([-np.inf, a[0] - width, a[0] + width, np.inf])
    else:
        cuts[0], cuts[-1] = -np.inf, np.inf
    pa = np.histogram(a, bins=cuts)[0] / len(a)
    pb = np.histogram(b, bins=cuts)[0] / len(b)
    pa, pb = np.maximum(pa, 1e-6), np.maximum(pb, 1e-6)
    return float(np.sum((pb - pa) * np.log(pb / pa)))

# COMMAND ----------

"""Features no instante correto, seleção temporal e contrato de inferência."""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, confusion_matrix, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

COLUNAS_ENTRADA = ["distancia_km", "volumes", "hora_pico", "previsao_chuva", "dia_semana"]
NUMERICAS = [c for c in COLUNAS_ENTRADA if c != "dia_semana"]


def montar_modelo(seed=42, C=1.0):
    """Logística com dia da semana categórico; o scaler só vê as features numéricas."""
    pre = ColumnTransformer([
        ("num", StandardScaler(), NUMERICAS),
        ("dia", OneHotEncoder(categories=[list(range(7))], sparse_output=False), ["dia_semana"]),
    ])
    return make_pipeline(pre, LogisticRegression(C=C, random_state=seed, max_iter=300))


def juntar_no_instante(pedidos, historico):
    """Escolhe a última feature já disponível, preservando pedidos sem histórico."""
    contratos = [(pedidos, {"pedido_id", "cliente_id", "previsto_em"}),
                 (historico, {"cliente_id", "disponivel_em", "risco_historico"})]
    for frame, columns in contratos:
        if not isinstance(frame, pd.DataFrame) or set(frame.columns) != columns or frame.columns.duplicated().any() or not 1 <= len(frame) <= 2000:
            raise ValueError("Contrato de colunas ou tamanho inválido para a junção temporal.")
        if not frame.cliente_id.map(lambda x: isinstance(x, str) and bool(x)).all():
            raise ValueError("Cada cliente precisa de uma chave textual não vazia.")
    left, right = pedidos.copy(), historico.copy()
    if left.pedido_id.isna().any() or left.pedido_id.duplicated().any():
        raise ValueError("pedido_id precisa ser único e preenchido.")
    left["previsto_em"] = pd.to_datetime(left.previsto_em, utc=True, errors="raise")
    right["disponivel_em"] = pd.to_datetime(right.disponivel_em, utc=True, errors="raise")
    if left.previsto_em.isna().any() or right.disponivel_em.isna().any():
        raise ValueError("Instantes não podem ser nulos.")
    risk = pd.to_numeric(right.risco_historico, errors="raise")
    if not np.isfinite(risk).all() or not risk.between(0, 1).all():
        raise ValueError("Risco histórico precisa estar entre zero e um.")
    right["risco_historico"] = risk
    if right.duplicated(["cliente_id", "disponivel_em"]).any():
        raise ValueError("Duas versões disponíveis no mesmo instante são ambíguas.")
    left["_ordem_lb"] = np.arange(len(left))
    joined = pd.merge_asof(left.sort_values("previsto_em", kind="mergesort"),
                           right.sort_values("disponivel_em", kind="mergesort"),
                           left_on="previsto_em", right_on="disponivel_em",
                           by="cliente_id", direction="backward")
    return joined.sort_values("_ordem_lb").drop(columns="_ordem_lb").reset_index(drop=True)


def validar_entrada(frame):
    """Contrato do caso fictício: nomes, números finitos e domínio de cada feature."""
    if not isinstance(frame, pd.DataFrame) or frame.columns.duplicated().any() or set(frame.columns) != set(COLUNAS_ENTRADA) or not 1 <= len(frame) <= 1200:
        raise ValueError("Use somente as cinco features do contrato, em até 1.200 linhas.")
    if any(not pd.api.types.is_numeric_dtype(frame[c]) or pd.api.types.is_bool_dtype(frame[c]) for c in COLUNAS_ENTRADA):
        raise ValueError("Features precisam ser numéricas; texto e booleanos são rejeitados.")
    values = frame[COLUNAS_ENTRADA].astype(float)
    if not np.isfinite(values.to_numpy()).all():
        raise ValueError("Features precisam ser preenchidas e finitas.")
    valid = (values.distancia_km.between(1, 45) & values.volumes.between(1, 7)
             & values.volumes.mod(1).eq(0) & values.hora_pico.isin([0, 1])
             & values.previsao_chuva.isin([0, 1]) & values.dia_semana.between(0, 6)
             & values.dia_semana.mod(1).eq(0))
    if not valid.all():
        raise ValueError("Feature fora do domínio do caso fictício de entregas.")
    return values


def dividir_por_datas(frame):
    """60%/20%/20% de datas inteiras; nenhum dia entra em duas partições."""
    if not isinstance(frame, pd.DataFrame) or "data" not in frame or not 100 <= len(frame) <= 1200:
        raise ValueError("Use um histórico com datas e de 100 a 1.200 linhas.")
    data = frame.copy()
    data["data"] = pd.to_datetime(data.data, utc=True, errors="raise").dt.normalize()
    dates = sorted(data.data.dropna().unique())
    if data.data.isna().any() or len(dates) < 10:
        raise ValueError("Use pelo menos dez datas preenchidas.")
    cut1, cut2 = dates[int(len(dates) * .6)], dates[int(len(dates) * .8)]
    return tuple(part.copy() for part in [data.loc[data.data < cut1],
                 data.loc[(data.data >= cut1) & (data.data < cut2)], data.loc[data.data >= cut2]])


def _medir(labels, probability, threshold):
    predicted = (probability >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(labels, predicted, labels=[0, 1]).ravel()
    return {"brier": float(brier_score_loss(labels, probability)),
            "auc": float(roc_auc_score(labels, probability)) if labels.nunique() == 2 else None,
            "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
            "custo": int(fp) * 5 + int(fn) * 30}


def avaliar_ciclo(frame, seed=42):
    """Seleciona modelo/limiar na validação e aplica a escolha congelada ao teste."""
    if not isinstance(frame, pd.DataFrame) or type(seed) is not int or not 0 <= seed <= 1000 or "atrasou" not in frame or not frame.atrasou.isin([0, 1]).all():
        raise ValueError("Semente ou rótulos inválidos.")
    validar_entrada(frame[COLUNAS_ENTRADA])
    train, validation, test = dividir_por_datas(frame)
    if train.atrasou.nunique() != 2:
        raise ValueError("Treino precisa conter as duas classes.")
    candidates = {"baseline": DummyClassifier(strategy="prior"),
                  "logistica_C_0.1": montar_modelo(seed, .1),
                  "logistica_C_1": montar_modelo(seed, 1)}
    rows = []
    for name, model in candidates.items():
        model.fit(validar_entrada(train[COLUNAS_ENTRADA]), train.atrasou)
        probability = model.predict_proba(validar_entrada(validation[COLUNAS_ENTRADA]))[:, 1]
        for threshold in np.linspace(.1, .9, 17):
            rows.append({"modelo": name, "limiar": float(threshold), **_medir(validation.atrasou, probability, threshold)})
    board = pd.DataFrame(rows).sort_values(["custo", "brier", "modelo", "limiar"], kind="mergesort").reset_index(drop=True)
    chosen = board.iloc[0]
    model = candidates[chosen.modelo]
    test_probability = model.predict_proba(validar_entrada(test[COLUNAS_ENTRADA]))[:, 1]
    final = _medir(test.atrasou, test_probability, chosen.limiar)
    final.update(modelo=chosen.modelo, limiar=float(chosen.limiar), custo_validacao=int(chosen.custo),
                 treino=len(train), validacao=len(validation), teste=len(test),
                 treino_fim=str(train.data.max().date()), validacao_inicio=str(validation.data.min().date()),
                 validacao_fim=str(validation.data.max().date()), teste_inicio=str(test.data.min().date()))
    scored = test[["data", "atrasou"]].copy()
    scored["probabilidade"] = test_probability
    scored["alerta"] = (test_probability >= chosen.limiar).astype(int)
    return model, board, final, scored

# COMMAND ----------

"""Seleção, calibração e decisões em janelas temporais sem consumir o teste."""
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator


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

# COMMAND ----------

frame = gerar_entregas(600,42)
windows, refit, test = janelas_temporais(frame,gap=2)
for treino,validacao in windows:
    assert (validacao.data.min()-treino.data.max()).days >= 3
    assert set(validacao.data).isdisjoint(test.data)
model, ranking, avaliacao = selecionar_temporal(frame,gap=2)
display(ranking.head(8))
print(avaliacao)
calibracao, curvas = comparar_calibracao(frame)
display(calibracao)
for nome,curva in curvas.items():
    print(nome)
    display(curva)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Desafio
# MAGIC 
# MAGIC Mude apenas os rótulos do teste e prove que seleção e limiar empírico não mudam. Compare limiar teórico e empírico com suporte por intervalo. Registre resultado, não uma promessa de melhoria.
