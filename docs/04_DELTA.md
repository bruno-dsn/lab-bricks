# Quando chegam alterações

Um pedido já existente teve a quantidade corrigida. Outro pedido chegou pela primeira vez. Repetir uma inserção dos dois criaria registros duplicados. O notebook 03 demonstra uma atualização orientada por chave e versão.

## MERGE

```sql
MERGE INTO tabela_de_estudo AS destino
USING lote_incremental AS origem
ON destino.venda_id = origem.venda_id
WHEN MATCHED AND origem.atualizado_em > destino.atualizado_em
  THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *;
```

Uma chave nova é inserida. Para uma chave existente, só uma versão mais recente substitui os valores. O lote de exemplo tem as mesmas colunas e tipos da tabela de destino; usar `SET *` fora desse contrato precisa de cuidado.

Antes de atualizar, o notebook confirma que o lote tem uma única linha por chave. Ele escreve em `silver_incremental`, uma cópia de estudo, para manter a Silver e a Gold do primeiro pipeline como estavam.

## Provar a idempotência

Executamos o mesmo MERGE duas vezes. Depois da primeira execução, guardamos um snapshot pequeno e ordenado. Depois da segunda, comparamos todo o conteúdo. A contagem também precisa ser a original mais um: o lote tem um pedido novo e uma atualização.

Só conferir a contagem seria insuficiente: os valores poderiam mudar sem aparecer uma linha nova. Só conferir a soma também seria insuficiente: duas alterações poderiam se compensar.

## Histórico e consulta de versões

Delta registra operações e versões. O notebook lê a versão anterior à atualização e mostra o pedido antes da mudança. Essa consulta depende dos arquivos e logs ainda retidos. Um histórico de versões não substitui uma política de backup e retenção.

O laboratório não roda comandos de limpeza. Estude a retenção na [documentação oficial](https://docs.databricks.com/aws/en/tables/history) antes de experimentar remoção de arquivos.

## O que falta para uma ingestão contínua

Este exemplo recebe um lote em memória. Uma solução contínua precisa identificar lotes, tratar entregas atrasadas, definir a origem do timestamp, aplicar o MERGE na tabela oficial e atualizar os agregados. Também precisa de observação de falhas e reexecução.

Se o notebook 03 rodar novamente do início, ele restaura a tabela de demonstração antes do lote. Se apenas a célula do MERGE rodar outra vez, ela exercita a idempotência. Explique essa diferença no seu relatório de estudo.
