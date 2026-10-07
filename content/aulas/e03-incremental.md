+++
id = "e03-incremental"
title = "Faça reprocessamento sem duplicar eventos"
track = "engenharia"
level = "Intermediário"
version = "2.0"
prerequisites = ["e02-delta"]
sources = ["engenharia-livro", "oficial"]
objectives = ["Distinguir deduplicação de lote e chave", "Tratar atualização antiga e versão nova inválida"]
lab = "Ingestão incremental; notebook 03"
+++

# Faça reprocessamento sem duplicar eventos

## Problema

O arquivo de ontem chega novamente e uma correção de um pedido antigo aparece no lote de hoje. Repetição, atualização e atraso são situações distintas, que precisam de regras distintas.

## Conceito

Idempotência significa que reaplicar a mesma operação preserva o resultado pretendido. No simulador, um manifesto usa ID do lote e hash do conteúdo: mesmo ID e mesmo conteúdo são ignorados; mesmo ID com conteúdo diferente é rejeitado. Isso evita repetir um lote, mas não escolhe a versão vigente de um pedido.

A chave de negócio e o timestamp de atualização decidem a versão. Antes de um MERGE, a origem precisa de no máximo uma linha candidata por chave; múltiplas correspondências tornam a intenção ambígua. Um checkpoint de streaming registra progresso do mecanismo; não é um substituto da chave de negócio nem uma licença para apagar estado.

## Exemplo explicado

No app, lote A recebe a fonte; lote B corrige um pedido e acrescenta um novo; repetir B não adiciona Bronze. Uma versão mais antiga não deve vencer a nova. Já uma atualização mais recente inválida vai para quarentena: o laboratório não restaura silenciosamente uma versão antiga.

## Experimente

Abra Ingestão incremental e ative a repetição de lote. Depois inclua um evento antigo e uma correção inválida. Inspecione manifesto, Silver e rejeitados. No notebook 03, execute dois MERGEs do mesmo lote e compare o conteúdo completo, não apenas COUNT(*).

## Resultado esperado

O destino do notebook 03 tem 721 chaves depois da atualização e do novo pedido; o segundo MERGE mantém o mesmo conteúdo. No simulador, repetição de ID de lote contribui com zero novas linhas e versões antigas ficam substituídas.

## Erros comuns

Usar INSERT para todos os lotes; deduplicar somente por hash de arquivo; confiar só na contagem; excluir checkpoints para resolver uma falha sem entender o reprocessamento.

## Desafio

Descreva como tratar uma origem que reutiliza nomes de arquivo com conteúdo corrigido. Defina identidade do evento, versão e uma trilha de auditoria.

## Critério de conclusão

Você demonstra reaplicação estável e explica três responsabilidades: manifesto, chave/versionamento e checkpoint.

## Referências

Fonte: guia de engenharia; [MERGE Delta](https://docs.databricks.com/aws/en/delta/merge).
