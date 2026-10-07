# Databricks notebook source

# MAGIC %md
# MAGIC # 07 · Lab Bricks / gate de qualidade para Jobs
# MAGIC Execute depois do notebook 02. Lê somente suas tabelas e não cria nem apaga registros. Contagens fixas são do fixture padrão.

# COMMAND ----------

# MAGIC %run ./00_configuracao

# COMMAND ----------

bronze_check = spark.table(tabela('bronze_vendas'))
silver_check = spark.table(tabela('silver_vendas'))
quarantine_check = spark.table(tabela('quarentena_vendas'))
superseded_check = spark.table(tabela('versoes_substituidas'))
gold_check = spark.table(tabela('gold_diario'))
counts = {'bronze': bronze_check.count(), 'silver': silver_check.count(), 'rejeitadas': quarantine_check.count(), 'substituidas': superseded_check.count()}
assert counts == {'bronze': 727, 'silver': 720, 'rejeitadas': 6, 'substituidas': 1}, counts
assert counts['bronze'] == counts['silver'] + counts['rejeitadas'] + counts['substituidas']
assert silver_check.groupBy('venda_id').count().where('count > 1').count() == 0
assert silver_check.where("valor_centavos IS NULL OR valor_centavos <= 0").count() == 0
assert gold_check.agg(F.sum('receita_centavos')).first()[0] == silver_check.where("status='concluida'").agg(F.sum('valor_centavos')).first()[0]
print({'qualidade': 'aprovada', **counts})

# COMMAND ----------

# MAGIC %md
# MAGIC Se um assert falhar, a tarefa falha e uma tarefa dependente de sucesso não deve publicar resultados como válidos. Preserve evidência e investigue contrato/fonte antes de aplicar retry. Não ajuste as contagens só para esconder um problema.
