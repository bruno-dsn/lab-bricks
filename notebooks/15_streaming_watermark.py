# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # Watermark e replay de checkpoint
# MAGIC 
# MAGIC O operador nativo usa agregação por janela, saída append e sink Delta. Não pressupõe descarte idêntico ao simulador por timestamp individual. Cada arquivo só entra depois do trigger anterior terminar; a ordem não depende de mtime igual.

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

lotes = [[{'evento_id':'a','instante':'2026-01-01T10:20:00Z','valor':20}], [{'evento_id':'b','instante':'2026-01-01T10:02:00Z','valor':99}], []]
audit, janelas = simular_watermark(lotes)
display(audit)
display(janelas)

# COMMAND ----------

import json, re, uuid
from pathlib import PurePosixPath
from pyspark.sql import functions as F
dbutils.widgets.text('executar_streaming','nao')
dbutils.widgets.text('volume_raiz','')
if dbutils.widgets.get('executar_streaming') == 'sim':
    volume = dbutils.widgets.get('volume_raiz').rstrip('/')
    if not re.fullmatch(r'/Volumes/[A-Za-z0-9_-]+/[A-Za-z0-9_-]+/[A-Za-z0-9_-]+', volume):
        raise ValueError('Informe um Volume dedicado no formato /Volumes/catalogo/schema/volume.')
    base = volume + '/lab_bricks_' + uuid.uuid4().hex
    entrada, saida, checkpoint = [base+'/'+x for x in ('entrada','saida','checkpoint')]
    dbutils.fs.mkdirs(entrada)
    esquema = 'evento_id STRING, instante TIMESTAMP, valor DOUBLE'
    stream = (spark.readStream.schema(esquema).json(entrada).withWatermark('instante','10 minutes').groupBy(F.window('instante','5 minutes')).agg(F.sum('valor').alias('valor'),F.count('*').alias('eventos')))
    def executar_trigger():
        query = stream.writeStream.format('delta').outputMode('append').option('checkpointLocation',checkpoint).trigger(availableNow=True).start(saida)
        if not query.awaitTermination(120):
            query.stop()
            raise RuntimeError('Trigger excedeu dois minutos; registre a falha.')
        if query.exception() is not None:raise RuntimeError(str(query.exception()))
    lotes = [
      [{'evento_id':'a','instante':'2026-01-01T10:02:00','valor':10.0},{'evento_id':'b','instante':'2026-01-01T10:20:00','valor':20.0}],
      [{'evento_id':'c','instante':'2026-01-01T10:12:00','valor':12.0},{'evento_id':'tardio','instante':'2026-01-01T10:02:00','valor':99.0},{'evento_id':'d','instante':'2026-01-01T10:30:00','valor':30.0}],
      [{'evento_id':'e','instante':'2026-01-01T10:50:00','valor':50.0}],
    ]
    for i,lote in enumerate(lotes):
        conteudo = '\n'.join(json.dumps(r) for r in lote)+'\n'
        dbutils.fs.put(f'{entrada}/{i:02d}.json',conteudo,False)
        executar_trigger()
    executar_trigger()
    antes = spark.read.format('delta').load(saida).orderBy('window').collect()
    executar_trigger()  # Mesmo checkpoint, sem regravar arquivos: replay vazio.
    depois = spark.read.format('delta').load(saida).orderBy('window').collect()
    assert antes == depois
    assert sum(float(r.valor) for r in depois if r.window.start.hour==10 and r.window.start.minute==0) == 10.0
    display(spark.read.format('delta').load(saida))
    print('Guarde os caminhos e o checkpoint para sua evidência:',base)
else:
    print('Streaming nativo não executado. Ative na sua conta e registre a evidência.')


# COMMAND ----------

# MAGIC %md
# MAGIC ## Desafio
# MAGIC 
# MAGIC Compare um evento antes da fronteira com uma janela que ainda termina depois dela. Explique replay do checkpoint versus deduplicação de IDs. Não apague o checkpoint para simular um teste que não ocorreu.
