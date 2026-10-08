# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # CDC, SCD2 e MERGE sobre snapshot completo
# MAGIC 
# MAGIC A referência local reconstrói o log completo. A opção Delta só escreve uma tabela dedicada marcada como demonstração. Fonte completa e reconstrução de intervalos são requisitos; isto não é um MERGE de CDC de produção.

# COMMAND ----------

"""Referências limitadas em Pandas: histórico CDC e watermark por microbatch."""
import math
import pandas as pd


def historico_scd2(eventos):
    if not isinstance(eventos, list) or not 1 <= len(eventos) <= 1000:
        raise ValueError('Use um log completo de até 1.000 eventos.')
    known, rows, audit, unique = {}, [], [], []
    for item in eventos:
        if not isinstance(item, dict) or set(item) != {'evento_id', 'chave', 'instante', 'operacao', 'valor'} or not all(isinstance(item[k], str) and 1 <= len(item[k]) <= 128 for k in ('evento_id', 'chave')) or not isinstance(item['instante'],str) or not 1<=len(item['instante'])<=60 or not isinstance(item['operacao'],str) or item['operacao'] not in {'upsert', 'delete'}:
            raise ValueError('Contrato CDC inválido.')
        if item['operacao'] == 'upsert' and (not isinstance(item['valor'], str) or not 1 <= len(item['valor']) <= 128):
            raise ValueError('Valor de upsert precisa ser textual.')
        if item['operacao']=='delete' and item['valor'] is not None:
            raise ValueError('Delete deve declarar valor nulo.')
        row = {**item, 'instante': pd.to_datetime(item['instante'], utc=True, errors='raise')}
        if pd.isna(row['instante']):
            raise ValueError('Instante CDC ausente.')
        if row['evento_id'] in known:
            if known[row['evento_id']] != row:
                raise ValueError('Mesmo ID CDC com conteúdo divergente.')
            audit.append({'evento_id': row['evento_id'], 'resultado': 'replay'})
        else:
            known[row['evento_id']] = row; unique.append(row)
    if pd.DataFrame(unique).duplicated(['chave', 'instante']).any():
        raise ValueError('Duas alterações da mesma chave no mesmo instante são ambíguas.')
    active = {}
    for row in sorted(unique, key=lambda x: (x['instante'], x['chave'], x['evento_id'])):
        current = active.get(row['chave'])
        if current is not None and row['operacao'] == 'upsert' and rows[current]['valor'] == row['valor']:
            audit.append({'evento_id': row['evento_id'], 'resultado': 'sem_alteracao'});continue
        if current is not None:
            rows[current].update(fim=row['instante'], atual=False)
            del active[row['chave']]
        if row['operacao'] == 'upsert':
            active[row['chave']] = len(rows)
            rows.append({'evento_id': row['evento_id'], 'chave': row['chave'], 'valor': row['valor'],
                         'inicio': row['instante'], 'fim': pd.NaT, 'atual': True})
        audit.append({'evento_id': row['evento_id'], 'resultado': row['operacao']})
    return pd.DataFrame(rows, columns=['evento_id', 'chave', 'valor', 'inicio', 'fim', 'atual']), pd.DataFrame(audit)


def simular_watermark(lotes, atraso_minutos=10, janela_minutos=5):
    if not isinstance(lotes, list) or not 1 <= len(lotes) <= 20 or any(not isinstance(b, list) for b in lotes) or sum(map(len, lotes)) > 1000:
        raise ValueError('Use até 20 lotes e 1.000 eventos no total.')
    if any(type(x) is not int or not 1 <= x <= 60 for x in (atraso_minutos, janela_minutos)):
        raise ValueError('Durações precisam ser inteiras entre 1 e 60 minutos.')
    maximum, seen, windows, audit = None, {}, {}, []
    for batch_index, batch in enumerate(lotes):
        frontier = maximum - pd.Timedelta(minutes=atraso_minutos) if maximum is not None else None
        for state in windows.values():
            if frontier is not None and state['fim'] <= frontier:
                state['estado'] = 'finalizada'
        batch_times = []
        for row in batch:
            if not isinstance(row, dict) or set(row) != {'evento_id', 'instante', 'valor'} or not isinstance(row['evento_id'], str) or not 1 <= len(row['evento_id']) <= 128 or not isinstance(row['instante'],str) or not 1<=len(row['instante'])<=60 or not isinstance(row['valor'], (int, float)) or isinstance(row['valor'], bool) or not math.isfinite(row['valor']):
                raise ValueError('Evento fora do contrato streaming.')
            instant = pd.to_datetime(row['instante'], utc=True, errors='raise')
            if pd.isna(instant):
                raise ValueError('Instante ausente.')
            batch_times.append(instant)
            identity = (instant, row['valor'])
            if row['evento_id'] in seen:
                if seen[row['evento_id']] != identity:
                    raise ValueError('ID streaming repetido com conteúdo divergente.')
                status = 'duplicado'
            elif frontier is not None and instant <= frontier:
                status = 'atrasado'
            else:
                status = 'aceito';seen[row['evento_id']] = identity
                start = instant.floor(f'{janela_minutos}min')
                state = windows.setdefault(start, {'inicio': start, 'fim': start + pd.Timedelta(minutes=janela_minutos), 'valor': 0., 'eventos': 0, 'estado': 'aberta'})
                state['valor'] += row['valor'];state['eventos'] += 1
            audit.append({'lote': batch_index, 'evento_id': row['evento_id'], 'instante': instant, 'watermark_anterior': frontier, 'resultado': status})
        if batch_times:
            maximum = max([*batch_times, *([] if maximum is None else [maximum])])
    return pd.DataFrame(audit), pd.DataFrame(sorted(windows.values(), key=lambda x: x['inicio']), columns=['inicio','fim','valor','eventos','estado'])

# COMMAND ----------

eventos = [
 {'evento_id':'e1','chave':'cliente-A','instante':'2026-01-01','operacao':'upsert','valor':'Norte'},
 {'evento_id':'e3','chave':'cliente-A','instante':'2026-01-03','operacao':'upsert','valor':'Sul'},
 {'evento_id':'e2','chave':'cliente-A','instante':'2026-01-02','operacao':'upsert','valor':'Centro'}
]
historico, auditoria = historico_scd2(eventos + [eventos[0].copy()])
assert historico.valor.tolist() == ['Norte','Centro','Sul']
assert historico.atual.sum() == 1
display(historico)
display(auditoria)

# COMMAND ----------

import re
from delta.tables import DeltaTable
from pyspark.sql import types as T
dbutils.widgets.text('executar_delta','nao')
dbutils.widgets.text('catalogo','workspace')
dbutils.widgets.text('schema_estudo','lab_bricks')
if dbutils.widgets.get('executar_delta') == 'sim':
    catalogo, esquema = [dbutils.widgets.get(k) for k in ('catalogo','schema_estudo')]
    if not all(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]{0,62}',x) for x in (catalogo,esquema)):
        raise ValueError('Catálogo ou schema inválidos.')
    tabela = f'{catalogo}.{esquema}.lb_escola_scd2'
    spark.conf.set('spark.sql.session.timeZone','UTC')
    estrutura = 'evento_id STRING, chave STRING, valor STRING, inicio TIMESTAMP, fim TIMESTAMP, atual BOOLEAN'
    linhas = [(r.evento_id,r.chave,r.valor,r.inicio.to_pydatetime().replace(tzinfo=None),None if pd.isna(r.fim) else r.fim.to_pydatetime().replace(tzinfo=None),bool(r.atual)) for r in historico.itertuples()]
    snapshot = spark.createDataFrame(linhas,estrutura)
    if not spark.catalog.tableExists(tabela):
        snapshot.write.format('delta').mode('errorifexists').saveAsTable(tabela)
        spark.sql(f"ALTER TABLE {tabela} SET TBLPROPERTIES ('lab_bricks.demo'='scd2')")
    propriedades = {r.key:r.value for r in spark.sql(f'SHOW TBLPROPERTIES {tabela}').collect()}
    if propriedades.get('lab_bricks.demo') != 'scd2':
        raise ValueError('Tabela sem marca de estudo; operação cancelada.')
    (DeltaTable.forName(spark,tabela).alias('t').merge(snapshot.alias('s'),'t.chave=s.chave AND t.inicio=s.inicio').whenMatchedUpdateAll().whenNotMatchedInsertAll().whenNotMatchedBySourceDelete().execute())
    assert spark.table(tabela).count() == len(historico)
    display(spark.table(tabela).orderBy('chave','inicio'))
else:
    print('MERGE Delta não executado. Ative explicitamente apenas na tabela de estudo.')

# COMMAND ----------

# MAGIC %md
# MAGIC ## Evidência
# MAGIC 
# MAGIC Repita o snapshot, simule delete e reconstrua a junção temporal. Registre as métricas do MERGE e o ID da execução real. O registro permanece pendente até essa evidência existir.
