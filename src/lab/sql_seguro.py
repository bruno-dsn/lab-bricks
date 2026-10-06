"""Editor SQL para uma cópia efêmera de dados fictícios.

O authorizer do SQLite controla as operações reais. Um filtro de texto
sozinho não seria uma fronteira de segurança para o editor.
"""
import sqlite3
import pandas as pd


class ConsultaInvalida(ValueError):
    pass


FUNCOES = {"sum", "count", "avg", "min", "max", "round", "coalesce",
           "abs", "length", "lower", "upper", "date", "strftime", "nullif"}


def consultar(silver, query, limite=200):
    if not isinstance(query, str) or not 1 <= len(query.strip()) <= 6000:
        raise ConsultaInvalida("Escreva uma consulta de até 6.000 caracteres.")
    if type(limite) is not int or not 1 <= limite <= 500:
        raise ConsultaInvalida("O limite deve ficar entre 1 e 500 linhas.")
    if len(silver) > 2000:
        raise ConsultaInvalida("A amostra excedeu o tamanho permitido.")
    conn = sqlite3.connect(":memory:")
    try:
        silver.to_sql("silver_vendas", conn, index=False)
        conn.execute("PRAGMA query_only = ON")
        conn.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 100_000)
        conn.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, 6000)
        conn.setlimit(sqlite3.SQLITE_LIMIT_EXPR_DEPTH, 50)
        conn.setlimit(sqlite3.SQLITE_LIMIT_COMPOUND_SELECT, 10)

        def authorize(action, arg1, arg2, database, trigger):
            if action == sqlite3.SQLITE_SELECT:
                return sqlite3.SQLITE_OK
            if action == sqlite3.SQLITE_READ and arg1 == "silver_vendas":
                return sqlite3.SQLITE_OK
            if action == sqlite3.SQLITE_FUNCTION and (arg2 or arg1 or "").lower() in FUNCOES:
                return sqlite3.SQLITE_OK
            return sqlite3.SQLITE_DENY

        conn.set_authorizer(authorize)
        steps = 0

        def budget():
            nonlocal steps
            steps += 1
            return steps >= 100  # no máximo cerca de 100 mil instruções da VM

        conn.set_progress_handler(budget, 1000)
        cursor = conn.execute(query)
        if cursor.description is None:
            raise ConsultaInvalida("Use uma consulta de leitura na tabela silver_vendas.")
        rows = cursor.fetchmany(limite + 1)
        return pd.DataFrame(rows[:limite], columns=[c[0] for c in cursor.description]), len(rows) > limite
    except sqlite3.Error:
        raise ConsultaInvalida("Consulta não permitida, inválida ou acima do limite de processamento. Use SELECT na tabela silver_vendas.") from None
    finally:
        conn.close()
