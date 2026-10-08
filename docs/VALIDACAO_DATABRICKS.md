# Validação nativa pendente

Os 17 notebooks foram exportados, conferidos sintaticamente e comparados aos módulos locais. Isso não demonstra execução em Databricks. Preencha [o registro](REGISTRO_EXECUCAO_DATABRICKS.md) após executar em seu workspace de estudo.

Comece pelo notebook 00 e prossiga na ordem indicada, respeitando dependências. Os 12 a 16 ampliam dados públicos, validação temporal/calibração, SCD2, watermark e RAG extrativo. Configuração de permissões e recursos pode exigir adaptações documentadas. O notebook 14 usa uma tabela dedicada e marca de propriedade para o MERGE; opções de escrita ficam desativadas inicialmente. O notebook 15 usa um caminho de estudo e checkpoint próprio.

Não substitua spark, dbutils ou display por mocks para afirmar validação nativa. Confirme contagens, valores, replay, histórico, permissões e falhas. Delta, Unity Catalog, Jobs, MLflow e Auto Loader permanecem pendentes, inclusive se Spark local estiver verde.
