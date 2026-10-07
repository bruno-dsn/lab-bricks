+++
id = "m02-temporal"
title = "Evite vazamento temporal nas features"
track = "machine-learning"
level = "Intermediário"
version = "2.0"
prerequisites = ["m01-baseline"]
sources = ["ml-livro", "oficial"]
objectives = ["Construir features disponíveis no instante da decisão", "Separar treino e teste antes de ajustar transformações"]
lab = "Previsão de vendas e ML e classificação"
+++

# Evite vazamento temporal nas features

## Problema

Um modelo parece excelente porque recebeu a duração real da entrega antes de prever se haveria atraso. Essa coluna só existe depois da viagem: o experimento aprendeu uma informação indisponível na decisão.

## Conceito

Vazamento acontece quando treino ou avaliação usam informações que não estariam disponíveis no uso real. Em séries, calcule `shift(1)` antes da média móvel. Ajuste scaler, imputação e seleção no treino. Em eventos datados, reserve datas inteiras para teste para impedir mistura temporal.

Feature Store ou Feature Engineering podem organizar features e reutilização. Para casos com histórico, point-in-time correctness significa recuperar a versão disponível até o instante de referência, sem juntar uma atualização futura. A infraestrutura ajuda, mas a definição correta de disponibilidade ainda é responsabilidade do projeto.

## Exemplo explicado

```python
media_7 = receita.shift(1).rolling(7).mean()
```

Na classificação de entregas, a lista permitida contém distância, volumes, hora de pico, previsão de chuva e dia da semana. `duracao_real_min` fica no dataset como exemplo negativo e jamais entra em `FEATURES`. A chuva é uma previsão disponível antes da viagem, não a chuva observada depois.

## Experimente

Abra ML e classificação. Leia as colunas e compare com FEATURES no módulo. Inspecione as datas: fim do treino deve preceder início do teste. Descreva quando cada feature fica disponível. No Ridge, localize o scaler dentro do pipeline ajustado somente no treino.

## Resultado esperado

Não há data de teste em treino. O modelo recebe somente cinco features pré-decisão; a duração real permanece excluída. Uma tabela de disponibilidade explica o papel de cada coluna.

## Erros comuns

Separar aleatoriamente eventos temporais; fazer normalização antes do corte; usar uma coluna calculada com todo o futuro; achar que remover o alvo basta para eliminar vazamento.

## Desafio

Desenhe uma tabela de features históricas com `cliente_id`, `valid_from` e valor. Mostre uma condição temporal de JOIN que impediria usar uma atualização futura.

## Critério de conclusão

Você demonstra corte temporal e justifica a disponibilidade de todas as features no instante da previsão.

## Referências

Fonte: livro ML; [Feature Engineering no Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/feature-store/uc/).
