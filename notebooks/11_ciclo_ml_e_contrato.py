# Databricks notebook source
# MAGIC %md
# MAGIC # 11 · Features, seleção temporal e contrato de inferência
# MAGIC Prática original inspirada nos temas de Databricks ML in Action. Não reproduz código do livro.
# MAGIC A primeira parte usa Pandas/scikit-learn no notebook. A segunda oferece Tracking MLflow 3 opcional, sem registrar em UC, trocar aliases ou criar endpoints.
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
# COMMAND ----------
frame = gerar_entregas()
model, ranking, evaluation, scored = avaliar_ciclo(frame)
assert (evaluation['treino'], evaluation['validacao'], evaluation['teste']) == (360, 120, 120)
display(ranking.head(10))
display(pd.DataFrame([evaluation]))
display(scored.head(10))
# COMMAND ----------
pedidos = pd.DataFrame({'pedido_id': ['P1', 'P2', 'P3'], 'cliente_id': ['A', 'A', 'B'], 'previsto_em': ['2026-01-10T10:00:00Z', '2026-01-10T13:00:00Z', '2026-01-10T10:00:00Z']})
historico = pd.DataFrame({'cliente_id': ['A', 'A'], 'disponivel_em': ['2026-01-09T09:00:00Z', '2026-01-10T12:00:00Z'], 'risco_historico': [.2, .8]})
joined = juntar_no_instante(pedidos, historico)
assert joined.risco_historico.iloc[:2].tolist() == [.2, .8]
assert pd.isna(joined.risco_historico.iloc[2])
display(joined)
# COMMAND ----------
example = frame.loc[:2, COLUNAS_ENTRADA].copy()
validar_entrada(example)
invalid = example.drop(columns='previsao_chuva')
try:
    validar_entrada(invalid)
except ValueError:
    print('Feature ausente rejeitada, como esperado.')
else:
    raise AssertionError('Contrato aceitou entrada incompatível.')
# COMMAND ----------
# MAGIC %md
# MAGIC ## Tracking opcional em MLflow 3
# MAGIC Selecione um experimento em que você tenha permissão. A política inclui o limiar escolhido, e a assinatura tem probabilidades e alertas como saída. O exemplo de entrada contém somente dados fictícios.
# MAGIC Este trecho exige MLflow 3 e execução na sua conta; sua execução remota permanece pendente no registro do projeto.
# COMMAND ----------
dbutils.widgets.dropdown('registrar_experimento', 'nao', ['nao', 'sim'])
dbutils.widgets.text('experimento_mlflow', '')
if dbutils.widgets.get('registrar_experimento') == 'sim':
    import mlflow
    from mlflow.models import infer_signature
    if int(mlflow.__version__.split('.')[0]) < 3:
        raise ValueError('Use um ambiente com MLflow 3; consulte o guia antes de atualizar pacotes.')
    experiment = dbutils.widgets.get('experimento_mlflow').strip()
    if not experiment:
        raise ValueError('Informe o caminho de um experimento autorizado.')
    mlflow.set_experiment(experiment)

    class PoliticaEntregas(mlflow.pyfunc.PythonModel):
        def __init__(self, modelo, limiar):
            self.modelo, self.limiar = modelo, limiar

        def predict(self, context, model_input, params=None):
            inputs = validar_entrada(model_input)
            probability = self.modelo.predict_proba(inputs)[:, 1]
            return pd.DataFrame({'probabilidade': probability, 'alerta': (probability >= self.limiar).astype(int)})

    policy = PoliticaEntregas(model, evaluation['limiar'])
    expected = policy.predict(None, example)
    with mlflow.start_run(run_name='lab-bricks-ciclo-ml') as run:
        mlflow.log_params({'semente': 42, 'modelo': evaluation['modelo'], 'limiar': evaluation['limiar'], 'treino': 360, 'validacao': 120, 'teste': 120})
        mlflow.log_metrics({'custo_validacao': evaluation['custo_validacao'], 'custo_teste': evaluation['custo'], 'brier_teste': evaluation['brier']})
        mlflow.set_tags({'projeto': 'lab-bricks', 'dados': 'ficticios', 'protocolo': 'temporal-60-20-20'})
        model_info = mlflow.pyfunc.log_model(name='politica_entregas', python_model=policy, signature=infer_signature(example, expected), input_example=example)
        print('Run:', run.info.run_id)
        print('Modelo:', model_info.model_uri)
    restored = mlflow.pyfunc.load_model(model_info.model_uri)
    actual = restored.predict(example)
    np.testing.assert_allclose(actual.probabilidade, expected.probabilidade, rtol=1e-8)
    assert actual.alerta.tolist() == expected.alerta.tolist()
    print('Round-trip da política validado. Registry e serving continuam etapas separadas.')
else:
    print('Tracking não solicitado. Práticas locais concluídas; etapa MLflow pendente.')

# EXTENSAO ESCOLA V3

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

_, ranking_temporal, avaliacao_temporal = selecionar_temporal(frame,gap=1)
display(ranking_temporal.head(8))
print(avaliacao_temporal)
