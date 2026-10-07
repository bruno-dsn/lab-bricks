# Databricks notebook source

# MAGIC %md
# MAGIC # 06 · Lab Bricks / JSON aninhado sem perder erros
# MAGIC Quatro mensagens próprias: duas válidas com três itens, uma malformada e uma sem itens. Exercício batch sem escrita; pode ser validado em Spark local.

# COMMAND ----------

from pyspark.sql import functions as F, types as T
import pandas as pd


def construir_json(spark):
    schema = T.StructType([
        T.StructField('pedido_id', T.StringType()),
        T.StructField('data_pedido', T.DateType()),
        T.StructField('itens', T.ArrayType(T.StructType([
            T.StructField('produto_id', T.IntegerType()),
            T.StructField('quantidade', T.IntegerType()),
            T.StructField('preco_centavos', T.LongType()),
        ]))),
    ])
    raw = pd.DataFrame({'evento_id': [1, 2, 3, 4], 'conteudo': [
        '{"pedido_id":"P001","data_pedido":"2026-01-01","itens":[{"produto_id":1,"quantidade":2,"preco_centavos":2400},{"produto_id":2,"quantidade":1,"preco_centavos":800}]}',
        '{"pedido_id":"P002","data_pedido":"2026-01-02","itens":[{"produto_id":3,"quantidade":1,"preco_centavos":12000}]}',
        '{JSON quebrado',
        '{"pedido_id":"P003","data_pedido":"2026-01-03","itens":[]}',
    ]})
    bronze_json = spark.createDataFrame(raw)
    parsed = bronze_json.withColumn('pedido', F.from_json('conteudo', schema))
    reason = (F.when(F.col('pedido.pedido_id').isNull() | F.col('pedido.data_pedido').isNull(), 'JSON, chave ou data inválida')
              .when(F.coalesce(F.size('pedido.itens'), F.lit(0)) <= 0, 'evento sem itens'))
    events = parsed.withColumn('motivo', reason)
    quarantine = events.where(F.col('motivo').isNotNull()).select('evento_id', 'conteudo', 'motivo')
    candidates = (events.where(F.col('motivo').isNull())
        .select('evento_id', F.col('pedido.pedido_id').alias('pedido_id'), F.col('pedido.data_pedido').alias('data_pedido'), F.explode('pedido.itens').alias('item')))
    valid_item = F.coalesce((F.col('item.produto_id') > 0) & (F.col('item.quantidade') > 0) & (F.col('item.preco_centavos') > 0), F.lit(False))
    rejected_items = candidates.where(~valid_item)
    silver_items = (candidates.where(valid_item).select('evento_id', 'pedido_id', 'data_pedido', 'item.*')
                    .withColumn('valor_centavos', F.col('quantidade') * F.col('preco_centavos')))
    return bronze_json, quarantine, silver_items, rejected_items

# COMMAND ----------

bronze_json, quarentena_json, silver_itens, itens_invalidos = construir_json(spark)
assert bronze_json.count() == 4
assert quarentena_json.count() == 2
assert silver_itens.count() == 3
assert itens_invalidos.count() == 0
assert silver_itens.agg(F.sum('valor_centavos')).first()[0] == 17600
display(quarentena_json)
display(silver_itens)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Reconcilie dois grãos
# MAGIC Mensagens e itens não têm a mesma contagem: duas mensagens válidas contêm três itens. A mensagem vazia não desaparece no explode: foi separada antes. Um item inválido fica em uma quarentena própria.
# MAGIC **Desafio:** acrescente um item com quantidade zero e defina seu motivo, preservando a mensagem de origem. Registre como novas colunas opcionais evoluiriam no contrato.
