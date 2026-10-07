# Projeto 01 · Um lakehouse que merece confiança

**Objetivo:** construir e explicar um fluxo de vendas com contratos, versionamento e métricas reconciliadas. **Trilhas:** fundamentos, engenharia, governança. **Tempo sugerido:** 4–6 horas depois das aulas. **Ambiente:** local para prototipar; Databricks para evidência Delta/Jobs.

## Enunciado

A fonte tem 720 pedidos fictícios, uma versão corrigida e seis registros inválidos. O gestor quer receita diária sem cancelamentos, com rastreabilidade das exclusões. Você precisa impedir publicação se as contagens ou os centavos não reconciliarem.

## Entregas

1. Um contrato com grão, chave, versão, campos, nulidade e domínios de status.
2. Bronze, Silver, Gold, quarentena e versões substituídas, com regra de destino explicada.
3. Evidência local de 727 = 720 + 6 + 1 e de receita Gold = Silver de concluídos em centavos.
4. Reprocessamento do mesmo lote, demonstrando conteúdo estável e não apenas contagem.
5. Ficha de privilégio, namespace, retenção e comportamento em falha.
6. Se tiver conta: notebook 02/03/07 executados e um run de Job com dependências. Sem conta, registre essa parte como pendente.

## Caminho orientado

Comece pelo app Pipeline e qualidade. Leia f04, e01 e e03. Escreva o contrato antes de alterar código. Use o gerador padrão para reproduzir as contagens. Depois acrescente uma atualização antiga, uma nova chave e uma atualização mais recente inválida. Preserve evidência da fonte; não converta erro em zero.

Na conta de estudo, escolha catálogo autorizado no notebook 00. Execute 02, 03 e 07, nessa ordem. O 03 usa uma tabela incremental própria e começa de um snapshot para tornar a aula repetível; não mistura o destino do 02. Não altere tabelas de outras pessoas. Registre a versão Delta e o gate executado. Se o Job falhar, explique a causa antes de adicionar retry.

## Critérios verificáveis

| Critério | Evidência | Pontos |
|---|---|---|
| Contrato explícito e coerente | Documento com exemplos válidos e inválidos | 20 |
| Reconciliação de linhas e dinheiro | Asserts/queries e parâmetros | 25 |
| Reprocessamento estável | Comparação completa antes/depois | 20 |
| Erro e quarentena rastreáveis | Motivo e procedimento de correção | 15 |
| Governança e operação | Matriz de acesso e runbook | 20 |

**Conclusão recomendada:** pelo menos 80/100 e nenhum critério de reconciliação em aberto. A nota é uma rubrica pessoal, não certificação oficial.

## Extensão

Modele devoluções sem apagar o pedido original. Escolha entre evento de estorno e atualização de status; explique o efeito sobre receita histórica. Acrescente um caso de teste que falharia se sua regra fosse implementada incorretamente.

## Evidência mínima

Salve contrato, queries, semente e versão do código. Screenshots devem mostrar contexto sem tokens nem dados privados. Não inclua logs de conta ou outputs completos no repositório. Consulte as soluções orientadas para comparar raciocínio somente depois de entregar sua proposta.
