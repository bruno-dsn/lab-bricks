# MLflow, registro e operação

O notebook 04 executa a avaliação sem exigir um endpoint. Tracking é opcional e usa um experimento autorizado. Modelo treinado, run registrado, versão no registry e serving são estados distintos.

## Ficha de experimento

Registre commit, versão da fonte, semente, features e instante de disponibilidade, cortes, baseline, métricas e limitações. No caso de previsão, declare avaliação de um dia à frente. Na classificação, não use `duracao_real_min` como feature e não selecione um limiar no mesmo teste que será reportado como avaliação final.

## Extensão: aliases em Unity Catalog

A documentação atual usa registry UC e aliases. O exemplo abaixo é um **roteiro de extensão**, não uma operação executada pelo projeto. Exige modelo já registrado, versão existente e privilégios apropriados. Valide assinatura e resultados antes de promover.

```python
import mlflow
from mlflow import MlflowClient

mlflow.set_registry_uri("databricks-uc")
client = MlflowClient()
# Substitua por objetos e versão de estudo que você efetivamente criou.
nome_modelo = "catalogo_estudo.schema_estudo.modelo_entregas"
versao_aprovada = "1"
client.set_registered_model_alias(nome_modelo, "Champion", versao_aprovada)
# Carregar um alias não implanta automaticamente serving:
modelo = mlflow.pyfunc.load_model(f"models:/{nome_modelo}@Champion")
```

Champion é uma convenção, não um selo automático. A assinatura de entrada deve incluir nomes/tipos esperados e rejeitar input incompatível. Não copie estágios legados do Workspace Model Registry para UC sem revisar a migração.

## Promoção e rollback

| Etapa | Evidência necessária |
|---|---|
| Avaliação | Mesmo protocolo, baseline e critério congelado |
| Registro | Run, artefato, assinatura e proveniência |
| Aprovação | Pessoa/automação autorizada, riscos e justificativa |
| Serving | Ambiente, acesso, orçamento, latência e falhas testados |
| Monitoramento | Dados, qualidade com rótulos, segmentos e disponibilidade |
| Rollback | Versão anterior, gatilho, responsável e verificação de consumidores |

PSI informa mudança exploratória da distribuição. Sem novos rótulos, não demonstra queda preditiva. Um Job de retreinamento deve validar contratos e dados antes de promover. Não há registro, troca de alias, endpoint ou retreinamento automático ao abrir o app.

Fonte: [Manage model lifecycle in Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/) e [MLflow](https://mlflow.org/docs/latest/). Referência conceitual: livro de ML fornecido, edição de 2023, adaptado com exemplos originais.

Para o fluxo novo com assinatura, seleção e MLflow 3, consulte [CICLO_ML](CICLO_ML.md) e o notebook 11.
