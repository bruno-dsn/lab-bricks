# Percurso da escola 3.0

As seis trilhas temáticas abaixo continuam para revisão. A sequência de construção agora tem 10 etapas em Minha escola e no [guia](GUIA_ESCOLA.md), cobrindo as 45 aulas e os 14 exercícios. As aulas novas acrescentam estudo com evidência, missões SQL, dados públicos, gap temporal, calibração, monitoramento, semântica, RAG, SCD2 e watermark.

# Sua trilha Lab Bricks

Estude fundamentos primeiro; avance pelas outras trilhas respeitando os pré-requisitos declarados em cada aula. No app, marque conclusões, exporte progresso e use os critérios para revisar aprendizado.

**Plano sugerido:** 57–82 horas de aulas/práticas, mais 6–10 horas de exercícios e 14–20 horas para projetos. É planejamento, não garantia de domínio. Se você já conhece Python/SQL, use os critérios para identificar o que pode revisar mais rápido.

## 01 · Fundamentos e ambiente

Ler dados, definir grão e escolher onde executar. **Ritmo sugerido:** 6–8 horas.

- [f01-mapa · Escolha seu ambiente e entenda o mapa](../content/aulas/f01-mapa.md) — Comece por aqui e notebook 00.
- [f02-grao · Defina o grão antes de contar](../content/aulas/f02-grao.md) — Pipeline e qualidade e BI e modelagem.
- [f03-python · Leia e transforme um DataFrame](../content/aulas/f03-python.md) — Pipeline e qualidade; notebooks 00 e 02.
- [f04-contrato · Escreva um contrato que rejeita ambiguidade](../content/aulas/f04-contrato.md) — Pipeline e qualidade.
- [f05-reprodutibilidade · Transforme uma experiência em evidência](../content/aulas/f05-reprodutibilidade.md) — README, testes e docs de validação.

## 02 · SQL, modelagem e BI

Consultas confiáveis, janelas, dimensões e dashboards. **Ritmo sugerido:** 8–12 horas.

- [s01-agregacoes · Filtre a população antes de agregar](../content/aulas/s01-agregacoes.md) — Laboratório SQL; notebook 01.
- [s02-joins · Construa joins sem multiplicar sua receita](../content/aulas/s02-joins.md) — BI e modelagem; notebook 05.
- [s03-janelas · Use CTEs e janelas mantendo o detalhe](../content/aulas/s03-janelas.md) — BI e modelagem; notebook 05.
- [s04-dashboard · Modele um dashboard com contrato de métricas](../content/aulas/s04-dashboard.md) — BI e modelagem; prática AI/BI guiada.
- [s05-desempenho · Investigue desempenho com um experimento justo](../content/aulas/s05-desempenho.md) — Notebook 05 e análise EXPLAIN guiada.

## 03 · Engenharia e lakehouse

Qualidade, Delta, incrementos e pipelines declarativos. **Ritmo sugerido:** 10–14 horas.

- [e01-medallion · Separe preservação, qualidade e consumo](../content/aulas/e01-medallion.md) — Pipeline e qualidade; notebook 02.
- [e02-delta · Entenda Delta, histórico e isolamento de escrita](../content/aulas/e02-delta.md) — Notebook 02 e 03.
- [e03-incremental · Faça reprocessamento sem duplicar eventos](../content/aulas/e03-incremental.md) — Ingestão incremental; notebook 03.
- [e04-json-streaming · Leia JSON com schema e avance para Auto Loader](../content/aulas/e04-json-streaming.md) — Notebook 06; notebook 08 opcional.
- [e05-declarativo · Declare uma pipeline e suas expectativas](../content/aulas/e05-declarativo.md) — pipelines/qualidade_declarativa.py; prática guiada.

## 04 · Machine learning e MLOps

Baselines, validação temporal, decisões e ciclo de modelos. **Ritmo sugerido:** 16–22 horas.

- [m01-baseline · Comece pelo problema e por uma baseline](../content/aulas/m01-baseline.md) — Previsão de vendas; notebook 04.
- [m02-temporal · Evite vazamento temporal nas features](../content/aulas/m02-temporal.md) — Previsão de vendas e ML e classificação.
- [m03-classificacao · Escolha o limiar pelo custo da decisão](../content/aulas/m03-classificacao.md) — ML e classificação; notebook 09.
- [m04-mlops · Registre, versione e promova com evidências](../content/aulas/m04-mlops.md) — Notebook 04; roteiro de registro no guia.
- [m05-drift · Monitore mudança sem confundi-la com falha](../content/aulas/m05-drift.md) — ML e classificação.

- [m06-features-temporais · Recupere a feature que já existia na previsão](../content/aulas/m06-features-temporais.md) — ML e ciclo completo; notebook 11.
- [m07-selecao-validacao · Escolha modelo e limiar sem consumir o teste](../content/aulas/m07-selecao-validacao.md) — ML e ciclo completo; notebook 11.
- [m08-contrato-inferencia · Leve o modelo à inferência com contrato](../content/aulas/m08-contrato-inferencia.md) — ML e ciclo completo; notebook 11.
- [m09-instabilidade-selecao · Meça o quanto a sua escolha de modelo balança](../content/aulas/m09-instabilidade-selecao.md) — Estabilidade da escolha; exercício 06.

## 05 · IA, LLMs e recuperação

Contexto, evidências, avaliação e revisão humana. **Ritmo sugerido:** 8–12 horas.

- [i01-llms · Entenda o que um LLM faz e onde ele falha](../content/aulas/i01-llms.md) — IA e recuperação; leitura guiada.
- [i02-busca · Recupere trechos com TF-IDF e meça limitações](../content/aulas/i02-busca.md) — IA e recuperação; notebook 10.
- [i03-rag · Planeje um RAG com citações e abstenção](../content/aulas/i03-rag.md) — IA e recuperação; roteiro sem chamadas externas.
- [i04-avaliacao · Avalie recuperação, resposta e segurança separadamente](../content/aulas/i04-avaliacao.md) — IA e recuperação; benchmark próprio.
- [i05-valor · Escolha automações pelo valor e pela supervisão](../content/aulas/i05-valor.md) — Projeto 03 e roteiro de decisão.
- [i06-benchmark-parafraseado · Meça a busca com perguntas de gente de verdade](../content/aulas/i06-benchmark-parafraseado.md) — IA e recuperação; exercício 07.

## 06 · Governança e operação

Permissões, Jobs, entrega, observabilidade e valor. **Ritmo sugerido:** 8–12 horas.

- [g01-acesso · Trate nomes, permissões e segredos como coisas distintas](../content/aulas/g01-acesso.md) — Notebook 00 e checklist de segurança.
- [g02-jobs · Orquestre tarefas com dependências e contratos](../content/aulas/g02-jobs.md) — resources/lab_bricks.job.yml; notebook 07.
- [g03-entrega · Versione conteúdo e entregue configurações revisáveis](../content/aulas/g03-entrega.md) — Adicionar conteúdo; scripts/new_lesson.py e databricks.yml.
- [g04-observabilidade · Observe qualidade, atualização e custo juntos](../content/aulas/g04-observabilidade.md) — Notebook 07; guia de operação.
- [g05-evolucao · Mantenha uma trilha viva e um portfólio verificável](../content/aulas/g05-evolucao.md) — Trilha e progresso; projetos 01 a 03.

## Portfólio

- [Projeto 01: lakehouse](../content/projetos/01-lakehouse-confiavel.md).
- [Projeto 02: BI](../content/projetos/02-bi-decisao.md).
- [Projeto 03: modelos e evidências](../content/projetos/03-ml-ia-evidencias.md).

As rubricas distinguem leitura, prática e evidência. Sem conta Databricks, conclua experiências locais e registre etapas nativas como pendentes.
