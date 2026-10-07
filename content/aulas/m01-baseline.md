+++
id = "m01-baseline"
title = "Comece pelo problema e por uma baseline"
track = "machine-learning"
level = "Intermediário"
version = "2.0"
prerequisites = ["f05-reprodutibilidade", "s01-agregacoes"]
sources = ["ml-livro", "mit-relatorio"]
objectives = ["Definir alvo e momento de previsão", "Comparar com uma regra simples"]
lab = "Previsão de vendas; notebook 04"
+++

# Comece pelo problema e por uma baseline

## Problema

A loja quer planejar capacidade para amanhã. Treinar um modelo é apenas uma parte: precisamos decidir o alvo, o momento de previsão, o horizonte e o custo de errar.

## Conceito

Baseline é uma referência simples que qualquer melhoria deve superar sob o mesmo protocolo. Para receita diária, repetir o dia anterior é uma baseline. Ridge usa lags, média móvel defasada e calendário. Uma métrica como MAE mede erro na unidade do alvo; resultados precisam de contexto de negócio.

AutoML pode acelerar a exploração, mas não corrige automaticamente vazamento, alvo inadequado ou definição ruim do teste. Não é requisito para executar este laboratório. Primeiro faça um processo pequeno e verificável; depois considere outras famílias de modelos, usando os mesmos cortes e critérios.

## Exemplo explicado

No app, os últimos 14 dias ficam para teste. A avaliação é de um dia à frente: quando prevê cada dia, a receita dos dias anteriores já é conhecida. Isso difere de fazer hoje uma previsão fechada de todas as próximas duas semanas, que exigiria tratar lags futuros de outro modo.

## Experimente

Abra Previsão de vendas. Registre MAE da baseline e do Ridge para 7, 14 e 21 dias de teste. Explique por que os resultados podem mudar. Rode o notebook 04 e, se MLflow estiver autorizado, registre parâmetros e métricas do experimento.

## Resultado esperado

Você obtém duas métricas comparáveis e datas de treino/teste. O Ridge pode ganhar ou perder; o laboratório não escolhe uma semente para prometer melhoria universal.

## Erros comuns

Chamar uma previsão retrospectiva de planejamento real; comparar modelos em testes diferentes; trocar MAE por outra métrica depois de ver o vencedor; usar AutoML como prova de validade.

## Desafio

Proponha uma baseline semanal que repete o mesmo dia da semana anterior. Compare com o Ridge sem alterar o conjunto de teste.

## Critério de conclusão

Seu relatório inclui alvo, horizonte, instante da decisão, baseline, corte e métrica, inclusive quando o modelo perde.

## Referências

Fontes: ML e relatório empresarial; [scikit-learn Dummy estimators](https://scikit-learn.org/stable/modules/model_evaluation.html#dummy-estimators).
