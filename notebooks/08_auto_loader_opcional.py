# Databricks notebook source

# MAGIC %md
# MAGIC # 08 · Lab Bricks / Auto Loader com arquivos próprios
# MAGIC **Opcional, exige Unity Catalog, volume e suporte a Auto Loader na sua conta.** Cria um volume gerenciado somente no schema de estudo e arquivos JSON fictícios. Não apaga checkpoints nem arquivos.
# MAGIC O trigger availableNow processa o disponível e termina. Consulte o guia antes de executar.

# COMMAND ----------

# MAGIC %run ./00_configuracao

# COMMAND ----------

import json
from pyspark.sql.types import StructType, StructField, StringType

VOLUME = 'entrada_lab_bricks'
spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOG_SQL}.{SCHEMA_SQL}.`{VOLUME}`")
BASE_VOLUME = f'/Volumes/{CATALOG}/{SCHEMA}/{VOLUME}'
ENTRADA = BASE_VOLUME + '/entrada'
CHECKPOINT = BASE_VOLUME + '/checkpoint_vendas'
dbutils.fs.mkdirs(ENTRADA)
existentes = {file.name for file in dbutils.fs.ls(ENTRADA)}
source_rows = gerar_vendas(90, False, 42)
for index, subset in enumerate([source_rows[:5], source_rows[5:10]], 1):
    filename = f'lote_{index:03d}.json'
    if filename not in existentes:
        dbutils.fs.put(ENTRADA + '/' + filename, '\n'.join(json.dumps(row, ensure_ascii=False) for row in subset) + '\n', overwrite=False)
json_schema = StructType([StructField(name, StringType(), True) for name in COLUNAS])

# COMMAND ----------

stream = (spark.readStream.format('cloudFiles')
          .option('cloudFiles.format', 'json')
          .schema(json_schema)
          .load(ENTRADA))
run = (stream.writeStream.format('delta')
       .option('checkpointLocation', CHECKPOINT)
       .trigger(availableNow=True)
       .toTable(tabela('bronze_auto_loader')))
run.awaitTermination()
received = spark.table(tabela('bronze_auto_loader'))
assert received.count() == 10, 'O fixture espera somente os dois arquivos próprios; investigue se acrescentou outros.'
display(received)
print({'linhas': received.count(), 'stream_ativo': run.isActive, 'checkpoint': CHECKPOINT})

# COMMAND ----------

# MAGIC %md
# MAGIC ## Reexecute sem apagar estado
# MAGIC Os mesmos nomes de arquivos não são sobrescritos, e o mesmo checkpoint deve evitar reingestão. A contagem continua dez enquanto apenas esses dois arquivos estiverem na entrada. Para uma nova origem, planeje um novo checkpoint/destino de estudo; não apague estado para “consertar” um fluxo.
# MAGIC O exercício é append-only. Correções de pedidos exigem chave/versionamento e MERGE adicional; o checkpoint não resolve sozinho a semântica de atualização. Valide permissões de volume e comportamento real na sua conta.
