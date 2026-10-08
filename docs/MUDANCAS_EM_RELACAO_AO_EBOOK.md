# Diferenças em relação ao e-book - edição 3.0

O e-book foi o ponto de partida. A escola mantém seus temas fundamentais, mas acrescenta conteúdo próprio e prática verificável: 45 aulas, 14 exercícios, missões SQL, caso público rastreável e comparação de resultados que inclui falhas.

A principal diferença é exigir construir a solução, investigar casos de erro e registrar evidência. ML ganhou gap temporal, calibração, instabilidade e decisão de monitoramento. Engenharia ganhou SCD2, CDC, replay e watermark. IA ganhou benchmark congelado lexical/semântico e geração local medida, com resultado negativo registrado.

Os livros anexados enriqueceram os temas de BI, engenharia, ML e LLMs. Não foram copiados ou redistribuídos. Nenhuma etapa de conta Databricks é apresentada como executada; notebooks e registro permitem realizar essa validação depois.

O texto abaixo registra diferenças das edições anteriores; números históricos não descrevem a entrega atual.

# Do e-book ao Lab Bricks

O e-book inicial apresentava uma visão introdutória de dados e Databricks. O projeto passou a ser um laboratório de estudo com conteúdo original e critérios de conclusão. Os livros novos ampliaram os temas; não foram publicados nem condensados como substitutos das obras.

| Antes | Lab Bricks 2.0 | Por que ajuda a estudar |
|---|---|---|
| Visão introdutória de SQL/engenharia/ML/IA | 35 aulas em seis trilhas com pré-requisitos | Sequência, revisão e objetivo observável |
| Um exemplo simples de vendas | Dois casos: pedido único e pedido com vários itens | Ensina grão, joins, dimensões e reconciliação |
| Discussão de pipelines | Qualidade, quarentena, incrementos, JSON, Auto Loader e pipeline declarativa | Combina mecanismo, erro e operação |
| Apresentação de ML | Baselines, corte temporal, classificação, custo, MLflow e drift | Avalia resultado sem usar o futuro |
| Apresentação de LLMs/agentes | Recuperação lexical executável, desenho RAG, benchmark e supervisão | Evidências e limites explícitos |
| Leitura sem registro | Progresso exportável, 43 perguntas e três projetos com rubricas | Dá um caminho e evidências pessoais |
| Conteúdo fixo | Catálogo Markdown/TOML, gerador e fontes versionadas | Acrescenta aulas sem alterar app.py |
| Identidade inicial | Nome Lab Bricks, marca original e paleta Lava/Navy/Oat | Visual coerente no app, diagramas e gráficos |

## Melhorias técnicas sobre a primeira versão

- O editor SQL passou a admitir quatro tabelas do caso BI e funções de janela, preservando authorizer, orçamento e bloqueio de escrita/arquivos.
- O app ganhou 15 páginas, biblioteca e progresso portátil com importação JSON restrita.
- Os notebooks passaram de cinco para doze, com pares `.py`/`.ipynb` sem saídas; há também uma pipeline declarativa e um bundle de Job.
- O schema de estudo agora usa prefixo `lb_`. Tabelas antigas com `dbnp_` não são removidas. Consulte o guia antes de migrar.
- A verificação de conteúdo valida IDs, fontes, questões e ciclos nos pré-requisitos. O ZIP segue seleção explícita de arquivos e exclui progresso pessoal e referências PDF.
- As novas experiências têm testes de invariantes, limites e comportamentos negativos. A auditoria NotKode foi revisada para a importação de progresso e SQL com múltiplas tabelas.

## Acréscimo do sexto material: Databricks ML in Action

As aulas m06–m08, a página ML e ciclo completo e o notebook 11 ampliam o estudo com features disponíveis na previsão, seleção temporal 60/20/20 e contrato de inferência. Há 51 combinações comparadas apenas na validação e uma política congelada no teste. Tracking opcional usa MLflow 3 com assinatura, limiar incluído no artefato e verificação de round-trip. O guia CICLO_ML diferencia essas práticas locais de Feature Store UC e serving, ainda dependentes de execução na conta.

## Onde termina o escopo

Você consegue aprender e praticar fundamentos de Databricks, engenharia, BI, ML e IA com esta trilha. Domínio profissional exige também execução em ambiente real e casos de escala. O material não promete cobrir cada página dos livros, toda a plataforma, aprovação em prova ou prontidão de produção.

Delta, Unity Catalog, Jobs, Auto Loader, pipelines e MLflow exigem conta, recursos e permissões. Há roteiros e exemplos; uma etapa só vira evidência validada depois de rodar. SCD tipo 2, CDC, integrações externas, serving e busca semântica estão no roadmap como aprofundamentos.
