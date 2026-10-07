# Databricks notebook source

# MAGIC %md
# MAGIC # 09 · Lab Bricks / risco de atraso e custo da decisão
# MAGIC Exemplo original de 600 entregas fictícias. Executa com Pandas e scikit-learn. Sem escrita Delta, registro de modelo ou endpoint automático. Se a biblioteca faltar, configure o ambiente conforme o README.

# COMMAND ----------

"""Classificação com corte temporal, baseline e custo ilustrativo de decisão."""
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = ["distancia_km", "volumes", "hora_pico", "previsao_chuva", "dia_semana"]


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
    model = make_pipeline(StandardScaler(), LogisticRegression(random_state=seed, max_iter=300))
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

previsoes, metricas, treino = avaliar_entregas()
assert metricas['treino'] == 480 and metricas['teste'] == 120
assert treino['data'].max() < previsoes['data'].min()
assert 'duracao_real_min' not in FEATURES
print(metricas)
display(previsoes[['data', *FEATURES, 'atrasou', 'probabilidade', 'alerta']])

# COMMAND ----------

for limiar in [.2, .5, .8]:
    _, resultado, _ = avaliar_entregas(threshold=limiar)
    print({key: resultado[key] for key in ['precision', 'recall', 'fp', 'fn', 'custo_ilustrativo']}, 'limiar=', limiar)
print('PSI sem mudança:', psi(treino['distancia_km'], treino['distancia_km']))
print('PSI com deslocamento:', psi(treino['distancia_km'], previsoes['distancia_km'] + 10))

# COMMAND ----------

# MAGIC %md
# MAGIC **Desafio:** escolha um limiar em uma validação temporal separada e congele antes do teste final. Os custos são ilustrativos. PSI da distância não prova queda de desempenho sem novos rótulos.
# MAGIC Para MLOps, registre commit, datas, FEATURES, baseline e métricas em um run autorizado. Tracking, registry e serving são etapas distintas.
