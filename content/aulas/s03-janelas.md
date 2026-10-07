+++
id = "s03-janelas"
title = "Use CTEs e janelas mantendo o detalhe"
track = "sql-bi"
level = "Intermediário"
version = "2.0"
prerequisites = ["s02-joins"]
sources = ["bi-livro", "engenharia-livro"]
objectives = ["Criar uma receita acumulada", "Explicar partição, ordenação e frame"]
lab = "BI e modelagem; notebook 05"
+++

# Use CTEs e janelas mantendo o detalhe

## Problema

Você quer saber a receita de cada dia e o total acumulado até aquele dia. Um GROUP BY sozinho reduz linhas; uma janela consegue acrescentar contexto sem perder o grão escolhido.

## Conceito

Uma CTE nomeia uma etapa da consulta. Ela melhora a leitura, mas não promete materialização nem aceleração automática. Uma função de janela recebe uma partição, uma ordem e, para agregações, um frame que define quais linhas entram no cálculo.

`SUM(receita) OVER (ORDER BY data ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` produz acumulado. `LAG` recupera a linha anterior na ordem escolhida. `ROW_NUMBER` atribui posições, enquanto DENSE_RANK mantém empates de valor. Ordenação com empates precisa de uma chave adicional para ser determinística.

## Exemplo explicado

```sql
WITH diario AS (
  SELECT p.data_pedido,
         SUM(i.quantidade*i.preco_unitario_centavos) AS centavos
  FROM pedidos p JOIN itens_pedido i ON p.pedido_id=i.pedido_id
  WHERE p.status='concluido'
  GROUP BY p.data_pedido
)
SELECT data_pedido, centavos,
       SUM(centavos) OVER (
         ORDER BY data_pedido
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS acumulado
FROM diario ORDER BY data_pedido;
```

A CTE primeiro define uma linha por dia. A janela opera nesse grão, evitando somar uma métrica diária repetida em várias linhas de itens.

## Experimente

Execute o exemplo de receita acumulada no app. Confira que a última linha corresponde ao total dos pedidos concluídos. Escreva uma diferença para o dia anterior com LAG. Considere que um dia ausente na tabela não é automaticamente um dia de receita zero.

## Resultado esperado

O acumulado é não decrescente porque essa fonte só tem receita não negativa de concluídos. A última linha reconcilia o total. Em dados com estornos, a propriedade não decrescente deixaria de ser uma regra válida.

## Erros comuns

Omitir a ordenação; usar uma janela antes de fixar o grão; assumir que LAG significa “ontem” quando há datas ausentes; aceitar desempate aleatório.

## Desafio

Faça um ranking de produtos por receita dentro de cada categoria. Escolha RANK ou DENSE_RANK e explique como tratar empates.

## Critério de conclusão

Você identifica partição, ordem e frame e demonstra uma reconciliação do último acumulado.

## Referências

Referências: BI e engenharia; [funções de janela Spark](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-window.html).
