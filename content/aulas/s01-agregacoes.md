+++
id = "s01-agregacoes"
title = "Filtre a população antes de agregar"
track = "sql-bi"
level = "Intermediário"
version = "2.0"
prerequisites = ["f03-python", "f02-grao"]
sources = ["bi-livro", "engenharia-livro"]
objectives = ["Construir SELECT, WHERE, GROUP BY e HAVING", "Reconciliar agregações por canal"]
lab = "Laboratório SQL; notebook 01"
+++

# Filtre a população antes de agregar

## Problema

Você precisa comparar receita por canal. Se o status cancelado entrar na soma, o total muda sem que a interface dê qualquer sinal de erro.

## Conceito

Uma consulta descreve a população com FROM e WHERE, agrupa com GROUP BY e calcula agregações como SUM e COUNT. HAVING filtra grupos já agregados; WHERE filtra linhas antes da agregação. ORDER BY organiza a apresentação e não muda a definição da métrica.

Em geral, condições sobre uma agregação precisam de HAVING ou de uma CTE posterior. NULL também exige atenção: COUNT(coluna) ignora nulos, enquanto COUNT(*) conta linhas. No editor local, a consulta é somente leitura sobre uma cópia em memória, com limites de trabalho e tamanho. SQLite e Spark SQL compartilham parte da linguagem, mas datas, tipos e algumas funções diferem.

## Exemplo explicado

```sql
SELECT canal,
       COUNT(*) AS pedidos,
       SUM(valor_centavos) AS receita_centavos
FROM silver_vendas
WHERE status = 'concluida'
GROUP BY canal
HAVING COUNT(*) >= 10
ORDER BY receita_centavos DESC;
```

O grão dessa Silver é pedido de um produto, portanto COUNT(*) conta pedidos. Essa equivalência não vale para o caso de vários itens da aula seguinte.

## Experimente

Rode a consulta no editor. Retire HAVING e some a receita dos canais. Compare com o total sem GROUP BY. Inclua cancelados e explique a mudança, sem chamar essa soma de receita de concluídos. Execute a versão Spark no notebook 01.

## Resultado esperado

A soma dos grupos sem HAVING coincide com o total da mesma população. Com HAVING, grupos podem ser excluídos e a soma deixa de representar toda a receita.

## Erros comuns

Filtrar status depois de somar; colocar SUM no WHERE; arredondar cada linha antes de somar; achar que LIMIT seleciona o período da análise.

## Desafio

Escreva uma consulta de taxa de cancelamento por canal. Defina numerador e denominador e use multiplicação por 100.0 para evitar divisão inteira no SQLite.

## Critério de conclusão

Você explica WHERE versus HAVING e reconcilia uma agregação com o total da mesma população.

## Referências

Referências: livros de BI e engenharia; [Spark SQL](https://spark.apache.org/docs/latest/sql-ref.html).
