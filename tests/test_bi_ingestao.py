import pandas as pd
import pytest
from lab.bi import gerar_comercio, fatos, resumo, CONSULTAS
from lab.dados import gerar_vendas
from lab.ingestao import processar_lotes
from lab.sql_seguro import consultar_tabelas, ConsultaInvalida


def test_join_preserva_itens_mas_pedidos_sao_distintos():
    tables = gerar_comercio()
    frame = fatos(tables)
    assert len(frame) == len(tables['itens_pedido'])
    metrics = resumo(tables)
    assert metrics['pedidos'] == 164 and metrics['linhas'] > 164
    assert metrics['receita_centavos'] - int(frame.loc[frame.status.eq('concluido'), 'custo_centavos'].sum()) == metrics['margem_centavos']
    result, _ = consultar_tabelas(tables, CONSULTAS['Grão: linhas versus pedidos'])
    assert result.iloc[0].to_dict() == {'linhas': metrics['linhas'], 'pedidos': metrics['pedidos']}
    accumulated, _ = consultar_tabelas(tables, CONSULTAS['Receita acumulada com janela'])
    assert accumulated.iloc[-1]['acumulada'] == metrics['receita_centavos'] / 100


def test_dimensao_duplicada_nao_publica_metrica_inflada():
    tables = gerar_comercio()
    tables['produtos'] = pd.concat([tables['produtos'], tables['produtos'].iloc[:1]])
    with pytest.raises(pd.errors.MergeError):
        fatos(tables)


@pytest.mark.parametrize('query', ['DROP TABLE pedidos', 'UPDATE clientes SET regiao="x"', 'SELECT * FROM sqlite_master', "SELECT load_extension('x')", 'PRAGMA table_info(pedidos)', "ATTACH DATABASE 'x' AS externo"])
def test_sql_multitabela_mantem_fronteira_de_leitura(query):
    with pytest.raises(ConsultaInvalida):
        consultar_tabelas(gerar_comercio(), query)


def test_repeticao_manifesto_e_atraso_nao_duplicam_destino():
    base = gerar_vendas(90, False)
    update = [{**base[0], 'quantidade': '8', 'atualizado_em': '2026-04-02 10:00:00'}]
    normal = processar_lotes([('A', base), ('B', update)])
    replay = processar_lotes([('A', base), ('B', update), ('B', update), ('C', [base[0]])])
    pd.testing.assert_frame_equal(normal.resultado.silver, replay.resultado.silver)
    assert replay.eventos[2]['adicionados'] == 0
    assert len(replay.resultado.bronze) == len(normal.resultado.bronze) + 1


def test_id_de_lote_reutilizado_com_conteudo_diferente_falha():
    base = gerar_vendas(90, False)
    with pytest.raises(ValueError, match='conteúdo diferente'):
        processar_lotes([('A', base), ('A', [{**base[0], 'quantidade': '99'}])])


def test_ultima_correcao_invalida_nao_ressuscita_versao_antiga():
    base = gerar_vendas(90, False)
    result = processar_lotes([('A', base), ('B', [{**base[0], 'preco_unitario': '-1', 'atualizado_em': '2026-04-02 10:00:00'}])]).resultado
    assert len(result.silver) == 89 and len(result.rejeitadas) == 1
    assert base[0]['venda_id'] not in set(result.silver.venda_id)
