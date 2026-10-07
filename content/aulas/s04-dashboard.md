+++
id = "s04-dashboard"
title = "Modele um dashboard com contrato de métricas"
track = "sql-bi"
level = "Intermediário"
version = "2.0"
prerequisites = ["s03-janelas"]
sources = ["bi-livro", "mit-relatorio", "oficial"]
objectives = ["Definir KPIs com população e período", "Planejar filtros e conferir totais"]
lab = "BI e modelagem; prática AI/BI guiada"
+++

# Modele um dashboard com contrato de métricas

## Problema

Uma direção quer acompanhar vendas. Um painel bonito, com filtros inconsistentes entre gráficos, pode levar a decisões contraditórias. Comece pelo contrato da métrica e pela pergunta do leitor.

## Conceito

Um dashboard útil tem público, decisão, frequência, definições e fonte. Defina receita, pedidos distintos, ticket e margem bruta com a mesma população. Declare se cancelamentos aparecem como indicador separado e qual fuso define a data de negócio. Filtros devem atuar de modo previsível em todos os elementos relevantes.

No Databricks atual, AI/BI dashboards trabalham com datasets, visualizações e controles. O livro de BI descreve interfaces e dashboards de uma época anterior. Use a documentação atual para publicar, compartilhar e entender credenciais de execução; publicar um painel não substitui a revisão de acesso aos dados.

## Exemplo explicado

Para o caso BI: receita = soma de quantidade × preço do item em pedidos concluídos; pedidos = COUNT(DISTINCT pedido_id) nessa população; ticket = receita/pedidos; margem bruta = receita − custo da mercadoria. Uma tabela mensal e um gráfico de receita por categoria são suficientes para a primeira decisão; quinze gráficos não aumentam automaticamente a clareza.

## Experimente

No app, escolha canal e região e compare os indicadores com a tabela de fatos filtrada. No Databricks, execute o notebook 05, crie um dataset consultando as tabelas `bi_*`, acrescente indicadores e um filtro de canal. Registre a consulta e teste o painel com uma segunda combinação de filtros. A publicação é uma etapa manual da sua conta.

## Resultado esperado

Cada cartão concilia com uma consulta da mesma população. A margem é rotulada como bruta e o painel informa dados fictícios. A evidência nativa inclui query, warehouse usado e permissões revisadas.

## Erros comuns

Rotular margem como lucro; usar filtros só em parte dos gráficos; misturar timestamp UTC com data local sem regra; compartilhar credenciais embutidas sem avaliar seu efeito.

## Desafio

Escreva uma ficha de métricas para uma pessoa que nunca viu o projeto. Inclua também uma pergunta que o painel não consegue responder por falta de dados.

## Critério de conclusão

Uma pessoa interpreta corretamente os KPIs, reproduz uma combinação de filtros e conhece as limitações.

## Referências

Fontes: BI e relatório empresarial fornecidos; [AI/BI dashboards](https://docs.databricks.com/aws/en/dashboards/).
