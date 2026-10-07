# Referências, proveniência e atualização

O conteúdo do Lab Bricks é original. Os materiais fornecidos foram examinados por temas e seções relevantes; não são reproduções integrais nem resumos substitutivos dos livros. Nenhum PDF, imagem editorial, código copiado de livro ou questão de exame entrou no Git/ZIP.

| Referência fornecida | Ano / autoria | Contribuição ao laboratório | Adaptação |
|---|---|---|---|
| E-book introdutório original | Autoria/ano não informados na conversa | Ponto de partida: Excel, SQL, engenharia, ML e agentes | Transformado em sequência de prática e evidência |
| Business Intelligence with Databricks SQL | 2022 · Vihag Gupta · Packt | SQL, modelagem, dashboards, segurança e investigação de desempenho | AI/BI e documentação atual; sem reutilizar interfaces antigas |
| Databricks Certified Data Engineer Associate Study Guide | 2025 · Derar Alhussein · O’Reilly | Spark, Delta, incrementos, produção e governança | Unity Catalog e recursos atuais; prova V3 do livro não tratada como currículo vigente |
| Practical Machine Learning on Databricks | 2023 · Debu Sinha · Packt | Baselines, features, MLflow, registro, serving, drift e entrega | Corte temporal, casos próprios e aliases UC; sem implantar serving automaticamente |
| Databricks ML in Action | 2024 · Stephanie Rivera, Anastasia Prokaieva, Amanda Baker e Hayley Horn · Packt | Features temporais, comparação de experimentos e passagem do modelo à inferência | Três aulas, ciclo temporal, contrato e notebook próprios; MLflow 3 e referências atuais |
| Guia compacto de LLMs | 2023 · Databricks | Tokens, transformers, personalização e usos empresariais | Busca, RAG e avaliação próprios; sem catálogo de modelos desatualizado |
| Relatório empresarial MITTR/Databricks | 2025 · MIT Technology Review Insights, patrocinado pela Databricks | Qualidade de dados, capacitação, valor e supervisão | Cenários ilustrativos próprios; não extrapolamos estatísticas da pesquisa |

## Mapa de influência

| Trilha | Referências principais | O que é original e verificável |
|---|---|---|
| Fundamentos | E-book, engenharia, BI | Contratos, tipos, fixtures e reconciliação |
| SQL/BI | BI e engenharia | Caso de quatro tabelas, métricas e queries |
| Engenharia | Engenharia e BI | Quarentena, MERGE, JSON e gates |
| ML | Livros de ML e relatório empresarial | Forecast, entregas sintéticas, limiar, custos, PSI, seleção e contrato de inferência |
| IA | Guia LLM, relatório e papers | Busca TF-IDF, benchmark, prompts não executados e rubricas |
| Governança | Engenharia, BI, ML e relatório | Matriz de acesso, bundle, CI e processo de conteúdo |

As aulas declaram IDs de fontes em seus metadados. O catálogo [sources.json](../content/sources.json) mantém autoria, ano, uso e links públicos quando disponíveis. O aluno pode acrescentar referências preservando essa atribuição.

## Fontes técnicas atuais · conferidas em 7 de outubro de 2026

- [Documentação Databricks](https://docs.databricks.com/aws/en/).
- [Free Edition e limites](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations).
- [Unity Catalog / privilégios](https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges/).
- [Delta MERGE](https://docs.databricks.com/aws/en/delta/merge) e [histórico](https://docs.databricks.com/aws/en/delta/history).
- [Auto Loader](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/).
- [Lakeflow Spark Declarative Pipelines em Python](https://docs.databricks.com/aws/en/ldp/developer/python-dev).
- [Lakeflow Jobs](https://docs.databricks.com/aws/en/jobs/jobs-quickstart).
- [AI/BI dashboards](https://docs.databricks.com/aws/en/dashboards/).
- [Declarative Automation Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/) e [exemplos de configuração](https://docs.databricks.com/aws/en/dev-tools/bundles/examples).
- [MLflow / lifecycle UC](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/).
- [MLflow 3](https://docs.databricks.com/aws/en/mlflow/mlflow-3-install), [features point-in-time](https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series), [inferência batch](https://docs.databricks.com/aws/en/machine-learning/model-inference) e [Model Serving](https://docs.databricks.com/aws/en/machine-learning/model-serving).
- [Guia oficial Data Engineer Associate](https://www.databricks.com/learn/certification/data-engineer-associate).
- [Spark](https://spark.apache.org/docs/latest/sql-programming-guide.html), [scikit-learn](https://scikit-learn.org/stable/) e [MLflow](https://mlflow.org/docs/latest/).
- [Attention Is All You Need, 2017](https://arxiv.org/abs/1706.03762) e [RAG, 2020](https://arxiv.org/abs/2005.11401).
- [Paleta oficial Databricks](https://brand.databricks.com/): Lava `#FF3621`, Navy `#0B2026`, Oat Medium `#EEEDE9`, Oat Light `#F9F7F4`, branco. A marca Lab Bricks é própria; não usamos o logotipo Databricks.
- [Checklist NotKode solicitado](https://notkode.com.br/pt/recursos/hub-de-conteudos/checklist-de-seguranca).

Conceitos históricos foram aproveitados; comandos, nomes e APIs atuais foram conferidos em fontes primárias. A execução desses recursos em sua conta precisa de validação; consulte o registro específico.
