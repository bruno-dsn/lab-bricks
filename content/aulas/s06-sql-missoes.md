+++
id = "s06-sql-missoes"
title = "JOIN, CTE e janela: escreva e confira"
track = "sql-bi"
level = "Intermediário"
version = "3.0"
prerequisites = ["s03-janelas"]
sources = ["bi-livro", "oficial"]
objectives = ["Executar a prática e explicar o resultado", "Identificar um erro e provar a correção"]
lab = "Missões SQL e ex11_janela_sql"
+++

# JOIN, CTE e janela: escreva e confira

## Problema
Seu dashboard dobrou o faturamento depois de juntar itens e pagamentos. Uma consulta pode executar sem erro e ainda calcular a população errada.

## Conceito
Um pedido com dois itens e dois pagamentos gera quatro combinações quando as duas tabelas filhas entram no mesmo JOIN. O SUM repete tanto itens quanto pagamentos. Agregue cada filha em uma CTE no grão de pedido e só depois faça o JOIN. LEFT JOIN mantém pedidos sem correspondência; COALESCE transforma um total ausente em zero quando essa é a regra de negócio. Na janela acumulada, agregue primeiro no grão diário e declare ROWS para tornar o quadro explícito.

## Exemplo explicado
A missão cte tem pedido 1 com itens de 1.200 e 800 centavos e pagamentos de 900 e 1.100. A resposta correta é 2.000 e 2.000. O JOIN cru produz 4.000 e 4.000. SUM(DISTINCT valor) não resolve: dois itens legítimos podem custar exatamente o mesmo.

## Experimente
Abra Missões SQL, leia as tabelas e escreva as três consultas. Use nomes de colunas e ordem exigidos no enunciado. Depois implemente ex11_janela_sql e confira com o SQLite de leitura.

## Resultado esperado
Os pedidos 1, 2 e 3 aparecem com receitas 2.000, 1.500 e zero. O acumulado diário termina em 4.000 centavos.

## Erros comuns
INNER JOIN que elimina pedidos sem itens; SUM(DISTINCT) que descarta valores legítimos; janela sobre itens quando o indicador tem grão diário. Uma correção precisa explicar a população, não só o número final.

## Desafio
Acrescente dois itens com o mesmo preço ao fixture e mostre por que SUM(DISTINCT) erra. Compare sua solução em Pandas e SQL.

## Critério de conclusão
As três missões passam e você desenha os grãos antes e depois de cada agregação.

## Referências
- Business Intelligence with Databricks SQL; material fornecido, não redistribuído.
- [Documentação oficial atual do Databricks](https://docs.databricks.com/aws/en/)
