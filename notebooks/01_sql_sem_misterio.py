# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # 01 · SQL: da linha à resposta
# MAGIC **Objetivo:** calcular receita, quantidade de pedidos e ticket médio, sem incluir cancelamentos.
# MAGIC 
# MAGIC Importe também `00_configuracao` para a mesma pasta. Quando o `%run` terminar, confirme que o widget `catalogo` aponta para o espaço escolhido. Todos os notebooks devem usar o mesmo catálogo.

# COMMAND ----------

# MAGIC %run ./00_configuracao

# COMMAND ----------

vendas, _, _ = normalizar(fonte(sujeira=False))
vendas.createOrReplaceTempView("vendas_exemplo")
display(vendas.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Primeiro filtre; depois agregue
# MAGIC `WHERE` escolhe os pedidos concluídos. `SUM` soma os centavos desses pedidos. Dividir por 100 converte a unidade para reais. Aqui cada registro é um pedido, por isso `COUNT(*)` conta pedidos.

# COMMAND ----------

display(spark.sql("""
SELECT canal,
       COUNT(*) AS pedidos,
       SUM(valor_centavos) / 100.0 AS receita,
       ROUND(SUM(valor_centavos) / 100.0 / COUNT(*), 2) AS ticket_medio
FROM vendas_exemplo
WHERE status = 'concluida'
GROUP BY canal
ORDER BY receita DESC
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Um teste para a definição da métrica
# MAGIC A receita por canal precisa reconciliar com a soma dos pedidos concluídos. Alterar a consulta é permitido; alterar a definição da receita exige discutir a regra de negócio.

# COMMAND ----------

total = spark.sql("SELECT SUM(valor_centavos) AS total FROM vendas_exemplo WHERE status = 'concluida'").first()["total"]
por_canal = spark.sql("SELECT canal, SUM(valor_centavos) AS total FROM vendas_exemplo WHERE status = 'concluida' GROUP BY canal")
assert por_canal.agg(F.sum("total")).first()[0] == total
print("Receita reconciliada.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercício
# MAGIC Calcule unidades vendidas por produto. Depois escreva uma consulta para a taxa de cancelamento: pedidos cancelados divididos pelo total de pedidos. Explique por que esse denominador é diferente do usado no ticket médio.
# MAGIC 
# MAGIC O gabarito está em `docs/SOLUCOES.md`. Uma consulta correta para este exercício deve incluir zero cancelamentos de receita e manter os cancelados no cálculo da taxa.
