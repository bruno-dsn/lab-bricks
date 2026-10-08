"""Previsão de um dia à frente, com passado observado e teste temporal."""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


FEATURES = ["lag_1", "lag_7", "media_7", "dia_semana"]
NUMERICAS = ["lag_1", "lag_7", "media_7"]


def montar_modelo():
    """Ridge com dia da semana como categoria: segunda não é "menos" que domingo."""
    pre = ColumnTransformer([
        ("num", StandardScaler(), NUMERICAS),
        ("dia", OneHotEncoder(categories=[list(range(7))], sparse_output=False), ["dia_semana"]),
    ])
    return make_pipeline(pre, Ridge(alpha=10.0))


def preparar_features(gold):
    serie = gold.set_index(pd.to_datetime(gold["data_venda"]))["receita"].sort_index()
    if len(serie) < 30:
        raise ValueError("Use ao menos 30 dias de vendas.")
    serie = serie.reindex(pd.date_range(serie.index.min(), serie.index.max()), fill_value=0)
    df = pd.DataFrame({"receita": serie})
    df["lag_1"] = serie.shift(1)
    df["lag_7"] = serie.shift(7)
    df["media_7"] = serie.shift(1).rolling(7).mean()
    df["dia_semana"] = df.index.dayofweek
    return df.dropna()


def comparar(gold, dias_teste=14):
    if type(dias_teste) is not int or not 7 <= dias_teste <= 21:
        raise ValueError("Use entre 7 e 21 dias para o teste.")
    df = preparar_features(gold)
    if len(df) - dias_teste < 15:
        raise ValueError("Há poucos dias para treinar e avaliar.")
    train, test = df.iloc[:-dias_teste], df.iloc[-dias_teste:]
    modelo = montar_modelo()
    modelo.fit(train[FEATURES], train["receita"])
    prediction = modelo.predict(test[FEATURES]).clip(min=0)
    # Três baselines: ontem, o mesmo dia da semana passada e a média do treino (o "modelo" mais simples possível).
    media = pd.Series(float(train["receita"].mean()), index=test.index)
    result = pd.DataFrame({"real": test["receita"], "baseline": test["lag_1"], "baseline_semanal": test["lag_7"], "baseline_media": media, "modelo": prediction}, index=test.index)
    return result, {
        "mae_baseline": float(mean_absolute_error(result["real"], result["baseline"])),
        "mae_baseline_semanal": float(mean_absolute_error(result["real"], result["baseline_semanal"])),
        "mae_baseline_media": float(mean_absolute_error(result["real"], result["baseline_media"])),
        "mae_modelo": float(mean_absolute_error(result["real"], result["modelo"])),
        "treino_inicio": str(train.index.min().date()), "treino_fim": str(train.index.max().date()),
        "teste_inicio": str(test.index.min().date()), "teste_fim": str(test.index.max().date()),
    }
