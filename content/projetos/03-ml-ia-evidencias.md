# Projeto 03 · Modelos e assistência com evidências

**Objetivo:** tomar uma decisão com previsão e classificação, depois construir uma busca de estudo avaliada. **Trilhas:** ML, IA e governança. **Tempo sugerido:** 6–8 horas. **Ambiente:** local; MLflow opcional em conta.

## Parte A · Decisão preditiva

Defina alvo, horizonte e instante de decisão para receita de amanhã e risco de atraso antes da viagem. Registre baseline, features e corte temporal. Compare o Ridge com repetir ontem usando o mesmo teste. Compare Brier da classificação com prevalência de treino. Uma derrota do modelo é um resultado válido.

Avalie limiares 0,2/0,5/0,8 e interprete matriz de confusão. Use custos ilustrativos ou explicite suas próprias premissas. Para escolher um limiar como proposta de uso, faça uma validação temporal separada e congele antes de abrir o teste. A exploração do slider no teste é didática e não uma seleção imparcial.

Documente por que `duracao_real_min` fica fora das features. Desloque a distância para estudar PSI e explique por que esse sinal não comprova queda de qualidade sem novos rótulos. Escreva um plano de monitoramento e rollback.

## Parte B · Assistência de estudo

Use somente aulas próprias do catálogo. Crie dez perguntas com documento esperado, incluindo paráfrases. Acrescente duas perguntas sem resposta e uma tentativa de instrução adversarial dentro de um documento. Avalie recall@k da recuperação separadamente de fundamentação e abstenção de respostas manuais.

O app recupera por TF-IDF e exibe trechos; não executa geração por LLM. Se você posteriormente integrar um modelo, essa será uma extensão com autenticação, orçamento, tratamento de dados e avaliação próprios. Não apresente o benchmark lexical como qualidade de um LLM que não rodou.

## Entregas

1. Ficha de experimento com versão, semente, datas, baseline e métricas.
2. Tabela de disponibilidade das features e evidência de corte temporal.
3. Política de limiar/custos, monitoramento e rollback.
4. Conjunto de perguntas e relatório de recuperação por tipo de caso.
5. Três respostas manuais com citações e uma abstenção fundamentada.
6. Business case simples com capacidade potencial, custo e revisão humana.

## Rubrica

| Critério | Evidência | Pontos |
|---|---|---|
| Protocolo temporal e baseline | Ficha e datas sem sobreposição | 25 |
| Decisão e custos | Matriz e política de limiar | 20 |
| Observabilidade do modelo | Drift distinto de desempenho | 15 |
| Recuperação e evidências | Casos, recall e citações válidas | 25 |
| Supervisão e valor | Limites de ação e premissas | 15 |

**Conclusão recomendada:** pelo menos 80/100, sem vazamento temporal nem citação inventada.

## Extensão

Troque TF-IDF por um índice semântico autorizado e compare no conjunto congelado. Controle acesso antes de recuperar, versionamento do índice, custo e atualização do corpus. Proponha um estudo em MLflow sem publicar serving automaticamente.
