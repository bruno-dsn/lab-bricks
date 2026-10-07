"""Editor SQL para uma cópia efêmera de dados fictícios.

O authorizer do SQLite controla as operações reais. Um filtro de texto
sozinho não seria uma fronteira de segurança para o editor.
"""
import sqlite3
import re
import pandas as pd


class ConsultaInvalida(ValueError):
    pass


FUNCOES = {"sum", "count", "avg", "min", "max", "round", "coalesce",
           "abs", "length", "lower", "upper", "date", "strftime", "nullif",
           "row_number", "rank", "dense_rank", "lag", "lead"}


def consultar(silver, query, limite=200):
    return consultar_tabelas({"silver_vendas": silver}, query, limite)


def consultar_tabelas(tabelas, query, limite=200):
    if not isinstance(query, str) or not 1 <= len(query.strip()) <= 6000:
        raise ConsultaInvalida("Escreva uma consulta de até 6.000 caracteres.")
    if type(limite) is not int or not 1 <= limite <= 500:
        raise ConsultaInvalida("O limite deve ficar entre 1 e 500 linhas.")
    if not isinstance(tabelas, dict) or not 1 <= len(tabelas) <= 5 or not all(isinstance(name, str) and re.fullmatch(r"[a-z][a-z0-9_]{0,40}", name) and isinstance(frame, pd.DataFrame) for name, frame in tabelas.items()):
        raise ConsultaInvalida("Tabelas fora do contrato do laboratório.")
    if any(len(frame) > 2000 for frame in tabelas.values()) or sum(len(frame) for frame in tabelas.values()) > 4000:
        raise ConsultaInvalida("A amostra excedeu o tamanho permitido.")
    conn = sqlite3.connect(":memory:")
    try:
        for name, frame in tabelas.items():
            frame.to_sql(name, conn, index=False)
        conn.execute("PRAGMA query_only = ON")
        conn.setlimit(sqlite3.SQLITE_LIMIT_LENGTH, 100_000)
        conn.setlimit(sqlite3.SQLITE_LIMIT_SQL_LENGTH, 6000)
        conn.setlimit(sqlite3.SQLITE_LIMIT_EXPR_DEPTH, 50)
        conn.setlimit(sqlite3.SQLITE_LIMIT_COMPOUND_SELECT, 10)

        def authorize(action, arg1, arg2, database, trigger):
            if action == sqlite3.SQLITE_SELECT:
                return sqlite3.SQLITE_OK
            if action == sqlite3.SQLITE_READ and arg1 in tabelas:
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
            raise ConsultaInvalida("Use uma consulta de leitura nas tabelas do laboratório.")
        rows = cursor.fetchmany(limite + 1)
        return pd.DataFrame(rows[:limite], columns=[c[0] for c in cursor.description]), len(rows) > limite
    except sqlite3.Error:
        raise ConsultaInvalida("Consulta não permitida, inválida ou acima do limite de processamento. Use SELECT nas tabelas do laboratório.") from None
    finally:
        conn.close()
