# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # 00 · Preparar seu espaço de estudo
# MAGIC Esta configuração é usada por todos os notebooks. Ela cria um schema de estudo cujo nome é derivado da identidade autenticada no Databricks.
# MAGIC 
# MAGIC Escolha no widget um catálogo em que você possa criar schemas e tabelas. O catálogo atual é o padrão. Não execute no catálogo de produção.
# MAGIC 
# MAGIC O nome por usuário evita colisões acidentais. **As permissões de acesso continuam sendo responsabilidade do Unity Catalog.**

# COMMAND ----------

import hashlib
import re

current_catalog = spark.sql("SELECT current_catalog() AS nome").first()["nome"]
dbutils.widgets.text("catalogo", current_catalog, "Catálogo de estudo")
CATALOG = dbutils.widgets.get("catalogo").strip()
if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,63}", CATALOG):
    raise ValueError("Escolha um catálogo com nome simples: letras, números e underscore.")
identity = spark.sql("SELECT current_user() AS usuario").first()["usuario"]
SCHEMA = "dbnp_" + hashlib.sha256(identity.encode()).hexdigest()[:12]
CATALOG_SQL = f"`{CATALOG}`"
SCHEMA_SQL = f"`{SCHEMA}`"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG_SQL}.{SCHEMA_SQL}")
print(f"Espaço de estudo: {CATALOG}.{SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Uma fonte reproduzível
# MAGIC O gerador é o mesmo usado no laboratório local. Nenhum download nem token de API é necessário. Cada linha é um pedido com um produto. Os dados começam em 1º de janeiro de 2026 e cobrem 90 dias.

# COMMAND ----------

"""Uma fonte pequena, determinística e inteiramente fictícia."""
from datetime import date, timedelta
from random import Random


COLUNAS = [
    "venda_id", "data_venda", "produto", "categoria", "canal",
    "quantidade", "preco_unitario", "status", "atualizado_em",
]


def gerar_vendas(n=720, sujeira=True, seed=42):
    """Gera strings como um CSV recebido de outra ferramenta.

    Cada linha representa um pedido com um único produto. As seis linhas
    inválidas e uma versão repetida são adicionadas ao tamanho solicitado.
    """
    if type(n) is not int or not 90 <= n <= 2000:
        raise ValueError("Use entre 90 e 2000 pedidos.")
    if type(seed) is not int or not 0 <= seed <= 1000:
        raise ValueError("Use uma semente inteira entre 0 e 1000.")
    if type(sujeira) is not bool:
        raise ValueError("A opção de qualidade deve ser booleana.")
    rng = Random(seed)
    produtos = [
        ("Caderno", "Papelaria", "24.90"),
        ("Luminaria", "Casa", "89.90"),
        ("Fone", "Tecnologia", "159.90"),
        ("Garrafa", "Casa", "49.90"),
    ]
    rows = []
    for i in range(n):
        dia = date(2026, 1, 1) + timedelta(days=i % 90)
        produto, categoria, preco = rng.choice(produtos)
        rows.append(dict(zip(COLUNAS, [
            f"V{i+1:06d}", dia.isoformat(), produto, categoria,
            rng.choice(["Site", "Aplicativo", "Marketplace"]),
            str(rng.randint(1, 5)), preco,
            "cancelada" if rng.random() < 0.12 else "concluida",
            f"{dia.isoformat()} 10:00:00",
        ])))
    if sujeira:
        rows.append({**rows[0], "quantidade": "4", "atualizado_em": "2026-04-01 12:00:00"})
        falhas = [
            {"data_venda": "2026-02-30"}, {"quantidade": "0"},
            {"preco_unitario": "-9.90"}, {"produto": ""},
            {"status": "desconhecida"}, {"venda_id": ""},
        ]
        for i, falha in enumerate(falhas):
            rows.append({**rows[1], "venda_id": f"X{i+1:06d}", **falha})
    return rows

# COMMAND ----------

# MAGIC %md
# MAGIC ## Funções que vamos reutilizar
# MAGIC Leia as funções quando chegar ao notebook 02. `normalizar` separa chaves inválidas, ordena as versões e só então valida as regras do negócio. Uma versão recente inválida vai para a quarentena.

# COMMAND ----------

from pyspark.sql import functions as F, Window

def tabela(nome):
    if not re.fullmatch(r"[a-z][a-z0-9_]{0,63}", nome):
        raise ValueError("Nome de tabela inválido.")
    return f"{CATALOG_SQL}.{SCHEMA_SQL}.`{nome}`"

def fonte(n=720, sujeira=True):
    rows = gerar_vendas(n=n, sujeira=sujeira)
    values = [tuple(row[col] for col in COLUNAS) + (i,) for i, row in enumerate(rows)]
    schema = ", ".join(f"{col} STRING" for col in COLUNAS) + ", _ordem LONG"
    return spark.createDataFrame(values, schema=schema)

def normalizar(bronze):
    # Um campo nulo é vazio para as regras; a Bronze conserva a entrada original.
    df = bronze.select(*[F.trim(F.coalesce(F.col(c), F.lit(""))).alias(c) for c in COLUNAS], "_ordem")
    df = df.withColumn("status", F.lower("status"))
    df = df.withColumn("_ts", F.expr("try_cast(atualizado_em AS TIMESTAMP)"))
    chave_ok = (F.col("venda_id") != "") & F.col("_ts").isNotNull() & F.col("atualizado_em").rlike(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
    invalidas_chave = df.where(~chave_ok).select(*COLUNAS).withColumn("motivo", F.lit("chave ou atualização inválida"))
    w = Window.partitionBy("venda_id").orderBy(F.col("_ts").desc(), F.col("_ordem").desc())
    ranked = df.where(chave_ok).withColumn("_rank", F.row_number().over(w))
    substituidas = ranked.where("_rank > 1").select(*COLUNAS)
    latest = ranked.where("_rank = 1")
    latest = latest.withColumn("_data", F.expr("try_cast(data_venda AS DATE)"))
    latest = latest.withColumn("_qtd", F.expr("try_cast(quantidade AS INT)"))
    latest = latest.withColumn("_preco", F.expr("try_cast(preco_unitario AS DECIMAL(12,2))"))
    regras = [
        (F.col("_data").isNotNull() & F.col("data_venda").rlike(r"^\d{4}-\d{2}-\d{2}$"), "data inválida"),
        (F.col("quantidade").rlike(r"^[0-9]{1,4}$") & F.col("_qtd").between(1, 1000), "quantidade inválida"),
        (F.col("preco_unitario").rlike(r"^[0-9]{1,8}(\.[0-9]{1,2})?$") & (F.col("_preco") > 0), "preço inválido"),
        ((F.col("produto") != "") & (F.col("categoria") != "") & (F.col("canal") != ""), "dimensão vazia"),
        (F.col("status").isin("concluida", "cancelada"), "status inválido"),
    ]
    latest = latest.withColumn("motivo", F.concat_ws("; ", *[
        F.when(~F.coalesce(ok, F.lit(False)), F.lit(motivo)) for ok, motivo in regras
    ]))
    rejeitadas = invalidas_chave.unionByName(latest.where("motivo != ''").select(*COLUNAS, "motivo"))
    silver = latest.where("motivo = ''").select(
        "venda_id", F.col("_data").alias("data_venda"), "produto", "categoria", "canal",
        F.col("_qtd").alias("quantidade"), F.col("_preco").alias("preco_unitario"), "status",
        F.col("_ts").alias("atualizado_em"),
        (F.col("_preco") * 100).cast("long").alias("preco_centavos"),
        (F.col("_preco") * 100 * F.col("_qtd")).cast("long").alias("valor_centavos"),
    )
    return silver, rejeitadas, substituidas

# COMMAND ----------

# MAGIC %md
# MAGIC ## Confira antes de continuar
# MAGIC O comando acima criou apenas o schema e as funções. Os notebooks seguintes escrevem exclusivamente tabelas de estudo nesse schema. Rerodar 02 substitui os snapshots de estudo. O notebook 03 usa uma tabela separada para o MERGE.
