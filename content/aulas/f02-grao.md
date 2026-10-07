+++
id = "f02-grao"
title = "Defina o grão antes de contar"
track = "fundamentos"
level = "Iniciante"
version = "2.0"
prerequisites = ["f01-mapa"]
sources = ["bi-livro", "engenharia-livro"]
objectives = ["Distinguir pedido, item e unidade", "Escolher chave e regra para uma métrica"]
lab = "Pipeline e qualidade e BI e modelagem"
+++

# Defina o grão antes de contar

## Problema

O relatório diz “vendas: 400”, mas ninguém sabe se são pedidos, itens ou unidades. Duas consultas podem estar corretas e ainda responder a perguntas diferentes. Precisamos declarar o que cada linha representa.

## Conceito

Grão é a unidade representada por uma linha. No primeiro caso do Lab Bricks, uma venda tem um único produto e a chave é `venda_id`. No segundo caso, um pedido pode ter vários itens: `pedido_id` identifica o pedido, `item_id` identifica uma linha e `quantidade` conta unidades. Uma dimensão descreve clientes ou produtos; uma tabela de fatos registra eventos mensuráveis.

Defina também população, período, status e unidade monetária. Receita aqui considera pedidos concluídos. A margem bruta do segundo caso subtrai o custo das mercadorias, sem despesas, tributos ou frete; não deve ser chamada de lucro líquido.

## Exemplo explicado

Se um pedido tem três linhas, cada uma com duas unidades, ele representa um pedido, três itens e seis unidades. Após um JOIN com itens, `COUNT(*)` retorna três. `COUNT(DISTINCT pedido_id)` retorna um. Somar o valor total do pedido em cada linha multiplicaria a receita por três.

## Experimente

Abra BI e modelagem. Inspecione as quatro tabelas. Rode o exemplo “Grão: linhas versus pedidos”. Compare `linhas`, `pedidos` e o indicador de unidades. Escreva um contrato de cinco linhas: grão, chave, filtro de status, período e fórmula de receita.

## Resultado esperado

No cenário padrão de 180 pedidos existem 16 cancelados e 164 concluídos. A contagem de linhas de itens concluídos é maior que 164. Alterar a semente pode alterar itens e valores, mas não a regra de cancelamento dessa fonte sintética.

## Erros comuns

Usar COUNT(*) após um JOIN e chamar o resultado de clientes ou pedidos; confundir quantidade com linhas; misturar centavos e reais; remover cancelados da fonte em vez de filtrá-los na métrica.

## Desafio

Crie uma métrica de ticket médio: receita de concluídos dividida por pedidos concluídos distintos. Explique por que dividir pelas linhas de itens responde outra pergunta.

## Critério de conclusão

Seu contrato permite que outra pessoa reproduza o indicador e explica por que o JOIN muda a contagem de linhas.

## Referências

Referências conceituais: Business Intelligence with Databricks SQL e guia de engenharia fornecidos. As tabelas e regras desta aula são exemplos originais do Lab Bricks.
