# Da feature à inferência: um ciclo que dá para verificar

Databricks ML in Action, de 2024, acrescentou uma perspectiva de ciclo completo. As práticas abaixo são próprias e usam entregas fictícias. Aulas [m06](../content/aulas/m06-features-temporais.md), [m07](../content/aulas/m07-selecao-validacao.md) e [m08](../content/aulas/m08-contrato-inferencia.md) conectam os conceitos ao app e ao [notebook 11](../notebooks/11_ciclo_ml_e_contrato.py).

## 1. Torne a disponibilidade uma parte do contrato

Registre separadamente instante do evento, instante da disponibilidade, entidade, versão e unidade. A função local `juntar_no_instante` usa somente uma versão disponível até a previsão, preserva pedidos sem histórico e rejeita instantes ambíguos. No cenário padrão, P1/P2/B têm risco 0,2/0,8/ausente.

Em Feature Engineering UC, a tabela e o lookup precisam declarar o tempo corretamente. Uma coluna timestamp incluída apenas como chave não garante lookup temporal. Confira [conceitos](https://docs.databricks.com/aws/en/machine-learning/feature-store/concepts), [lookup temporal](https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series) e a [API da biblioteca](https://api-docs.databricks.com/python/feature-engineering/latest/feature_engineering.client.html) na versão instalada. Um lookback limita a idade admissível; ele não corrige sozinho um timestamp que representa ocorrência, mas não disponibilidade.

## 2. Separe o aprendizado da escolha

O fixture de 600 entregas produz 360 linhas de treino, 120 de validação e 120 de teste. Três candidatos e 17 limiares geram 51 combinações na validação. O custo ilustrativo é R$ 5 × FP + R$ 30 × FN. Empates seguem custo, Brier, nome e limiar.

O treino ajusta cada pipeline; a validação escolhe; o teste mede. A baseline pode vencer. Este exercício não retreina após a seleção. Se você retreinar com mais dados, documente o novo artefato e avalie-o de acordo com o protocolo definido. Não use o teste já observado para decidir alterações.

AutoML pode gerar um ponto de partida e código para examinar. Inspecione features, split, transformações e orçamento de busca. Mais candidatos não justificam consumir repetidamente o teste.

## 3. Valide o input antes de inferir

O contrato local exige cinco colunas numéricas, finitas e nos domínios do caso fictício. Ele rejeita ausência, colunas extras, texto, booleanos e valores inadmissíveis. A assinatura MLflow descreve estrutura; disponibilidade, unidades e domínios também precisam de controles próprios.

O notebook 11 oferece Tracking **opcional**. Deixe `registrar_experimento=nao` para praticar sem registrar artefatos. Se usar `sim`, informe um experimento autorizado e execute em ambiente com MLflow 3. O exemplo registra uma política PythonModel com o pipeline e o limiar escolhido, produzindo probabilidade e alerta. Assim, o artefato não perde a regra de decisão na serialização.

No MLflow 3, `name` substitui o parâmetro depreciado `artifact_path` nos exemplos de logging comuns. Carregue pela URI retornada pelo log, sem presumir um caminho legado de artefato. O notebook confere o round-trip das probabilidades e dos alertas. Fonte: [migração e instalação do MLflow 3](https://docs.databricks.com/aws/en/mlflow/mlflow-3-install). Esse trecho não foi executado numa conta por este trabalho.

## 4. Escolha batch ou endpoint pelo uso

| Questão | Inferência em lote | Endpoint |
|---|---|---|
| Consumidor | Tabela de pedidos de um período | Aplicação que envia solicitações |
| Critério operacional | Prazo do lote, contagem, falhas e custo | Latência, disponibilidade, autorização e custo |
| Evidência | Versão/URI, input e tabela de previsões reconciliados | Versão servida, contrato e chamadas de teste |
| Falha | Quarentena e reprocessamento definido | Erro controlado, supervisão e rollback definido |

Registro UC, alias e endpoint são etapas distintas. Use uma versão resolvida e auditável; defina quem pode promover e como reverter. Fontes: [inferência batch](https://docs.databricks.com/aws/en/machine-learning/model-inference), [Model Serving](https://docs.databricks.com/aws/en/machine-learning/model-serving) e [ciclo UC](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/).

## Atualizações em relação à edição de 2024

| Referência histórica | Orientação atual aplicada |
|---|---|
| Community Edition | Consultar Free Edition e suas limitações atuais |
| Delta Live Tables | Lakeflow Spark Declarative Pipelines; exemplo separado em `pipelines/` |
| Workflows / Asset Bundles | Lakeflow Jobs / Declarative Automation Bundles |
| Lakeview | AI/BI dashboards |
| MLflow 2 e caminhos de run | Notebook novo com MLflow 3, URI devolvida, assinatura e política completa |
| Catálogos de modelos/regiões de 2024 | Consultar a disponibilidade atual antes de escolher recursos |

São adaptações conceituais com fontes atuais. Vector Search, embeddings remotos, image classification, Feature Store UC e serving não são funcionalidades locais já implantadas. Para aprofundar, use o roadmap e registre a execução real em [validação da conta](VALIDACAO_DATABRICKS.md).
