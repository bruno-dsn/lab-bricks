# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # 02 · Um lakehouse de vendas
# MAGIC **Pergunta:** quanto a loja vendeu por dia e quais registros não podemos usar?
# MAGIC 
# MAGIC Este projeto cria snapshots pequenos em tabelas Delta. Bronze é a fonte intacta; Silver tem a versão vigente e validada; Gold resume a regra de negócio. A quarentena conserva os motivos de rejeição. Isso é um exercício batch, não uma implementação de streaming.

# COMMAND ----------

# MAGIC %run ./00_configuracao

# COMMAND ----------

bronze = fonte()
bronze.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(tabela("bronze_vendas"))
display(spark.table(tabela("bronze_vendas")).limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Transformar sem perder a explicação
# MAGIC Chamamos `normalizar`, definida no 00. Preços têm no máximo duas casas decimais; quantidades são inteiros de 1 a 1.000. Cancelamento é um status válido. Uma chave só pode ter uma versão na Silver.

# COMMAND ----------

silver, rejeitadas, substituidas = normalizar(spark.table(tabela("bronze_vendas")))
for nome, frame in [("silver_vendas", silver), ("quarentena_vendas", rejeitadas), ("versoes_substituidas", substituidas)]:
    frame.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(tabela(nome))
display(rejeitadas)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Dar uma forma útil para a análise
# MAGIC Gold considera somente pedidos concluídos. O valor do pedido é `quantidade × preço`. Receita não é lucro: não incluímos custo, frete, impostos ou margem neste dataset.

# COMMAND ----------

gold = (silver.where("status = 'concluida'").groupBy("data_venda")
        .agg(F.count("venda_id").alias("pedidos"), F.sum("valor_centavos").alias("receita_centavos"))
        .withColumn("receita", F.col("receita_centavos") / 100)
        .withColumn("ticket_medio", F.col("receita") / F.col("pedidos")))
gold.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(tabela("gold_diario"))
display(gold.orderBy("data_venda"))

# COMMAND ----------

counts = {"bronze": bronze.count(), "silver": silver.count(), "rejeitadas": rejeitadas.count(), "substituidas": substituidas.count()}
assert counts == {"bronze": 727, "silver": 720, "rejeitadas": 6, "substituidas": 1}, counts
assert counts["bronze"] == sum(counts[k] for k in ["silver", "rejeitadas", "substituidas"])
assert silver.groupBy("venda_id").count().where("count > 1").count() == 0
assert gold.agg(F.sum("receita_centavos")).first()[0] == silver.where("status = 'concluida'").agg(F.sum("valor_centavos")).first()[0]
print(counts)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Criar um painel na sua conta
# MAGIC No editor SQL, escolha o catálogo exibido pelo notebook e seu schema `dbnp_...`. Execute `SELECT * FROM gold_diario ORDER BY data_venda` e crie uma visualização de receita por dia. Salve a consulta em um dashboard disponível no seu workspace.
# MAGIC 
# MAGIC O painel local do repositório ajuda a experimentar as mesmas métricas. Ele não é uma captura de tela do Databricks.
# MAGIC 
# MAGIC **Desafio:** inclua uma regra para canais autorizados. Adicione uma linha com um canal desconhecido e explique por que ela foi rejeitada.
