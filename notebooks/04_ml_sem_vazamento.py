# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # 04 · Previsão que respeita o tempo
# MAGIC **Objetivo:** prever a receita de um dia à frente e comparar com três baselines: repetir ontem, repetir o mesmo dia da semana passada e prever sempre a média do treino.
# MAGIC 
# MAGIC Use a Gold criada no 02. As bibliotecas necessárias são pandas e scikit-learn. Se o ambiente serverless não as tiver, adicione-as pelo painel de ambiente do notebook antes de executar. MLflow é opcional para registrar as métricas.

# COMMAND ----------

# MAGIC %run ./00_configuracao

# COMMAND ----------

gold = spark.table(tabela("gold_diario")).orderBy("data_venda").limit(1000).toPandas()
print(f"{len(gold)} dias para o experimento.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Features disponíveis antes da previsão
# MAGIC Para o dia t usamos a receita de t-1, a de t-7, a média de t-7 até t-1 e o dia da semana de t. A receita do próprio dia t é o alvo e nunca entra nas features. O scaler é ajustado apenas no treino. O dia da semana entra como **categoria** (one-hot): tratar domingo=6 como "maior" que segunda=0 criaria uma ordem que não existe.
# MAGIC 
# MAGIC A avaliação é de um passo à frente: no segundo dia do teste, as vendas do primeiro já foram observadas. Não é uma projeção de 14 dias feita de uma vez.

# COMMAND ----------

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

# COMMAND ----------

previsoes, metricas = comparar(gold, dias_teste=14)
assert metricas["treino_fim"] < metricas["teste_inicio"]
display(previsoes.reset_index(names="data"))
print(metricas)
melhor_baseline = min(metricas["mae_baseline"], metricas["mae_baseline_semanal"], metricas["mae_baseline_media"])
if metricas["mae_modelo"] >= melhor_baseline:
    print("Uma baseline foi melhor ou empatou. Registre isso no relatório.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Registrar o experimento sem credencial embutida
# MAGIC O notebook usa a sessão autenticada no Databricks. A célula abaixo fica desligada por padrão. Para executá-la, habilite o widget e tenha MLflow no ambiente e permissão de criar experimentos em sua pasta pessoal.

# COMMAND ----------

dbutils.widgets.dropdown("registrar_mlflow", "nao", ["nao", "sim"])
if dbutils.widgets.get("registrar_mlflow") == "sim":
    import mlflow
    usuario = spark.sql("SELECT current_user() AS u").first()["u"]
    mlflow.set_experiment(f"/Users/{usuario}/databricks-na-pratica")
    with mlflow.start_run(run_name="ridge_receita_um_dia"):
        mlflow.log_params({"dias_teste": 14, "alpha": 10.0, "horizonte_dias": 1})
        mlflow.log_metrics({k: v for k, v in metricas.items() if k.startswith("mae_")})
        mlflow.set_tag("dados", "sinteticos")
    print("Experimento registrado.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercício
# MAGIC Teste 7, 14 e 21 dias no fim da série. Compare o MAE de cada alternativa. Justifique a janela escolhida com o uso pretendido e a quantidade de dados disponível.
# MAGIC 
# MAGIC Estes dados são fictícios. Uma boa métrica neste experimento não comprova qualidade em vendas reais.
