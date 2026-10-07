+++
id = "e01-medallion"
title = "Separe preservação, qualidade e consumo"
track = "engenharia"
level = "Intermediário"
version = "2.0"
prerequisites = ["f04-contrato", "s01-agregacoes"]
sources = ["engenharia-livro", "bi-livro", "oficial"]
objectives = ["Atribuir responsabilidades às camadas", "Definir reconciliações para uma publicação"]
lab = "Pipeline e qualidade; notebook 02"
+++

# Separe preservação, qualidade e consumo

## Problema

Uma mudança de regra exige recalcular o painel. Se a fonte original foi descartada, ninguém consegue explicar como o número anterior foi produzido nem reconstruir o histórico.

## Conceito

Bronze preserva o que chegou; Silver normaliza e aplica regras; Gold prepara métricas de consumo. Essa separação é uma convenção arquitetural, não uma função mágica de três pastas. Uma organização pode adotar outros nomes desde que preserve responsabilidades e rastreabilidade.

No Lab Bricks, as versões substituídas e a quarentena ficam explícitas. Uma tabela Silver pode conter concluídos e cancelados porque ambos são eventos válidos. A Gold de receita filtra concluídos. Publicar significa satisfazer contratos e critérios de qualidade, não apenas conseguir escrever arquivos.

## Exemplo explicado

O padrão local recebe 727 linhas. Uma atualização substitui uma versão, seis linhas são inválidas e 720 pedidos ficam na Silver. A Gold diária deve satisfazer `SUM(gold.receita_centavos) = SUM(silver.valor_centavos WHERE status='concluida')`. Em produção, também registraríamos lote, origem e timestamp de ingestão.

## Experimente

Abra cada etapa no app. No notebook 02, inspecione as tabelas e rode as reconciliações. Explique a diferença entre reter um cancelamento válido e rejeitar um status desconhecido. Faça uma ficha com produtor, consumidor, chave e atualização de cada camada.

## Resultado esperado

As contas de linhas e dinheiro fecham. A Bronze permite investigar o erro sem reconstruir dados inventados. Reexecutar o exemplo completo recria somente suas tabelas de estudo.

## Erros comuns

Transformar Bronze em depósito sem metadados; tratar Gold como sinônimo de dashboard; descartar rejeitados; executar overwrite sobre um destino que não é do laboratório.

## Desafio

Proponha retenção da Bronze e quarentena para uma fonte diária. Diga quais dados de auditoria devem sobreviver e quem pode ler os registros.

## Critério de conclusão

Você consegue rastrear um indicador até os registros e explicar o limite de cada camada.

## Referências

Fontes: engenharia e BI; [medallion architecture](https://docs.databricks.com/aws/en/lakehouse/medallion).
