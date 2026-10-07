+++
id = "e04-json-streaming"
title = "Leia JSON com schema e avance para Auto Loader"
track = "engenharia"
level = "Intermediário"
version = "2.0"
prerequisites = ["e03-incremental"]
sources = ["engenharia-livro", "oficial"]
objectives = ["Extrair itens de JSON aninhado", "Distinguir tempo de evento, ingestão e execução"]
lab = "Notebook 06; notebook 08 opcional"
+++

# Leia JSON com schema e avance para Auto Loader

## Problema

A origem muda de CSV para eventos JSON com um array de itens. Um evento quebrado não pode simplesmente desaparecer durante explode; precisamos conservar a evidência do erro.

## Conceito

JSON aninhado exige um schema explícito e uma decisão sobre campos ausentes. `from_json` interpreta a estrutura; `explode` transforma itens em linhas. Separe validação do evento e do item. A quarentena deve indicar por que o evento ou item não entrou na Silver.

Streaming processa dados incrementalmente usando estado e checkpoints. Auto Loader descobre arquivos de forma incremental em armazenamento suportado. O trigger `availableNow` processa o que está disponível e termina, útil para uma atividade limitada. Event time é a hora de negócio do evento; processing time é a execução; ingestão é quando o sistema recebeu o dado. Watermark envolve estado e tolerância a atraso, não uma promessa geral de deduplicação eterna.

## Exemplo explicado

O notebook 06 usa quatro mensagens próprias: um pedido com dois itens, um com um item, um JSON malformado e um evento sem itens. Três itens válidos vão para a Silver; duas mensagens entram na quarentena. Cada item preserva o identificador do pedido.

## Experimente

Execute o notebook 06 e confira contagens. Depois leia o 08: ele cria somente um volume de estudo no seu schema, gera arquivos fictícios e define checkpoint próprio. Execute 08 apenas se sua conta permitir volumes e Auto Loader. Repita sem remover checkpoint e observe o avanço.

## Resultado esperado

No caso JSON: quatro mensagens, duas válidas, três itens, duas mensagens rejeitadas. No Auto Loader, a evidência é um stream terminado, tabela acessível e reexecução sem reingerir os mesmos arquivos; precisa ser confirmada em sua conta.

## Erros comuns

Inferir schema diferente a cada lote; perder evento vazio no explode; confundir checkpoint com backup; aplicar expectativas de exactly-once a qualquer integração externa sem avaliar o destino.

## Desafio

Adicione um campo opcional de cupom e um novo item inválido. Escreva como preservar compatibilidade do schema e contabilizar mensagens versus itens.

## Critério de conclusão

Você reconcilia eventos e itens e sabe qual parte foi executada em batch local/nativo e qual exige streaming na conta.

## Referências

Fonte: engenharia; [Auto Loader](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/) e [Structured Streaming](https://spark.apache.org/docs/latest/streaming/index.html).
