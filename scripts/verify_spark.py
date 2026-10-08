"""Compara a função real do notebook 00 com as regras locais, sem Delta ou conta."""
import ast
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lab.dados import COLUNAS, gerar_vendas
from lab.pipeline import tratar
from lab.bi import gerar_comercio, resumo, CONSULTAS
from lab.retail_real import carregar_amostra, limpar_retail, gold_retail
import json


def verificar():
    from pyspark.sql import SparkSession, Window, functions as F

    source = ast.parse((ROOT / "notebooks/00_configuracao.py").read_text())
    functions = [node for node in source.body if isinstance(node, ast.FunctionDef)
                 and node.name == "normalizar"]
    if len(functions) != 1:
        raise RuntimeError("Funções de transformação não encontradas no notebook.")
    with TemporaryDirectory(prefix="lab-bricks-spark-") as temporary:
        spark = (SparkSession.builder.master("local[2]").appName("lab-bricks-verificacao")
                 .config("spark.ui.enabled", "false")
                 .config("spark.driver.host", "127.0.0.1")
                 .config("spark.sql.shuffle.partitions", "2")
                 .config("spark.sql.session.timeZone", "UTC")
                 .config("spark.sql.execution.arrow.pyspark.enabled", "true")
                 .config("spark.sql.execution.arrow.pyspark.fallback.enabled", "false")
                 .config("spark.sql.warehouse.dir", str(Path(temporary) / "warehouse"))
                 .getOrCreate())
        spark.sparkContext.setLogLevel("ERROR")
        try:
            namespace = {"spark": spark, "F": F, "Window": Window,
                         "COLUNAS": COLUNAS, "gerar_vendas": gerar_vendas}
            exec(compile(ast.Module(body=functions, type_ignores=[]), "notebook_00", "exec"), namespace)
            default = gerar_vendas()
            base = gerar_vendas(n=90, sujeira=False)[0]
            nulls = [{**base, "venda_id": f"N{i}", campo: None}
                     for i, campo in enumerate(COLUNAS)]
            versions = [base, {**base, "quantidade": "0", "atualizado_em": "2026-04-01 12:00:00"},
                        {**base, "venda_id": "EMPATE", "quantidade": "2"},
                        {**base, "venda_id": "EMPATE", "quantidade": "4"}]
            cases = [default, list(reversed(default)), nulls + versions]
            schema = ", ".join(f"{col} STRING" for col in COLUNAS) + ", _ordem LONG"
            for rows in cases:
                values = [tuple(row[col] for col in COLUNAS) + (i,) for i, row in enumerate(rows)]
                # Arrow envia a fonte para a JVM; o teste exercita as expressões Spark.
                bronze = spark.createDataFrame(pd.DataFrame(values, columns=COLUNAS + ["_ordem"]), schema=schema)
                silver, rejected, superseded = namespace["normalizar"](bronze)
                local = tratar(rows)
                actual_silver = silver.toPandas()
                actual_rejected = rejected.toPandas()
                actual_superseded = superseded.toPandas()

                def snapshot(frame, columns):
                    return sorted(tuple(str(value) for value in row)
                                  for row in frame[columns].itertuples(index=False, name=None))

                columns = ["venda_id", "data_venda", "quantidade", "status", "preco_centavos", "valor_centavos"]
                assert snapshot(actual_silver, columns) == snapshot(local.silver, columns), "Silver divergiu"
                assert snapshot(actual_rejected, COLUNAS + ["motivo"]) == snapshot(local.rejeitadas, COLUNAS + ["motivo"]), "Quarentena divergiu"
                assert snapshot(actual_superseded, COLUNAS) == snapshot(local.substituidas, COLUNAS), "Versões divergiu"
                assert len(rows) == len(actual_silver) + len(actual_rejected) + len(actual_superseded)
            # Exercita a função real do notebook JSON, sem copiar a implementação.
            json_source = ast.parse((ROOT / 'notebooks/06_json_e_qualidade.py').read_text())
            json_functions = [node for node in json_source.body if isinstance(node, ast.FunctionDef) and node.name == 'construir_json']
            from pyspark.sql import types as T
            json_namespace = {'spark': spark, 'F': F, 'T': T, 'pd': pd}
            exec(compile(ast.Module(body=json_functions, type_ignores=[]), 'notebook_06', 'exec'), json_namespace)
            raw, rejected_events, items, rejected_items = json_namespace['construir_json'](spark)
            assert (raw.count(), rejected_events.count(), items.count(), rejected_items.count()) == (4, 2, 3, 0)
            assert items.agg(F.sum('valor_centavos')).first()[0] == 17600
            # Valida SQL/joins/janela do BI em Spark, sem substituir o teste Delta.
            tables = gerar_comercio()
            for name, frame in tables.items():
                spark.createDataFrame(frame).createOrReplaceTempView(name)
            counts_bi = spark.sql(CONSULTAS['Grão: linhas versus pedidos']).first().asDict()
            expected = resumo(tables)
            assert counts_bi == {'linhas': expected['linhas'], 'pedidos': expected['pedidos']}
            window_rows = spark.sql(CONSULTAS['Receita acumulada com janela']).collect()
            assert abs(float(window_rows[-1]['acumulada']) - expected['receita_centavos'] / 100) < 1e-6
            # Gold público: mesma moeda, mesmo total e tipos inteiros no Spark.
            silver_real, _, _, counts = limpar_retail(carregar_amostra(ROOT/'data'))
            gold = gold_retail(silver_real)
            structure = 'dia STRING, venda_bruta_centavos LONG, estorno_centavos LONG, receita_liquida_centavos LONG, linhas LONG'
            # Arrow evita o caminho PythonRDD e mantém os tipos explícitos.
            native_gold = spark.createDataFrame(gold,structure)
            assert native_gold.agg(F.sum('receita_liquida_centavos')).first()[0] == 5682033
            assert counts['entrada'] == counts['silver'] + counts['rejeitadas'] + counts['substituidas']
            # Streaming nativo: um arquivo por trigger, preservando o checkpoint.
            base_stream = Path(temporary)/'stream';input_dir=base_stream/'input';input_dir.mkdir(parents=True)
            output_dir=base_stream/'output';checkpoint=base_stream/'checkpoint'
            stream=(spark.readStream.schema('evento_id STRING, instante TIMESTAMP, valor DOUBLE').json(str(input_dir)).withWatermark('instante','10 minutes').groupBy(F.window('instante','5 minutes')).agg(F.sum('valor').alias('valor'),F.count('*').alias('eventos')))
            def trigger():
                query=(stream.writeStream.format('parquet').outputMode('append').option('checkpointLocation',str(checkpoint)).trigger(availableNow=True).start(str(output_dir)))
                if not query.awaitTermination(120):
                    query.stop();raise RuntimeError('Streaming local excedeu dois minutos.')
                if query.exception() is not None:raise RuntimeError(str(query.exception()))
            def event(key,time,value):return {'evento_id':key,'instante':f'2026-01-01T{time}:00','valor':float(value)}
            batches=[[event('a','10:02',10),event('b','10:20',20)],
                     [event('c','10:12',12),event('tardio','10:02',99),event('d','10:30',30)],
                     [event('e','10:50',50)]]
            for i,batch in enumerate(batches):
                (input_dir/f'{i:02d}.json').write_text('\n'.join(json.dumps(row) for row in batch)+'\n')
                trigger()
            trigger()
            before=spark.read.parquet(str(output_dir)).orderBy('window').collect()
            assert sum(float(row.valor) for row in before)==72.0
            assert sum(float(row.valor) for row in before if row.window.start.minute==0)==10.0
            trigger()
            after=spark.read.parquet(str(output_dir)).orderBy('window').collect()
            assert before==after,'Replay do checkpoint alterou o resultado'
            print(f"Spark {spark.version}: 7 cenários validados: pipeline (3), JSON, BI, Gold público e streaming com replay de checkpoint. Delta e conta Databricks não executados.")
        finally:
            spark.stop()


if __name__ == "__main__":
    verificar()
