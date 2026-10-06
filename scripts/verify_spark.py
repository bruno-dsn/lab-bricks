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


def verificar():
    from pyspark.sql import SparkSession, Window, functions as F

    source = ast.parse((ROOT / "notebooks/00_configuracao.py").read_text())
    functions = [node for node in source.body if isinstance(node, ast.FunctionDef)
                 and node.name == "normalizar"]
    if len(functions) != 1:
        raise RuntimeError("Funções de transformação não encontradas no notebook.")
    with TemporaryDirectory(prefix="dbnp-spark-") as temporary:
        spark = (SparkSession.builder.master("local[2]").appName("dbnp-verificacao")
                 .config("spark.ui.enabled", "false")
                 .config("spark.driver.host", "127.0.0.1")
                 .config("spark.sql.shuffle.partitions", "2")
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
            print(f"Spark {spark.version}: 3 cenários reconciliados com Pandas, incluindo nulos e versões. Delta e Unity Catalog não foram executados.")
        finally:
            spark.stop()


if __name__ == "__main__":
    verificar()
