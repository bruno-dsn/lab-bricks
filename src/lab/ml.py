"""Previsão de um dia à frente, com passado observado e teste temporal."""
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


FEATURES = ["lag_1", "lag_7", "media_7", "dia_semana"]


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
    modelo = make_pipeline(StandardScaler(), Ridge(alpha=10.0))
    modelo.fit(train[FEATURES], train["receita"])
    prediction = modelo.predict(test[FEATURES]).clip(min=0)
    result = pd.DataFrame({"real": test["receita"], "baseline": test["lag_1"], "modelo": prediction}, index=test.index)
    return result, {
        "mae_baseline": float(mean_absolute_error(result["real"], result["baseline"])),
        "mae_modelo": float(mean_absolute_error(result["real"], result["modelo"])),
        "treino_inicio": str(train.index.min().date()), "treino_fim": str(train.index.max().date()),
        "teste_inicio": str(test.index.min().date()), "teste_fim": str(test.index.max().date()),
    }
