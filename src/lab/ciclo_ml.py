"""Features no instante correto, seleção temporal e contrato de inferência."""
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, confusion_matrix, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

COLUNAS_ENTRADA = ["distancia_km", "volumes", "hora_pico", "previsao_chuva", "dia_semana"]


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
                  "logistica_C_0.1": make_pipeline(StandardScaler(), LogisticRegression(C=.1, random_state=seed, max_iter=300)),
                  "logistica_C_1": make_pipeline(StandardScaler(), LogisticRegression(C=1, random_state=seed, max_iter=300))}
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
