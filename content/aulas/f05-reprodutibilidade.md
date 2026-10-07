+++
id = "f05-reprodutibilidade"
title = "Transforme uma experiência em evidência"
track = "fundamentos"
level = "Iniciante"
version = "2.0"
prerequisites = ["f04-contrato"]
sources = ["ml-livro", "engenharia-livro", "oficial"]
objectives = ["Registrar dados, parâmetros e versão", "Distinguir resultado testado de plano futuro"]
lab = "README, testes e docs de validação"
+++

# Transforme uma experiência em evidência

## Problema

Um colega obtém um resultado diferente. Vocês usaram sementes, dependências ou filtros distintos? Sem registro, uma melhoria aparente pode ser apenas outro conjunto de dados.

## Conceito

Reprodutibilidade exige fonte, versão do código, parâmetros, dependências e procedimento. Os geradores são determinísticos para a mesma semente. O lock fixa dependências Python. Os notebooks `.py` são a fonte canônica dos `.ipynb`; a exportação remove saídas que poderiam conter dados privados.

Evidência tem escopo: testes locais comprovam comportamentos locais. Uma transformação validada em Spark local não prova permissões Unity Catalog, transações Delta ou sucesso de um Job em uma conta. Registre separadamente testes locais, validação Spark e execução Databricks.

## Exemplo explicado

```bash
python scripts/verify_project.py
python -m pytest
python scripts/export_notebooks.py
```

A primeira verificação procura inconsistências, links quebrados, saídas e padrões de segredo, incluindo histórico Git disponível. O pytest verifica cenários de comportamento. A exportação sincroniza formatos; não executa os notebooks no Databricks.

## Experimente

Escolha uma métrica e anote semente, tamanho da fonte, filtros e commit. Rode novamente e compare. Altere a semente, mantendo o contrato. Leia docs/VALIDACAO_DATABRICKS.md e preencha evidências somente depois de uma execução real.

## Resultado esperado

A mesma configuração reproduz tabelas e métricas. Mudanças de semente afetam números, mas os contratos e testes de invariantes continuam válidos. O relatório distingue o que foi executado do que ainda requer conta.

## Erros comuns

Guardar screenshots sem parâmetros; chamar uma importação de notebook de execução validada; incluir `mlruns`, caches ou tokens no Git; apagar falhas do relatório para melhorar a aparência.

## Desafio

Crie uma ficha de experimento de seis campos e registre um resultado ruim com a mesma clareza de um resultado bom.

## Critério de conclusão

Outra pessoa consegue reproduzir sua observação e identificar quais dependências ou serviços ainda faltam.

## Referências

Referências: ML e engenharia fornecidos; [MLflow Tracking](https://mlflow.org/docs/latest/ml/tracking/).
