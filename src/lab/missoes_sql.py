"""Três missões com respostas conferidas no SQLite de leitura."""
import pandas as pd
from .sql_seguro import consultar_tabelas

MISSOES = {
 'join': {'titulo':'Preserve pedidos sem itens', 'enunciado':'Retorne pedido_id e receita_centavos, em ordem de pedido, incluindo receita zero para pedidos sem itens.', 'colunas':['pedido_id','receita_centavos'], 'esperado':[(1,2000),(2,1500),(3,0)], 'exemplo':'SELECT p.pedido_id, COALESCE(SUM(i.valor_centavos),0) AS receita_centavos FROM pedidos p LEFT JOIN itens i ON p.pedido_id=i.pedido_id GROUP BY p.pedido_id ORDER BY p.pedido_id'},
 'cte': {'titulo':'Evite multiplicar duas tabelas filhas', 'enunciado':'Retorne pedido_id, receita_centavos e recebido_centavos. Agregue itens e pagamentos separadamente antes de juntá-los.', 'colunas':['pedido_id','receita_centavos','recebido_centavos'], 'esperado':[(1,2000,2000),(2,1500,1500),(3,0,0)], 'exemplo':'WITH i AS (SELECT pedido_id,SUM(valor_centavos) AS r FROM itens GROUP BY pedido_id), g AS (SELECT pedido_id,SUM(valor_centavos) AS r FROM pagamentos GROUP BY pedido_id) SELECT p.pedido_id,COALESCE(i.r,0) AS receita_centavos,COALESCE(g.r,0) AS recebido_centavos FROM pedidos p LEFT JOIN i ON p.pedido_id=i.pedido_id LEFT JOIN g ON p.pedido_id=g.pedido_id ORDER BY p.pedido_id'},
 'janela': {'titulo':'Acumulado com grão diário', 'enunciado':'Agregue vendas por dia antes da janela. Retorne dia, receita_centavos e acumulado_centavos, ordenados por dia.', 'colunas':['dia','receita_centavos','acumulado_centavos'], 'esperado':[('2026-01-01',1200,1200),('2026-01-02',800,2000),('2026-01-03',2000,4000)], 'exemplo':'WITH d AS (SELECT dia,SUM(valor_centavos) AS receita_centavos FROM vendas GROUP BY dia) SELECT dia,receita_centavos,SUM(receita_centavos) OVER (ORDER BY dia ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS acumulado_centavos FROM d ORDER BY dia'},
}


def tabelas_missao():
    return {'pedidos':pd.DataFrame({'pedido_id':[1,2,3]}),
            'itens':pd.DataFrame({'pedido_id':[1,1,2],'valor_centavos':[1200,800,1500]}),
            'pagamentos':pd.DataFrame({'pedido_id':[1,1,2],'valor_centavos':[900,1100,1500]}),
            'vendas':pd.DataFrame({'dia':['2026-01-01','2026-01-01','2026-01-02','2026-01-03'],'valor_centavos':[700,500,800,2000]})}


def corrigir_missao(identifier, query):
    if identifier not in MISSOES:
        raise ValueError('Missão desconhecida.')
    spec = MISSOES[identifier]
    result, truncated = consultar_tabelas(tabelas_missao(), query)
    actual = list(result.itertuples(index=False, name=None))
    ok = not truncated and list(result.columns) == spec['colunas'] and actual == spec['esperado']
    return {'ok':ok,'feedback':'Resultado correto. Explique o grão e por que cada JOIN preserva a população.' if ok else 'Confira nomes das colunas, ordem, população e agregações. Compare cada linha com o contrato.', 'resultado':result}
