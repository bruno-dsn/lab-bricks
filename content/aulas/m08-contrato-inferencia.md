+++
id = "m08-contrato-inferencia"
title = "Leve o modelo à inferência com contrato e evidências"
track = "machine-learning"
level = "Avançado"
version = "2.0"
prerequisites = ["m04-mlops", "m07-selecao-validacao"]
sources = ["ml-acao-livro", "oficial"]
objectives = ["Validar nomes, tipos e domínios de entrada", "Distinguir assinatura, inferência batch e serving"]
lab = "ML e ciclo completo; notebook 11; guia do ciclo ML"
+++

# Leve o modelo à inferência com contrato e evidências

## Problema

O modelo espera distância em quilômetros e cinco features. Um consumidor envia distância negativa, omite chuva ou acrescenta a duração real da entrega. Conseguir chamar `predict` não garante que a entrada representa a mesma experiência de treino.

## Conceito

Um contrato descreve nomes, tipos, domínios, unidades, disponibilidade e comportamento de falha. A assinatura MLflow registra estrutura de entrada e saída; regras de negócio e de tempo ainda precisam de validação própria. Não trate uma assinatura como garantia automática de que toda semântica foi respeitada.

No exemplo, são aceitas somente cinco colunas numéricas, finitas e preenchidas. Distância fica entre 1 e 45 km; volumes são inteiros de 1 a 7; pico e previsão de chuva usam 0/1; dia da semana é inteiro de 0 a 6. Esses limites são o domínio do gerador fictício, não uma regra universal de logística.

Inferência batch processa um conjunto de dados; um endpoint serve solicitações por uma API. Registro, versão, alias e endpoint são objetos distintos. Antes de servir, escolha consumidores, latência, autenticação, orçamento, supervisão e rollback. O laboratório não cria endpoints nem promove aliases ao abrir uma página.

## Exemplo explicado

`validar_entrada` seleciona a ordem canônica das features depois de conferir o conjunto de colunas. Uma coluna extra, inclusive `duracao_real_min`, é rejeitada. O pipeline conserva scaler e regressão juntos, reduzindo diferenças entre transformações de treino e inferência. O resultado local permite ensinar o contrato antes de operar um serviço remoto.

O notebook 11 oferece Tracking opcional em MLflow 3: usa `name`, assinatura, input de exemplo fictício e a URI devolvida pelo log. O modelo carregado precisa reproduzir as probabilidades do modelo original. Esse round-trip é uma evidência do artefato, não de um endpoint já implantado.

## Experimente

Na página ML e ciclo completo, escolha as quatro entradas de inferência. Veja o contrato válido ser aceito e os demais falharem com uma mensagem explicativa. Execute a prática local do notebook. Se a sua conta tiver MLflow 3 e um experimento autorizado, habilite Tracking e registre o run; caso contrário, deixe essa etapa pendente.

## Resultado esperado

Três entradas incompatíveis são rejeitadas. O modelo válido usa as mesmas transformações do treino. Com Tracking habilitado e executado, o modelo recarregado produz as mesmas probabilidades dentro da tolerância numérica e possui assinatura e proveniência registradas.

## Erros comuns

Registrar sem assinatura; mudar unidade silenciosamente; usar um alias sem guardar a versão resolvida; declarar serving feito porque um run existe; copiar padrões antigos de estágios de registry para Unity Catalog.

## Desafio

Escreva um plano de inferência diária com versão fixa, contrato, falhas de dados, tabela de resultados, orçamento e rollback. Para serving, acrescente um teste de latência e autorização a ser executado na conta. Identifique claramente o que foi executado e o que é roteiro.

## Critério de conclusão

Você mostra entrada aceita, falhas de contrato, versão/URI do artefato quando houver Tracking e separa evidências locais de pendências do serviço remoto.

## Referências

Referência conceitual: Databricks ML in Action, capítulo 7. [MLflow 3](https://docs.databricks.com/aws/en/mlflow/mlflow-3-install), [inferência batch](https://docs.databricks.com/aws/en/machine-learning/model-inference) e [Model Serving](https://docs.databricks.com/aws/en/machine-learning/model-serving). Conteúdo original.
