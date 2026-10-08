"""Referência: grão diário antes da janela acumulada."""


def consulta_acumulado():
    return '''WITH diario AS (
 SELECT dia, SUM(valor_centavos) AS receita_centavos FROM vendas GROUP BY dia
)
SELECT dia, receita_centavos,
 SUM(receita_centavos) OVER (ORDER BY dia ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS acumulado_centavos
FROM diario ORDER BY dia'''
