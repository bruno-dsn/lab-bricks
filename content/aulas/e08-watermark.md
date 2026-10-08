+++
id = "e08-watermark"
title = "Streaming: atraso, estado e checkpoint"
track = "engenharia"
level = "Intermediário"
version = "3.0"
prerequisites = ["e04-json-streaming", "e07-cdc-scd2"]
sources = ["spark", "oficial"]
objectives = ["Executar a prática e explicar o resultado", "Identificar um erro e provar a correção"]
lab = "Streaming e atrasos e notebook 15"
+++

# Streaming: atraso, estado e checkpoint

## Problema
Uma venda ocorreu às 10h02, mas chegou depois de eventos das 10h30. Qual regra permite incorporar atraso sem manter estado para sempre?

## Conceito
Tempo do evento descreve quando o fato ocorreu; tempo de processamento, quando o motor recebeu. Watermark deriva do maior tempo observado menos uma tolerância e controla estado de operadores compatíveis. No simulador, cada microbatch usa a fronteira do microbatch anterior; eventos com timestamp menor ou igual são descartados e janelas com fim até essa fronteira são finalizadas. Essa regra por evento é uma simplificação: o Spark pode aplicar descarte segundo o fim da janela, o operador e o modo de saída. Deduplicação local também mantém IDs globais limitados a 1.000; não modela a expulsão de estado completa do Spark.

## Exemplo explicado
Lote A observa 10h20. Com tolerância de dez minutos, lote B usa fronteira 10h10. Um evento de 10h15 pode entrar e um de 10h02 é tardio. Um evento mais novo do lote B só influencia a fronteira do lote seguinte. Um microbatch vazio pode permitir finalização de estado já observado.

## Experimente
Abra Streaming e atrasos, varie a tolerância e leia a auditoria. Faça ex13_watermark. No notebook 15, use um diretório de entrada de estudo, checkpoint exclusivo e o mesmo checkpoint no replay. O validador Spark local executa microbatches em ordem explícita.

## Resultado esperado
Cada evento recebe aceito, duplicado ou atrasado na referência. O replay de um lote já processado não altera totais. O cenário Spark nativo registra seu próprio comportamento, sem exigir que toda borda coincida com a simplificação Pandas.

## Erros comuns
Confundir watermark com espera obrigatória de dez minutos; usar o máximo do lote atual para rejeitar linhas do próprio lote; apagar checkpoint antes de testar replay; depender da ordem de arquivos com a mesma data de modificação.

## Desafio
Crie um evento cujo timestamp está antes da fronteira mas cuja janela termina depois dela. Compare o operador Spark com a regra individual do simulador e documente a diferença.

## Critério de conclusão
Entregue audit por lote, evolução da fronteira, teste de replay e uma comparação honesta entre referência e execução nativa.

## Referências
- [Spark 4.0.1: Structured Streaming](https://spark.apache.org/docs/4.0.1/streaming/apis-on-dataframes-and-datasets.html)
- [Documentação oficial atual do Databricks](https://docs.databricks.com/aws/en/)
