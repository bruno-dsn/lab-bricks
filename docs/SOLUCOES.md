# Gabaritos comentados

## Receita, pedidos e unidades

```sql
SELECT canal,
       COUNT(*) AS pedidos,
       SUM(valor_centavos) / 100.0 AS receita
FROM silver_vendas
WHERE status = 'concluida'
GROUP BY canal;

SELECT produto, SUM(quantidade) AS unidades
FROM silver_vendas
WHERE status = 'concluida'
GROUP BY produto;
```

Neste contrato, a chave identifica um pedido com um produto. A contagem representa pedidos e a quantidade representa unidades. Numa fonte com vários itens por pedido, seria preciso revisar a granularidade.

## Taxa de cancelamento

```sql
SELECT ROUND(
  100.0 * SUM(CASE WHEN status = 'cancelada' THEN 1 ELSE 0 END)
  / NULLIF(COUNT(*), 0), 2
) AS cancelamento_percentual
FROM silver_vendas;
```

O denominador inclui concluídos e cancelados. `NULLIF` evita divisão por zero numa tabela vazia; um resultado nulo precisa ser tratado como ausência de pedidos, sem inventar uma taxa observada.

## Canal desconhecido

No pipeline local, acrescente um motivo na lista `reasons` quando `row['canal']` não estiver em `{'Site', 'Aplicativo', 'Marketplace'}`. Na função `normalizar` do notebook 00, acrescente uma condição equivalente na lista `regras`.

O teste deve usar um pedido válido com só o canal alterado. Depois da transformação, a Silver deve estar vazia para essa entrada e a quarentena deve mencionar o canal. Faça também um teste para cada canal permitido para evitar rejeitar toda a fonte por engano.

## Versão antiga

A condição `origem.atualizado_em > destino.atualizado_em` bloqueia uma versão mais antiga. A igualdade também não atualiza. Se sua origem permitir duas correções com o mesmo timestamp, será preciso definir uma política adicional de sequência ou versão; este exercício não inventa essa ordenação.

## Versão recente inválida

```python
from lab.pipeline import tratar

base = {
    'venda_id': 'P1', 'data_venda': '2026-01-01',
    'produto': 'Caderno', 'categoria': 'Papelaria', 'canal': 'Site',
    'quantidade': '2', 'preco_unitario': '10.25',
    'status': 'concluida', 'atualizado_em': '2026-01-01 10:00:00'
}
recente = {**base, 'preco_unitario': '-1.00',
           'atualizado_em': '2026-01-02 10:00:00'}
resultado = tratar([base, recente])
assert resultado.silver.empty
assert len(resultado.rejeitadas) == 1
assert len(resultado.substituidas) == 1
```

Execute dentro de um ambiente em que `src/` esteja no `PYTHONPATH`, como os testes deste repositório. O caso já tem cobertura em `tests/test_pipeline.py`.

## Janelas de teste

```python
from lab.dados import gerar_vendas
from lab.pipeline import tratar
from lab.ml import comparar

gold = tratar(gerar_vendas()).gold
for dias in [7, 14, 21]:
    _, metricas = comparar(gold, dias_teste=dias)
    print(dias, metricas)
```

Cada janela reserva outra parte do calendário e muda a quantidade de treino. A comparação precisa mencionar isso. O resultado não permite declarar que um modelo é sempre melhor nem escolher a janela só para obter o menor erro divulgado.
