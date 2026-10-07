+++
id = "s05-desempenho"
title = "Investigue desempenho com um experimento justo"
track = "sql-bi"
level = "Avançado"
version = "2.0"
prerequisites = ["s04-dashboard", "f05-reprodutibilidade"]
sources = ["bi-livro", "engenharia-livro", "oficial"]
objectives = ["Ler plano e procurar trabalho desnecessário", "Planejar benchmark sem confundir cache e ganho real"]
lab = "Notebook 05 e análise EXPLAIN guiada"
+++

# Investigue desempenho com um experimento justo

## Problema

Uma consulta fica mais rápida depois de executada pela segunda vez. Isso não comprova que uma alteração no SQL, Photon ou outra configuração trouxe o ganho: o cache e o aquecimento podem explicar a diferença.

## Conceito

Desempenho depende de volume lido, filtros, arquivos, estatísticas, cardinalidade de joins, shuffle, compute e concorrência. `EXPLAIN` ajuda a entender o plano; o perfil de execução traz trabalho efetivo. Selecione só as colunas necessárias, filtre cedo quando a semântica permitir e evite transferir tabelas grandes para o driver.

Photon é uma tecnologia de execução do Databricks, não uma biblioteca ativada por este app. SQL warehouse e Spark local são ambientes diferentes. Em tabelas pequenas, diferenças de milissegundos têm pouco valor como evidência sobre escala. Estratégias de organização e otimização de Delta devem seguir recomendações atuais, compatibilidade do ambiente e medidas reais.

## Exemplo explicado

Compare uma consulta que agrega depois de um JOIN desnecessário com outra que agrega diretamente a fato. Antes de comparar tempo, valide a equivalência dos resultados em centavos e contagens. Depois use EXPLAIN, anote compute e faça repetições com ordem alternada. Se uma versão muda a população, ela deixou de ser uma otimização da mesma pergunta.

## Experimente

Rode EXPLAIN sobre as consultas do notebook 05 no Databricks. Identifique scans, joins e agregações. Monte uma ficha com volume, cache, compute, concorrência, número de repetições e mediana. Não atribua o resultado do SQLite local a Photon.

## Resultado esperado

Você produz um diagnóstico do plano e um protocolo reproduzível. O projeto não fornece um percentual universal de ganho nem apresenta um benchmark sintético pequeno como medição empresarial.

## Erros comuns

Comparar resultados diferentes; medir só uma execução; desativar controles para ganhar velocidade; particionar demais uma tabela pequena; tomar qualquer cache hit como redução de custo de ponta a ponta.

## Desafio

Escolha uma hipótese concreta, como reduzir colunas lidas, e defina o critério que poderia refutá-la. Registre também uma hipótese que não pode ser testada no seu ambiente.

## Critério de conclusão

Seu relatório separa equivalência semântica, tempo medido e explicação provável do ganho.

## Referências

Referências: BI e engenharia; [otimização de desempenho](https://docs.databricks.com/aws/en/optimizations/).
