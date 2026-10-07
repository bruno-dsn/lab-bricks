+++
id = "e02-delta"
title = "Entenda Delta, histórico e isolamento de escrita"
track = "engenharia"
level = "Intermediário"
version = "2.0"
prerequisites = ["e01-medallion"]
sources = ["engenharia-livro", "bi-livro", "oficial"]
objectives = ["Distinguir arquivo Parquet e tabela Delta", "Inspecionar histórico sem tratar time travel como backup"]
lab = "Notebook 02 e 03"
+++

# Entenda Delta, histórico e isolamento de escrita

## Problema

Dois processos tentam atualizar a mesma tabela. Ler uma pasta de arquivos sem um protocolo transacional não garante que um leitor enxergue um estado coerente durante a escrita.

## Conceito

Delta mantém um log de transações e arquivos de dados. Um commit publica um estado da tabela; leitores utilizam snapshots coerentes e escritas concorrentes seguem controles de conflito. O schema faz parte do contrato. Uma evolução de schema autorizada não deve ser uma aceitação indiscriminada de toda coluna que chegou.

Histórico e time travel permitem investigar versões retidas. Sua disponibilidade depende de retenção do log e dos arquivos. VACUUM pode remover arquivos antigos necessários a versões anteriores; não é uma operação de aula para executar sem revisar retenção e consumidores. Time travel não substitui estratégia de backup e recuperação.

## Exemplo explicado

```sql
DESCRIBE HISTORY silver_vendas;
SELECT COUNT(*) FROM silver_vendas;
```

Execute no schema do notebook. O histórico registra operações e métricas. Para consultar uma versão, escolha uma versão realmente exibida e ainda disponível; não assuma que “VERSION AS OF 0” continuará funcionando para sempre.

## Experimente

Execute os notebooks 02 e 03 em sua conta. Compare histórico antes e depois do MERGE. Leia o schema e identifique campos monetários em centavos. Registre versão, operação e contagem de linhas. Evite comandos de limpeza enquanto estiver estudando versões.

## Resultado esperado

O MERGE registra novas transações e a tabela mantém uma linha vigente por chave no destino incremental. O app local não apresenta histórico Delta: seus resultados são simulações conceituais com DataFrames.

## Erros comuns

Chamar Parquet de Delta; forçar evolução de schema para mascarar um contrato quebrado; usar VACUUM com baixa retenção por copiar um tutorial; testar concorrência sobre uma tabela compartilhada.

## Desafio

Escreva um plano de recuperação após um overwrite acidental: evidências disponíveis, versões retidas, autorização para restaurar e limite do time travel.

## Critério de conclusão

Você identifica log, dados, snapshot e retenção e apresenta um histórico de execução real ou marca essa etapa como pendente.

## Referências

Referências: engenharia e BI; [histórico Delta](https://docs.databricks.com/aws/en/delta/history) e [Delta Lake](https://docs.databricks.com/aws/en/delta/).
