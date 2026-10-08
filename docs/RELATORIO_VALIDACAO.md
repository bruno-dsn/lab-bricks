# Relatório de validação - Lab Bricks 3.0

## Escopo observado em 8 de outubro de 2026

A versão 2.1 recebida passou em 120 testes antes da expansão. A escola foi validada em Python 3.12.14 com os 52 pacotes do requirements.lock. A repetição após recuperação e correções finais terminou com **169 passed in 30.75s**. O conjunto final tem **169 testes de manutenção**; inclui abertura das **23 páginas** por Streamlit AppTest. Os **14 exercícios** têm **64 verificações de aluno**: todas as referências passam, e esqueletos temporários vazios não aprovam. A verificação não sobrescreve arquivos do estudante.

Comandos: build_school_notebooks.py, export_notebooks.py, verify_project.py e python -m pytest. O verificador confere sintaxe, links, 17 pares de notebooks sem outputs, cópias dos módulos, escola, perguntas congeladas, cache de vetores e dados sintéticos.

## Experimentos executados

| Experiência | Resultado | Limite |
|---|---|---|
| Online Retail | 3.000 = 2.946 + 10 + 44; Gold 5.682.033 pence | Um dia, sem previsão real |
| Estabilidade | 30 sementes; vitórias 17/13; ganho 385, IC [336,50; 437,00] | Gerador sintético |
| Busca | TF-IDF R@1 46,7%; encoder 40,0% | Corpus congelado 35 aulas; chunking confunde comparação |
| Geração local | 7 rejeições de contrato, 7 abstenções, 0 úteis | Revisão factual pendente |
| Spark 4.0.1 / Java 17 | Sete cenários aprovados | Sem Delta ou conta Databricks |
| OSV | 69 pacotes fixados, sem advisories retornados | Consulta datada, não garantia futura |

Spark exerceu três casos de pipeline, JSON, BI com janela, Gold público e streaming com replay de checkpoint. Uma tentativa inicial de transferência da Gold via PythonRDD falhou no worker; transferência Arrow corrigiu o caminho local e os sete cenários passaram. Isso não valida a execução dos notebooks inteiros nem serviços cloud.

A consulta OSV está registrada em DEPENDENCIAS_OSV.json e cobre locks de núcleo, Spark e semântica. O engine nativo e os pesos do LLM não são pacotes PyPI e não foram cobertos pelo OSV.

## Segurança e empacotamento

SQL usa authorizer real do SQLite e orçamento. Caderno/feedback têm JSON com esquema e limite de 100 KB. Cache de vetores não permite pickle. Código de aluno só é executado pelo comando local explícito. Artefatos pessoais, ambientes, pesos, livros, segredos e temporários ficam fora do ZIP.

Busca de padrões de segredo é limitada. Controles de conta, hospedagem e identidade continuam pendentes na auditoria. GitHub Actions deve ser conferido no commit publicado; resultados locais não implicam execução da CI.

## Databricks

Nenhum dos 17 notebooks foi executado em uma conta Databricks nesta revisão. [Registro](REGISTRO_EXECUCAO_DATABRICKS.md) permanece pendente. Preencha versões, resultado, run ID/link e falhas somente após execução real.
