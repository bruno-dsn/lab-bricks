+++
id = "m04-mlops"
title = "Registre, versione e promova com evidências"
track = "machine-learning"
level = "Avançado"
version = "2.0"
prerequisites = ["m03-classificacao", "f05-reprodutibilidade"]
sources = ["ml-livro", "oficial"]
objectives = ["Separar run de experimento, registro e serving", "Definir promoção e rollback de modelo"]
lab = "Notebook 04; roteiro de registro no guia"
+++

# Registre, versione e promova com evidências

## Problema

Um modelo novo foi treinado, mas ninguém consegue saber quais dados o produziram nem por que substituiu o anterior. MLOps organiza a passagem de uma experiência para um serviço operável.

## Conceito

Um run do MLflow registra parâmetros, métricas e artefatos. O registry organiza versões de modelos; serving executa inferência. São etapas distintas: registrar um arquivo não implanta automaticamente um endpoint. Em Unity Catalog, nomes usam catálogo.schema.modelo e aliases podem apontar para versões aprovadas.

O livro de 2023 descreve práticas e APIs de sua época. O fluxo atual em Unity Catalog usa aliases e tags no lugar dos estágios legados do Workspace Model Registry. Um alias como Champion é uma convenção da equipe, não uma comprovação de qualidade. Promoção exige contrato de entrada, assinatura, teste, permissão e avaliação de rollback.

## Exemplo explicado

Um registro útil inclui commit, versão de dados, datas do corte, FEATURES, semente, baseline e métricas. Antes de mudar um alias, compare no mesmo protocolo e verifique a assinatura. Um cenário pode ser reproduzido em MLflow sem publicar serving nem enviar dados a serviços externos.

## Experimente

Execute o notebook 04. Se sua conta permitir Tracking, observe o run e salve o link. Leia o roteiro de aliases em docs/MLFLOW_E_OPERACAO.md. Crie uma ficha de promoção sem executar publicação em produção. Teste inferência local com um input fora do schema para definir falha controlada.

## Resultado esperado

O experimento tem parâmetros e métricas identificáveis, ou registra que Tracking não estava disponível. A ficha diferencia modelo treinado, registrado e servido. Nenhuma implantação ocorre automaticamente ao abrir o app.

## Erros comuns

Promover pela menor métrica sem baseline; usar credencial pessoal em automação; não versionar features; considerar um alias garantia de disponibilidade; logar dados sensíveis como exemplos.

## Desafio

Escreva um rollback: versão anterior, gatilho, aprovador, consumidores e verificação depois da troca de alias.

## Critério de conclusão

Outra pessoa consegue localizar o run, reproduzir a avaliação e entender o critério de promoção e reversão.

## Referências

Fonte: ML; [lifecycle em Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/) e [MLflow](https://mlflow.org/docs/latest/).
