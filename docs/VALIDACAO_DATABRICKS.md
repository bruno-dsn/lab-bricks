# Registro de validação e limites

**Versão 2.0 · 7 de outubro de 2026.** Evidências locais e de conta têm escopos diferentes. Os materiais oficiais foram consultados, mas nenhuma conta Databricks foi usada para executar serviços neste trabalho.

## O que é validado localmente

- Funções Pandas/SQLite/scikit-learn, geração sintética, SQL de leitura e limites.
- Catálogo, referências, ciclo de pré-requisitos, questões e progresso JSON.
- Páginas do app com Streamlit AppTest e comportamentos de consulta.
- Sintaxe de Python/notebooks/pipeline; correspondência `.py`/`.ipynb` e ausência de outputs.
- Cenários selecionados de transformação em Spark local, descritos no relatório de testes.

Spark local não comprova Delta, Unity Catalog, serverless, Auto Loader, Jobs, pipelines ou MLflow na conta. A configuração de bundle não foi validada autenticada nem implantada por este trabalho.

## Preencha após executar na sua conta

| Item | Evidência a guardar | Estado inicial |
|---|---|---|
| Ambiente | Cloud, compute, versão, identidade e catálogo | Pendente |
| Namespace/permissões | Schema, privilégios e teste com outra identidade | Pendente |
| Notebook 02 | 727/720/6/1, reconciliação e histórico Delta | Pendente |
| Notebook 03 | 721 chaves, dois MERGEs e comparação de conteúdo | Pendente |
| Notebook 04 | Datas, baseline/MAE e run Tracking se autorizado | Pendente |
| Notebook 05 | Quatro tabelas, 164 concluídos e métricas | Pendente |
| Notebook 06 | Mensagens/itens/quarentena e soma | Pendente na conta |
| Notebook 07 | Gate sobre tabelas do 02 | Pendente |
| Notebook 08 | Volume/checkpoint, dez linhas, reexecução | Pendente |
| Notebooks 09/10 | Ambiente, métricas e evidências recuperadas | Pendente na conta |
| Notebook 11 | Corte 360/120/120, contrato, run/URI e round-trip MLflow 3 opcional | Pendente na conta |
| Job/bundle | CLI validate, deploy, run ID, grafo e falhas | Pendente |
| Pipeline declarativa | Grafo, 4/2/2 linhas, Gold 1.200 centavos | Pendente |
| AI/BI | Queries, filtros, totais e compartilhamento | Pendente |

Registre data, parâmetros, commit e mensagens relevantes sem tokens nem dados privados. Não publique outputs completos por conveniência. Uma falha encontrada deve constar da ficha com causa, correção e reexecução. Só marque como concluído o que foi efetivamente exercitado.

Siga o [guia nativo](GUIA_DATABRICKS.md). Se você não tiver a conta, conclua os projetos locais e preserve as pendências.
