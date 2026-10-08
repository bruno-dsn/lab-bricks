# Databricks notebook source

# COMMAND ----------

# MAGIC %md
# MAGIC # Caso público UCI Online Retail
# MAGIC 
# MAGIC Faça primeiro a configuração. Disponibilize o projeto completo em Workspace/Git folder ou Volume e informe projeto_dir. Este notebook usa a amostra pública incluída, sem CustomerID. Não escreva que rodou na conta sem guardar a evidência.

# COMMAND ----------

import re
from pathlib import Path
dbutils.widgets.text('projeto_dir', '')
projeto_dir = dbutils.widgets.get('projeto_dir')
if not re.fullmatch(r'/(?:Workspace|Volumes)/[A-Za-z0-9@._ /-]{1,240}', projeto_dir) or '..' in Path(projeto_dir).parts:
    raise ValueError('Informe a pasta do projeto em /Workspace ou /Volumes, com content/ e data/.')
PROJETO = Path(projeto_dir)


# COMMAND ----------

"""Contrato e reconciliação de linhas públicas do UCI Online Retail, em GBP."""
from pathlib import Path
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hashlib
import json
import pandas as pd

COLUNAS = ['linha_fonte', 'fatura', 'produto', 'descricao', 'quantidade', 'data', 'preco_gbp', 'pais']
SILVER = COLUNAS + ['preco_centavos', 'valor_centavos']
GOLD = ['dia', 'venda_bruta_centavos', 'estorno_centavos', 'receita_liquida_centavos', 'linhas']


def carregar_amostra(directory):
    directory = Path(directory)
    path = directory / 'online_retail_amostra.csv'
    meta = json.loads((directory / 'online_retail_meta.json').read_text())
    if path.is_symlink() or path.stat().st_size > 2_000_000:
        raise ValueError('Amostra fora do contrato.')
    if hashlib.sha256(path.read_bytes()).hexdigest() != meta['amostra_sha256']:
        raise ValueError('Amostra diverge da proveniência registrada.')
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def _normalizar(row):
    out = dict(row)
    for key in ('fatura', 'produto', 'descricao', 'pais'):
        value = row[key]
        if pd.isna(value) or not str(value).strip() or str(value).strip().casefold() in {'nan', 'none', 'null', '<na>'}:
            raise ValueError(f'{key}_ausente')
        out[key] = str(value).strip()
    try:
        quantity = Decimal(str(row['quantidade']))
        price = Decimal(str(row['preco_gbp']))
        if not quantity.is_finite() or quantity != quantity.to_integral_value() or quantity == 0 or abs(quantity) > 1_000_000:
            raise ValueError('quantidade_invalida')
        if not price.is_finite() or not 0 < price <= 1_000_000:
            raise ValueError('preco_invalido')
        cents = int((price * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
        if cents <= 0:
            raise ValueError('preco_arredonda_zero')
    except (InvalidOperation, TypeError):
        raise ValueError('numero_invalido') from None
    try:
        # Cada linha é interpretada sozinha: aceita ISO e dia/mês/ano.
        raw = row['data']
        if pd.isna(raw) or not str(raw).strip():
            raise ValueError
        dayfirst = '/' in str(raw)
        instant = pd.to_datetime(raw, dayfirst=dayfirst, errors='raise')
        if pd.isna(instant) or instant.tzinfo is not None:
            raise ValueError
    except (ValueError, TypeError, OverflowError):
        raise ValueError('data_invalida') from None
    qty = int(quantity)
    if out['fatura'].upper().startswith('C') != (qty < 0):
        raise ValueError('sinal_cancelamento_inconsistente')
    out.update(quantidade=qty, data=instant, preco_gbp=str(price.normalize()), preco_centavos=cents, valor_centavos=cents * qty)
    return out


def limpar_retail(bronze):
    if not isinstance(bronze, pd.DataFrame) or list(bronze.columns) != COLUNAS or not 1 <= len(bronze) <= 10_000:
        raise ValueError('Contrato Bronze inválido: oito colunas ordenadas e até 10.000 linhas.')
    if bronze.linha_fonte.isna().any() or bronze.linha_fonte.astype(str).str.strip().eq('').any() or bronze.linha_fonte.duplicated().any():
        raise ValueError('Identificador da linha de origem precisa ser único e preenchido.')
    good, rejected, replaced, seen = [], [], [], set()
    for row in bronze.to_dict('records'):
        try:
            normalized = _normalizar(row)
        except ValueError as error:
            rejected.append({**row, 'motivo': str(error)})
            continue
        # Chave de negócio não basta: um produto pode aparecer duas vezes legitimamente.
        fingerprint = tuple(str(normalized[k]) for k in COLUNAS if k != 'linha_fonte')
        if fingerprint in seen:
            replaced.append({**row, 'motivo': 'linha_identica'})
        else:
            seen.add(fingerprint)
            good.append(normalized)
    silver = pd.DataFrame(good, columns=SILVER)
    rejected = pd.DataFrame(rejected, columns=COLUNAS + ['motivo'])
    replaced = pd.DataFrame(replaced, columns=COLUNAS + ['motivo'])
    counts = {'entrada': len(bronze), 'silver': len(silver), 'rejeitadas': len(rejected), 'substituidas': len(replaced)}
    assert counts['entrada'] == counts['silver'] + counts['rejeitadas'] + counts['substituidas']
    return silver, rejected, replaced, counts


def gold_retail(silver):
    if list(silver.columns) != SILVER:
        raise ValueError('Contrato Silver inválido.')
    if silver.empty:
        return pd.DataFrame(columns=GOLD)
    data = silver.copy()
    data['dia'] = pd.to_datetime(data.data).dt.date.astype(str)
    data['venda_bruta_centavos'] = data.valor_centavos.clip(lower=0)
    data['estorno_centavos'] = -data.valor_centavos.clip(upper=0)
    result = data.groupby('dia', as_index=False).agg(
        venda_bruta_centavos=('venda_bruta_centavos', 'sum'), estorno_centavos=('estorno_centavos', 'sum'),
        receita_liquida_centavos=('valor_centavos', 'sum'), linhas=('linha_fonte', 'count'))
    return result[GOLD]

# COMMAND ----------

bronze = carregar_amostra(PROJETO / 'data')
silver, rejeitadas, substituidas, contagens = limpar_retail(bronze)
assert contagens == {'entrada':3000,'silver':2946,'rejeitadas':10,'substituidas':44}
display(rejeitadas)
display(gold_retail(silver))

# COMMAND ----------

from pyspark.sql import types as T
gold = gold_retail(silver)
schema = T.StructType([T.StructField('dia',T.StringType(),False),*[T.StructField(c,T.LongType(),False) for c in gold.columns[1:]]])
linhas = [(str(r[0]),*[int(x) for x in r[1:]]) for r in gold.itertuples(index=False,name=None)]
gold_spark = spark.createDataFrame(linhas,schema)
assert gold_spark.agg({'receita_liquida_centavos':'sum'}).first()[0] == 5682033
display(gold_spark)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Explique antes de concluir
# MAGIC 
# MAGIC Por que cancelamento válido não é rejeitado? O que foi removido por privacidade? Por que este recorte de um dia não sustenta previsão semanal? Registre versão do runtime, contagens, link/run ID e eventuais falhas.
