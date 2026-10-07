+++
id = "e05-declarativo"
title = "Declare uma pipeline e suas expectativas"
track = "engenharia"
level = "Avançado"
version = "2.0"
prerequisites = ["e04-json-streaming", "e01-medallion"]
sources = ["engenharia-livro", "oficial"]
objectives = ["Distinguir transformações declarativas de scripts com efeitos", "Planejar expectativas e publicação"]
lab = "pipelines/qualidade_declarativa.py; prática guiada"
+++

# Declare uma pipeline e suas expectativas

## Problema

Uma equipe mantém vários notebooks que escrevem tabelas em ordem manual. Um notebook pode falhar no meio e deixar consumidores com tabelas de momentos diferentes.

## Conceito

Lakeflow Spark Declarative Pipelines descreve tabelas ou views e dependências; o mecanismo planeja atualizações. O código Python atual usa `from pyspark import pipelines as dp`. Definições devem retornar DataFrames, sem chamadas de escrita, acesso externo mutável ou execução de Jobs dentro da função.

Expectativas expressam regras de qualidade. Manter métricas de violações, descartar linhas ou falhar uma atualização são decisões distintas. Descartar sem uma tabela de investigação prejudica rastreabilidade. O exemplo do Lab Bricks materializa uma fonte pequena, separa inválidos e agrega concluídos; usa APIs do Databricks que não estão disponíveis no Spark local 4.0 do projeto.

## Exemplo explicado

```python
from pyspark import pipelines as dp

@dp.materialized_view()
@dp.expect_or_fail("valor_positivo", "valor_centavos > 0")
def silver_exemplo():
    return spark.read.table("bronze_exemplo").where("valido")
```

A expectativa funciona como um contrato adicional sobre uma transformação. Nomes são resolvidos no catálogo e schema configurados para a pipeline; o exemplo usa o namespace padrão atual, sem depender de `LIVE`.

## Experimente

Leia o arquivo completo e o guia de execução. Crie uma pipeline de estudo apontando para seu catálogo/schema autorizado. Acrescente o arquivo como fonte e execute uma atualização. Inspecione grafo, métricas de expectativa e quarentena. Não execute esse arquivo como um notebook comum esperando o mesmo ciclo de vida.

## Resultado esperado

Fonte de quatro linhas: duas Silver válidas e duas inválidas; Gold totaliza somente o concluído. Registre as métricas reais depois da atualização. A verificação local cobre sintaxe, mas não execução do serviço.

## Erros comuns

Misturar DLT legado e APIs atuais sem contexto; chamar `.write` dentro da definição; presumir que uma expectativa de descarte conserva registros; configurar destino de produção por conveniência.

## Desafio

Defina uma regra que bloqueie a publicação e outra que apenas gere investigação. Justifique o impacto operacional de cada uma.

## Critério de conclusão

Você entrega grafo esperado, contratos e evidência real de atualização, ou uma ficha claramente marcada como pendente.

## Referências

Fonte: engenharia; [Python em pipelines declarativas](https://docs.databricks.com/aws/en/ldp/developer/python-dev).
