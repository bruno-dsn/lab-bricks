"""Lab Bricks / fonte batch pequena para Lakeflow Spark Declarative Pipelines.

Adicionar como arquivo-fonte de uma pipeline na conta; não executar como notebook.
Escolher catálogo e schema de estudo autorizados. Não utiliza LIVE nem escrita manual.
"""
from pyspark import pipelines as dp
from pyspark.sql import functions as F


def regra_valida():
    return F.coalesce((F.col('valor_centavos') > 0) & F.col('status').isin('concluida', 'cancelada'), F.lit(False))


@dp.materialized_view()
def bronze_declarativa():
    return (spark.range(1, 5)
            .withColumn('valor_centavos', F.when(F.col('id') == 1, 1200).when(F.col('id') == 2, 2200).when(F.col('id') == 3, -10).otherwise(F.lit(None).cast('long')))
            .withColumn('status', F.when(F.col('id') == 2, 'cancelada').otherwise('concluida')))


@dp.materialized_view()
@dp.expect_or_fail('valor_positivo', 'valor_centavos > 0')
@dp.expect_or_fail('chave_presente', 'id IS NOT NULL')
def silver_declarativa():
    return spark.read.table('bronze_declarativa').where(regra_valida())


@dp.materialized_view()
def quarentena_declarativa():
    return (spark.read.table('bronze_declarativa').where(~regra_valida())
            .withColumn('motivo', F.lit('valor ou status fora do contrato')))


@dp.materialized_view()
def gold_declarativa():
    return (spark.read.table('silver_declarativa').where("status='concluida'")
            .agg(F.sum('valor_centavos').alias('receita_centavos')))
