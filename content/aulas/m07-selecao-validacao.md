+++
id = "m07-selecao-validacao"
title = "Escolha modelo e limiar sem consumir o teste"
track = "machine-learning"
level = "Avançado"
version = "2.0"
prerequisites = ["m03-classificacao", "m06-features-temporais"]
sources = ["ml-acao-livro", "ml-livro", "oficial"]
objectives = ["Separar aprendizado, seleção e avaliação final", "Congelar uma política escolhida na validação"]
lab = "ML e ciclo completo; notebook 11"
+++

# Escolha modelo e limiar sem consumir o teste

## Problema

Você experimenta dez modelos e escolhe aquele que tem menor custo no teste. O mesmo conjunto escolheu o vencedor e avaliou o vencedor. A métrica final passa a refletir a sua busca, além do desempenho do modelo.

## Conceito

O treino ajusta parâmetros do modelo e transformações como o scaler. A validação orienta escolhas: features, hiperparâmetros, modelo e limiar. O teste final avalia a política depois que essas escolhas foram congeladas. No laboratório, datas inteiras mantêm a ordem: primeiras 60% para treino, próximas 20% para validação e últimas 20% para teste.

Esse protocolo é didático. Num problema real, considere a disponibilidade dos rótulos, horizontes que se sobrepõem, períodos sem observações e mudanças de regime. Uma feature que ficou pronta depois da decisão continua sendo vazamento, mesmo com três partições. O AutoML pode fornecer candidatos e uma baseline inicial; não substitui a inspeção do protocolo.

## Exemplo explicado

São comparados três candidatos: baseline de prevalência e regressões logísticas com C igual a 0,1 e 1. Cada um é treinado somente no primeiro período. Na validação, 17 limiares entre 0,1 e 0,9 avaliam o custo ilustrativo de R$ 5 por falso positivo e R$ 30 por falso negativo.

Ordenamos pelo custo, Brier, nome do modelo e limiar para que empates tenham uma regra fixa. Essa regra é definida antes de olhar o teste. O vencedor pode ser a baseline. Sem retreinar após a seleção, aplicamos o modelo e o limiar congelados ao teste final; assim, os resultados correspondem exatamente à política selecionada.

## Experimente

Abra ML e ciclo completo e examine o ranking da validação. Registre a escolha antes de interpretar o custo do teste. Execute o notebook 11. Compare os períodos e confirme que nenhum dia foi dividido. Mude a semente como experiência didática e descreva como a amostra altera a decisão.

## Resultado esperado

Com 600 entregas e 60 datas, o corte produz 360/120/120 linhas. O scaler de cada candidato aprende no treino. O teste não participa do ranking. Alterar apenas seus rótulos muda a avaliação final, mas não pode mudar o candidato nem o limiar escolhido.

## Erros comuns

Escolher C ou limiar no teste; ajustar o scaler em toda a amostra; tentar sementes até aparecer uma vitória; esconder uma baseline vencedora; retreinar com validação sem declarar que o artefato avaliado mudou.

## Desafio

Planeje uma validação por janelas temporais dentro do período de desenvolvimento. Reserve um teste final independente. Declare quando os rótulos chegam e qual intervalo precisa ser separado entre janelas para evitar sobreposição de informação.

## Critério de conclusão

Você entrega ranking com origem dos dados, regra de desempate, política congelada e avaliação final, e demonstra que os rótulos do teste não interferem na seleção.

## Referências

Referência conceitual: Databricks ML in Action, capítulo 6. [MLflow 3](https://docs.databricks.com/aws/en/mlflow/mlflow-3-install) e [validação cruzada do scikit-learn](https://scikit-learn.org/stable/modules/cross_validation.html). Protocolo, dados e candidatos próprios.
