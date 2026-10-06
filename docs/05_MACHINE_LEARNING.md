# Avaliar uma previsão sem usar o futuro

Queremos prever a receita de um dia. Antes de treinar, definimos o momento da previsão: começo do dia, com as vendas de ontem já observadas.

## Uma referência simples

A baseline usa a receita de ontem como previsão para hoje. Ela tem uma regra clara, custa pouco e permite perguntar se a complexidade do modelo trouxe alguma melhoria.

O modelo Ridge usa receita de um dia atrás, receita de sete dias atrás, média dos sete dias até ontem e dia da semana. O objetivo é comparar o procedimento, não demonstrar que um algoritmo sempre ganha.

```python
lag_1 = receita.shift(1)
lag_7 = receita.shift(7)
media_7 = receita.shift(1).rolling(7).mean()
```

O deslocamento ocorre antes da média. Incluir a receita de hoje na média faria o modelo receber parte da resposta que deveria prever.

## O corte respeita o calendário

Os dias finais ficam no teste; os anteriores ficam no treino. O scaler e o modelo são ajustados apenas no treino. No teste, cada previsão usa o passado realmente observado até aquele dia.

Isso permite prever um dia à frente repetidamente. Para simular uma previsão de 14 dias feita no primeiro dia, seria necessário outro procedimento: receitas futuras reais não estariam disponíveis para criar os próximos atrasos.

O código preenche dias sem vendas com zero antes de criar os atrasos. Essa escolha depende da origem: numa empresa real, uma ausência poderia significar falha de ingestão em vez de receita zero. Investigue essa diferença antes de aplicar a regra.

## Interpretar o MAE

MAE é a média da diferença absoluta entre receita observada e prevista. Ele mantém a unidade em reais. Um erro médio de R$ 100 significa uma distância média de R$ 100 por previsão neste conjunto; não significa que todas as previsões erram exatamente esse valor.

Compare o MAE do modelo com o da baseline no mesmo período. Se a baseline vencer, registre a conclusão. Também inspecione o gráfico: um erro médio pode esconder dificuldades em determinados dias.

## Registrar e reproduzir

O notebook permite registrar parâmetros e métricas com MLflow na sessão Databricks; a opção começa desligada. No laboratório local, o resultado é calculado com scikit-learn, sem servidor MLflow.

Registre semente da fonte, tamanho da amostra, features, período de treino, período de teste, métrica e baseline. Estes dados são sintéticos; o experimento verifica o método e não estabelece qualidade para uma loja real.

## Seu relatório

Escreva cinco frases: alvo, momento da previsão, informação disponível, comparação e limitação. Se uma feature depender de vendas ainda não observadas, explique como ela seria obtida antes de incluir o campo.
