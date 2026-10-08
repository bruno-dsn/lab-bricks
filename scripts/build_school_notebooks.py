"""Gera cinco notebooks e a extensão temporal do 11 com módulos compartilhados."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def source(name):
    return '\n'.join(line for line in (ROOT/'src/lab'/f'{name}.py').read_text().splitlines() if not line.startswith('from .')).strip()


def emit(name,cells):
    rows=['# Databricks notebook source']
    for kind,body in cells:
        rows.append('# COMMAND ----------')
        if kind=='md':body='%md\n'+body
        if body.startswith('%'):body='\n'.join('# MAGIC '+line for line in body.splitlines())
        rows.append(body)
    (ROOT/'notebooks'/f'{name}.py').write_text('\n\n'.join(rows)+'\n')


PATH_CONFIG='''import re
from pathlib import Path
dbutils.widgets.text('projeto_dir', '')
projeto_dir = dbutils.widgets.get('projeto_dir')
if not re.fullmatch(r'/(?:Workspace|Volumes)/[A-Za-z0-9@._ /-]{1,240}', projeto_dir) or '..' in Path(projeto_dir).parts:
    raise ValueError('Informe a pasta do projeto em /Workspace ou /Volumes, com content/ e data/.')
PROJETO = Path(projeto_dir)
'''


def build():
    emit('12_dados_publicos_reais',[
        ('md','# Caso público UCI Online Retail\n\nFaça primeiro a configuração. Disponibilize o projeto completo em Workspace/Git folder ou Volume e informe projeto_dir. Este notebook usa a amostra pública incluída, sem CustomerID. Não escreva que rodou na conta sem guardar a evidência.'),
        ('py',PATH_CONFIG),('py',source('retail_real')),
        ('py',"bronze = carregar_amostra(PROJETO / 'data')\nsilver, rejeitadas, substituidas, contagens = limpar_retail(bronze)\nassert contagens == {'entrada':3000,'silver':2946,'rejeitadas':10,'substituidas':44}\ndisplay(rejeitadas)\ndisplay(gold_retail(silver))"),
        ('py',"from pyspark.sql import types as T\ngold = gold_retail(silver)\nschema = T.StructType([T.StructField('dia',T.StringType(),False),*[T.StructField(c,T.LongType(),False) for c in gold.columns[1:]]])\nlinhas = [(str(r[0]),*[int(x) for x in r[1:]]) for r in gold.itertuples(index=False,name=None)]\ngold_spark = spark.createDataFrame(linhas,schema)\nassert gold_spark.agg({'receita_liquida_centavos':'sum'}).first()[0] == 5682033\ndisplay(gold_spark)"),
        ('md','## Explique antes de concluir\n\nPor que cancelamento válido não é rejeitado? O que foi removido por privacidade? Por que este recorte de um dia não sustenta previsão semanal? Registre versão do runtime, contagens, link/run ID e eventuais falhas.')])
    emit('13_validacao_temporal_calibracao',[
        ('md','# Desenvolvimento, gap e calibração\n\nDados sintéticos. Pacote de referência: scikit-learn 1.8.0. As versões reais do workspace precisam entrar no registro. A célula de instalação reinicia o Python.'),
        ('py','%pip install scikit-learn==1.8.0'),('py','dbutils.library.restartPython()'),
        ('py',source('classificacao')),('py',source('ciclo_ml')),('py',source('rigor_ml')),
        ('py',"frame = gerar_entregas(600,42)\nwindows, refit, test = janelas_temporais(frame,gap=2)\nfor treino,validacao in windows:\n    assert (validacao.data.min()-treino.data.max()).days >= 3\n    assert set(validacao.data).isdisjoint(test.data)\nmodel, ranking, avaliacao = selecionar_temporal(frame,gap=2)\ndisplay(ranking.head(8))\nprint(avaliacao)\ncalibracao, curvas = comparar_calibracao(frame)\ndisplay(calibracao)\nfor nome,curva in curvas.items():\n    print(nome)\n    display(curva)"),
        ('md','## Desafio\n\nMude apenas os rótulos do teste e prove que seleção e limiar empírico não mudam. Compare limiar teórico e empírico com suporte por intervalo. Registre resultado, não uma promessa de melhoria.')])
    emit('14_cdc_scd2',[
        ('md','# CDC, SCD2 e MERGE sobre snapshot completo\n\nA referência local reconstrói o log completo. A opção Delta só escreve uma tabela dedicada marcada como demonstração. Fonte completa e reconstrução de intervalos são requisitos; isto não é um MERGE de CDC de produção.'),
        ('py',source('engenharia_avancada')),
        ('py',"eventos = [\n {'evento_id':'e1','chave':'cliente-A','instante':'2026-01-01','operacao':'upsert','valor':'Norte'},\n {'evento_id':'e3','chave':'cliente-A','instante':'2026-01-03','operacao':'upsert','valor':'Sul'},\n {'evento_id':'e2','chave':'cliente-A','instante':'2026-01-02','operacao':'upsert','valor':'Centro'}\n]\nhistorico, auditoria = historico_scd2(eventos + [eventos[0].copy()])\nassert historico.valor.tolist() == ['Norte','Centro','Sul']\nassert historico.atual.sum() == 1\ndisplay(historico)\ndisplay(auditoria)"),
        ('py',"import re\nfrom delta.tables import DeltaTable\nfrom pyspark.sql import types as T\ndbutils.widgets.text('executar_delta','nao')\ndbutils.widgets.text('catalogo','workspace')\ndbutils.widgets.text('schema_estudo','lab_bricks')\nif dbutils.widgets.get('executar_delta') == 'sim':\n    catalogo, esquema = [dbutils.widgets.get(k) for k in ('catalogo','schema_estudo')]\n    if not all(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]{0,62}',x) for x in (catalogo,esquema)):\n        raise ValueError('Catálogo ou schema inválidos.')\n    tabela = f'{catalogo}.{esquema}.lb_escola_scd2'\n    spark.conf.set('spark.sql.session.timeZone','UTC')\n    estrutura = 'evento_id STRING, chave STRING, valor STRING, inicio TIMESTAMP, fim TIMESTAMP, atual BOOLEAN'\n    linhas = [(r.evento_id,r.chave,r.valor,r.inicio.to_pydatetime().replace(tzinfo=None),None if pd.isna(r.fim) else r.fim.to_pydatetime().replace(tzinfo=None),bool(r.atual)) for r in historico.itertuples()]\n    snapshot = spark.createDataFrame(linhas,estrutura)\n    if not spark.catalog.tableExists(tabela):\n        snapshot.write.format('delta').mode('errorifexists').saveAsTable(tabela)\n        spark.sql(f\"ALTER TABLE {tabela} SET TBLPROPERTIES ('lab_bricks.demo'='scd2')\")\n    propriedades = {r.key:r.value for r in spark.sql(f'SHOW TBLPROPERTIES {tabela}').collect()}\n    if propriedades.get('lab_bricks.demo') != 'scd2':\n        raise ValueError('Tabela sem marca de estudo; operação cancelada.')\n    (DeltaTable.forName(spark,tabela).alias('t').merge(snapshot.alias('s'),'t.chave=s.chave AND t.inicio=s.inicio').whenMatchedUpdateAll().whenNotMatchedInsertAll().whenNotMatchedBySourceDelete().execute())\n    assert spark.table(tabela).count() == len(historico)\n    display(spark.table(tabela).orderBy('chave','inicio'))\nelse:\n    print('MERGE Delta não executado. Ative explicitamente apenas na tabela de estudo.')"),
        ('md','## Evidência\n\nRepita o snapshot, simule delete e reconstrua a junção temporal. Registre as métricas do MERGE e o ID da execução real. O registro permanece pendente até essa evidência existir.')])
    streaming='''import json, re, uuid
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
        conteudo = '\\n'.join(json.dumps(r) for r in lote)+'\\n'
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
'''
    emit('15_streaming_watermark',[
        ('md','# Watermark e replay de checkpoint\n\nO operador nativo usa agregação por janela, saída append e sink Delta. Não pressupõe descarte idêntico ao simulador por timestamp individual. Cada arquivo só entra depois do trigger anterior terminar; a ordem não depende de mtime igual.'),
        ('py',source('engenharia_avancada')),
        ('py',"lotes = [[{'evento_id':'a','instante':'2026-01-01T10:20:00Z','valor':20}], [{'evento_id':'b','instante':'2026-01-01T10:02:00Z','valor':99}], []]\naudit, janelas = simular_watermark(lotes)\ndisplay(audit)\ndisplay(janelas)"),
        ('py',streaming),('md','## Desafio\n\nCompare um evento antes da fronteira com uma janela que ainda termina depois dela. Explique replay do checkpoint versus deduplicação de IDs. Não apague o checkpoint para simular um teste que não ocorreu.')])
    emit('16_rag_evidencias',[
        ('md','# Recuperação, resposta extrativa e avaliação\n\nEste notebook não baixa nem executa LLM. O experimento opcional de geração foi executado localmente e tem relatório próprio. Informe projeto_dir apontando para o projeto completo.'),
        ('py',PATH_CONFIG),('py',source('recuperacao')),('py',source('rag')),('py',source('benchmark')),
        ('py',"protocol = protocolo(PROJETO / 'content')\ndocuments = json.loads((PROJETO / 'content/benchmark_corpus.json').read_text())\npergunta = 'Como repetir um lote sem duplicar registros?'\nevidence = buscar(pergunta,documents,3)\nresposta = responder_extrativo(pergunta,evidence,.12)\nprint(resposta)\nassert set(resposta['citacoes']) <= {e['id'] for e in evidence}\nresults = json.loads((PROJETO / 'content/search_results.json').read_text())\nprint({k:{m:v for m,v in results[k].items() if m != 'casos'} for k in ('tfidf','semantica')})"),
        ('md','## Revise a afirmação\n\nCitação estruturalmente válida não prova suporte factual. Faça ex14, compare perguntas fora do escopo e registre se a resposta ajuda a resolver o problema. Geração local, Delta e conta Databricks são evidências separadas.')])
    p=ROOT/'notebooks/11_ciclo_ml_e_contrato.py';body=p.read_text();marker='# EXTENSAO ESCOLA V3'
    if marker in body:body=body.split(marker)[0].rstrip()
    body+='\n\n'+marker+'\n\n# COMMAND ----------\n\n'+source('rigor_ml')+'\n\n# COMMAND ----------\n\n_, ranking_temporal, avaliacao_temporal = selecionar_temporal(frame,gap=1)\ndisplay(ranking_temporal.head(8))\nprint(avaliacao_temporal)\n'
    p.write_text(body)
    print('Cinco notebooks e extensão do 11 gerados. Execute export_notebooks.py.')


if __name__=='__main__':build()
