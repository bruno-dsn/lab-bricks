# O que mudou em relação ao ebook

O material fornecido, **E-book Databricks 2026 — do zero ao primeiro projeto**, apresenta a plataforma a partir de situações conhecidas de planilhas e convida o leitor a uma imersão. Esta trilha transforma essa introdução em um projeto de estudo que pode ser lido, executado e modificado. A referência está em [Fontes](FONTES.md).

## Da explicação ao código

| Ponto de partida do ebook | O que este projeto acrescenta |
|---|---|
| Comparação com o trabalho em planilhas | Um caso de vendas com contrato de dados, regras explícitas e resultado reconciliado |
| Visão inicial de processamento distribuído | Distinção entre a plataforma Databricks, o motor Spark, as tabelas Delta e a governança Unity Catalog |
| Introdução ao armazenamento e à transformação | Cinco notebooks: configuração, SQL, lakehouse, atualização incremental e avaliação de modelo |
| Panorama de análise, engenharia e ciência de dados | Um laboratório interativo em que você muda a fonte, inspeciona rejeições, escreve SQL e compara previsões |
| Apresentação de recursos da plataforma | Exemplos de deduplicação, quarentena, MERGE idempotente, histórico Delta e experimento opcional com MLflow |
| Convite para continuar aprendendo | Trilha em etapas, desafios, gabaritos, orientações de execução e roadmap |

## Explicações mais precisas

A comparação com planilhas ajuda a começar. Para decidir como usar a plataforma, o projeto explica também o que cada componente faz. Spark distribui trabalho; Delta organiza tabelas com transações e versões; Unity Catalog controla acesso; Databricks reúne esses recursos em uma plataforma. Tamanho dos dados, disponibilidade, limites de compute e custo continuam exigindo planejamento.

A conta de estudo indicada é a Free Edition, com compute serverless e limites próprios. O laboratório local usa Pandas e SQLite para ensinar as regras com uma amostra pequena; seus resultados não medem desempenho de um cluster distribuído.

No modelo, a avaliação respeita a ordem do tempo. As variáveis usam o passado, o teste fica depois do treino e uma previsão simples serve de comparação. O experimento prevê um dia à frente com o passado observado; não promete uma previsão de duas semanas sem observar novos dados.

## Material criado para este repositório

- Fonte sintética: 720 pedidos, uma versão adicional e seis registros inválidos na amostra padrão.
- Código do app e dos notebooks, com regras de negócio e controles do editor SQL.
- Capa, desenho da arquitetura e gráfico gerado pelo experimento.
- Exercícios, soluções, guias, testes automáticos e auditoria dos 21 temas da NotKode.
- Configuração do GitHub, dependências fixadas e script para montar um ZIP limpo.

Os textos, imagens, PDF e peças promocionais do ebook não foram incluídos no pacote. O crédito permanece como inspiração; código e conteúdo original desta trilha estão sob a licença do repositório.

## O que ainda depende da sua conta

A entrega inclui os notebooks e seus testes de reconciliação. Executar Delta, Unity Catalog, o dashboard e MLflow na sua conta continua sendo uma validação do ambiente real. Registre esses resultados no [roteiro Databricks](VALIDACAO_DATABRICKS.md).

Um agente com LLM, pagamentos, cadastro de usuários e integrações de contas estão no [roadmap](ROADMAP.md). A versão atual entrega o projeto educacional de vendas e seu laboratório interativo.
