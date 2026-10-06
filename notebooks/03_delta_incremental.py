# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # 03 · Reprocessar sem duplicar
# MAGIC O primeiro pipeline substituía um snapshot completo. Agora vamos simular um lote com uma alteração e um pedido novo, usando `MERGE` em uma **tabela separada de estudo**.
# MAGIC 
# MAGIC Este notebook restaura a tabela `silver_incremental` a partir da Silver antes de demonstrar o lote. Reexecutar somente a célula do MERGE é o teste de idempotência.

# COMMAND ----------

# MAGIC %run ./00_configuracao

# COMMAND ----------

base = spark.table(tabela("silver_vendas"))
base.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(tabela("silver_incremental"))
original = base.where("venda_id = 'V000001'")
assert original.count() == 1, "Execute o notebook 02 primeiro."
changes = (original.withColumn("quantidade", F.col("quantidade") + 3)
           .withColumn("valor_centavos", F.col("quantidade") * F.col("preco_centavos"))
           .withColumn("atualizado_em", F.lit("2026-05-01 10:00:00").cast("timestamp")))
novo = changes.withColumn("venda_id", F.lit("NOVO0001"))
lote = changes.unionByName(novo)
assert lote.groupBy("venda_id").count().where("count > 1").count() == 0
lote.createOrReplaceTempView("lote_incremental")
version_before = spark.sql(f"DESCRIBE HISTORY {tabela('silver_incremental')}").select("version").first()[0]

# COMMAND ----------

# MAGIC %md
# MAGIC ## A chave diz qual pedido; a data diz qual versão
# MAGIC O lote foi construído com as mesmas colunas e os mesmos tipos da Silver. Num pipeline real, aplique o contrato e a deduplicação antes do MERGE. Uma origem com várias versões da mesma chave pode tornar a atualização ambígua.

# COMMAND ----------

merge_sql = f"""
MERGE INTO {tabela('silver_incremental')} AS destino
USING lote_incremental AS origem
ON destino.venda_id = origem.venda_id
WHEN MATCHED AND origem.atualizado_em > destino.atualizado_em THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
"""
spark.sql(merge_sql)
after_first = spark.table(tabela("silver_incremental"))
# materializar a comparação antes de executar outra operação na tabela
snapshot = after_first.toPandas().sort_values("venda_id").reset_index(drop=True)
spark.sql(merge_sql)
after_second = spark.table(tabela("silver_incremental")).toPandas().sort_values("venda_id").reset_index(drop=True)
assert snapshot.equals(after_second), "Reprocessar mudou o conteúdo."
assert len(after_second) == base.count() + 1
print("O lote entrou uma vez, mesmo com duas execuções.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Consultar o histórico
# MAGIC Delta mantém versões associadas às operações. A versão anterior abaixo depende da retenção de logs e arquivos; time travel não substitui uma política de backup. Não executamos VACUUM nem removemos dados neste laboratório.

# COMMAND ----------

display(spark.sql(f"DESCRIBE HISTORY {tabela('silver_incremental')}").select("version", "timestamp", "operation"))
antes = spark.read.option("versionAsOf", version_before).table(tabela("silver_incremental"))
assert antes.count() == base.count()
display(antes.where("venda_id = 'V000001'"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercício
# MAGIC Troque a atualização do lote por uma data mais antiga. A versão vigente deve permanecer intacta. Em seguida, tente criar duas versões do mesmo ID na origem e confirme que a validação bloqueia o lote antes do MERGE.
# MAGIC 
# MAGIC A Gold do notebook 02 continua representando a Silver original. Para transformar este exemplo numa ingestão contínua, é necessário aplicar o MERGE na tabela oficial do pipeline e atualizar a Gold depois, mantendo testes de reconciliação.
