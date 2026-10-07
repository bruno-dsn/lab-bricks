+++
id = "s02-joins"
title = "Construa joins sem multiplicar sua receita"
track = "sql-bi"
level = "Intermediário"
version = "2.0"
prerequisites = ["s01-agregacoes", "f02-grao"]
sources = ["bi-livro", "engenharia-livro"]
objectives = ["Reconhecer cardinalidade de joins", "Detectar duplicação em dimensões"]
lab = "BI e modelagem; notebook 05"
+++

# Construa joins sem multiplicar sua receita

## Problema

A receita dobra quando você acrescenta o nome do produto. O problema pode estar no relacionamento entre tabelas, mesmo que os valores financeiros não tenham mudado.

## Conceito

Um JOIN combina linhas que atendem a uma condição. Na relação muitos-para-um, cada item deve encontrar um único produto. Se a dimensão possui duas linhas para o mesmo `produto_id`, cada item pode virar duas linhas. Chave única não é só uma convenção visual: é uma pré-condição da métrica.

INNER JOIN elimina linhas sem correspondência. LEFT JOIN conserva a esquerda e produz nulos para não encontrados; colocar depois `WHERE direita.coluna = valor` pode eliminar essas linhas. Faça testes de unicidade e de cobertura de chaves, além de conferir contagens antes e depois do JOIN.

## Exemplo explicado

```sql
SELECT d.categoria,
       SUM(i.quantidade*i.preco_unitario_centavos)/100.0 AS receita
FROM itens_pedido i
JOIN pedidos p ON i.pedido_id=p.pedido_id
JOIN produtos d ON i.produto_id=d.produto_id
WHERE p.status='concluido'
GROUP BY d.categoria;
```

O preço usado é o preço do item no momento da compra. Uma alteração no preço atual da dimensão não deve reescrever automaticamente a receita histórica.

## Experimente

Inspecione as quatro tabelas de BI. Rode o JOIN e reconcilie categorias com a receita total. Faça uma cópia local da dimensão, duplique uma chave e observe que `fatos()` rejeita a relação com `validate='many_to_one'`. Para investigação SQL, conte chaves com GROUP BY e HAVING COUNT(*) > 1.

## Resultado esperado

Com dimensões válidas, o JOIN preserva a quantidade de linhas dos itens. Uma chave duplicada na dimensão dispara erro na montagem Pandas, antes de mostrar uma receita inflada.

## Erros comuns

Usar DISTINCT no resultado para esconder um JOIN errado; juntar por nome livre; aplicar preço atual a compras antigas; confundir ausência de correspondência com valor zero.

## Desafio

Defina um procedimento de quarentena para itens cujo produto não existe. Escolha entre bloquear publicação ou publicar com categoria “não identificada”, explicando a consequência.

## Critério de conclusão

Você demonstra uma cardinalidade muitos-para-um e detecta uma dimensão duplicada antes da agregação.

## Referências

Referências: BI e engenharia fornecidos; [JOIN no Spark](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-join.html).
