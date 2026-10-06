import pytest
from lab.dados import gerar_vendas
from lab.pipeline import tratar, indicadores
from lab.sql_seguro import consultar, ConsultaInvalida


@pytest.fixture
def silver():
    return tratar(gerar_vendas()).silver


def test_sql_reconcilia_com_a_metrica(silver):
    df, truncated = consultar(silver, "SELECT SUM(valor_centavos)/100.0 AS receita FROM silver_vendas WHERE status='concluida'")
    assert df.iloc[0].receita == indicadores(silver)["receita"]
    assert not truncated


def test_cte_de_leitura_e_permitida(silver):
    df, _ = consultar(silver, "WITH pedidos AS (SELECT * FROM silver_vendas) SELECT COUNT(*) AS n FROM pedidos")
    assert df.iloc[0].n == len(silver)


@pytest.mark.parametrize("query", [
    "DROP TABLE silver_vendas", "DELETE FROM silver_vendas", "UPDATE silver_vendas SET status='concluida'",
    "ATTACH DATABASE '/tmp/segredo.db' AS segredo", "PRAGMA database_list",
    "SELECT name FROM sqlite_master", "SELECT load_extension('/tmp/a.so')",
    "SELECT readfile('/etc/passwd')", "SELECT randomblob(1000000000)",
    "SELECT * FROM silver_vendas; DROP TABLE silver_vendas;",
    "WITH RECURSIVE a(n) AS (SELECT 1 UNION ALL SELECT n+1 FROM a) SELECT * FROM a",
    "SELECT * FROM silver_vendas a CROSS JOIN silver_vendas b CROSS JOIN silver_vendas c ORDER BY a.preco_unitario",
])
def test_bloqueia_escrita_arquivos_e_abuso(silver, query):
    with pytest.raises(ConsultaInvalida):
        consultar(silver, query)
    # A próxima consulta usa uma cópia nova e segue intacta.
    df, _ = consultar(silver, "SELECT COUNT(*) AS n FROM silver_vendas")
    assert df.iloc[0].n == len(silver)


def test_limita_resultado(silver):
    df, truncated = consultar(silver, "SELECT * FROM silver_vendas", limite=5)
    assert len(df) == 5 and truncated


def test_sql_longo_e_bloqueado(silver):
    with pytest.raises(ConsultaInvalida):
        consultar(silver, "SELECT " + "1" * 6000)
