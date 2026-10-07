+++
id = "f01-mapa"
title = "Escolha seu ambiente e entenda o mapa"
track = "fundamentos"
level = "Iniciante"
version = "2.0"
prerequisites = []
sources = ["ebook-original", "engenharia-livro", "oficial"]
objectives = ["Distinguir execução local de execução no Databricks", "Localizar tabelas, compute e notebooks"]
lab = "Comece por aqui e notebook 00"
+++

# Escolha seu ambiente e entenda o mapa

## Problema

Uma loja tem planilhas, pedidos em JSON e um painel com números inconsistentes. Antes de escolher uma ferramenta, precisamos saber onde o dado vive, quem pode acessá-lo e que pergunta será respondida. Um notebook sozinho não resolve essas decisões.

## Conceito

O lakehouse reúne armazenamento e processamento analítico com gestão de tabelas. Spark processa dados; Delta acrescenta um log transacional às tabelas; Unity Catalog organiza e controla objetos; um SQL warehouse executa consultas SQL; Jobs coordena tarefas. Esses papéis se relacionam, mas não são equivalentes.

O app local usa Pandas, SQLite e scikit-learn para experimentar conceitos com dados pequenos. Os notebooks nativos usam Spark e, em algumas atividades, Delta. A Free Edition é uma opção para estudo com limites de compute e recursos; consulte as limitações atuais antes de planejar Jobs ou pipelines. O projeto é independente e não representa um produto oficial Databricks.

## Exemplo explicado

No notebook 00 você escolhe um catálogo autorizado. O projeto cria um schema `lb_` seguido de um hash do usuário atual. A intenção é reduzir colisões entre alunos. O hash não cria uma permissão: o Unity Catalog continua sendo a fronteira de autorização. Duas pessoas com acesso ao mesmo schema podem acessar seus objetos conforme os privilégios.

## Experimente

1. Rode o app local seguindo o README e abra Pipeline e qualidade.
2. Identifique qual parte é armazenamento, transformação e visualização.
3. No Databricks, importe os notebooks, execute o 00 em um catálogo de estudo permitido e registre o catálogo/schema exibidos.
4. Se não tiver uma conta, conclua a experiência local e marque a execução nativa como pendente.

## Resultado esperado

A execução local mostra 727 registros recebidos, 720 pedidos na Silver, seis rejeitados e uma versão substituída no cenário padrão. No Databricks, a evidência inicial é um schema autorizado identificado, não uma alegação de que todo o laboratório foi validado.

## Erros comuns

Confundir uma pasta de notebooks com um pipeline agendado; usar um catálogo de produção para treino; supor que um nome exclusivo protege dados; procurar botões de uma interface antiga descrita em um livro.

## Desafio

Desenhe em cinco caixas o caminho fonte → Bronze → Silver → Gold → decisão. Para cada caixa, escreva onde roda e qual ferramenta exerce a função.

## Critério de conclusão

Você explica Spark, Delta, Unity Catalog, SQL warehouse e Jobs com uma frase cada e registra quais atividades foram efetivamente executadas.

## Referências

Fontes conceituais: e-book original e guia de engenharia fornecidos. Atualização: [Free Edition](https://docs.databricks.com/aws/en/getting-started/free-edition) e [limitações](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations).
