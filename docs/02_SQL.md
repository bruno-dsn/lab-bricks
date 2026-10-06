# Uma pergunta de negócio por consulta

Pergunte primeiro: **quanto vendemos em pedidos concluídos por canal?** Para responder, precisamos do canal, do valor de cada pedido e da regra que exclui cancelamentos.

```sql
SELECT canal,
       SUM(valor_centavos) / 100.0 AS receita
FROM silver_vendas
WHERE status = 'concluida'
GROUP BY canal
ORDER BY receita DESC;
```

`FROM` define a tabela. `WHERE` escolhe as linhas. `GROUP BY` reúne linhas com o mesmo canal. `SUM` agrega o valor de cada grupo. `ORDER BY` organiza a apresentação do resultado.

O campo guarda centavos inteiros para preservar a unidade monetária na soma. `100.0` faz a conversão para reais; usar divisão inteira no motor errado pode eliminar os centavos.

## Ticket médio depende do que estamos contando

```sql
SELECT COUNT(*) AS pedidos,
       SUM(valor_centavos) / 100.0 AS receita,
       SUM(valor_centavos) / 100.0 / COUNT(*) AS ticket_medio
FROM silver_vendas
WHERE status = 'concluida';
```

Neste caso, uma linha representa um pedido com um produto. `COUNT(*)` conta pedidos, e `SUM(quantidade)` conta unidades. Se um pedido tiver várias linhas de produtos numa fonte futura, essa definição precisará mudar: contar linhas deixará de contar pedidos.

## Uma taxa usa outro universo

Para medir cancelamento, o denominador é o total de pedidos válidos, incluindo cancelados. A consulta precisa dividir uma contagem filtrada por outra que representa o universo completo.

Antes de olhar o gabarito, escreva a consulta. Confira se a divisão produz uma fração entre zero e um. Diga no título se o resultado está em fração ou porcentagem.

## O que pode mudar entre os motores

As consultas acima usam um subconjunto comum a SQLite e Spark SQL. Funções de data, conversões tolerantes a erro, nomes de tabelas e tipos decimais diferem entre os ambientes. `MERGE`, histórico Delta e catálogo de três níveis pertencem aos notebooks, não ao editor local.

O editor aceita consultas de leitura na `silver_vendas` e funções aprovadas. CTEs comuns de leitura funcionam. Escrita, PRAGMA, extensões e recursão são bloqueados; uma consulta muito pesada também pode ser interrompida.

## Teste a explicação

Retire o filtro de status da consulta de receita e compare o resultado. Explique a diferença usando os pedidos cancelados. Depois recoloque o filtro e reconcilie a soma por canal com a soma total de concluídos. Um total que parece plausível ainda precisa desse teste.
