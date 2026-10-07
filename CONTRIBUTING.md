# Como contribuir com o Lab Bricks

Crie conteúdo próprio, pequeno o suficiente para ser reproduzido e profundo o suficiente para exigir uma decisão. Referências ajudam a fundamentar; não autorizam copiar livros, imagens, perguntas de prova ou dados privados.

## Acrescentar uma aula

1. Gere um template pela página Adicionar conteúdo ou `python scripts/new_lesson.py --id g06-minha-pratica --title "Minha prática" --track governanca`.
2. Preencha as nove seções pedagógicas. Descreva ambiente, parâmetros, resultado e critério verificável.
3. Declare IDs de pré-requisitos existentes e fontes em `content/sources.json`. Use versão estável e incremente quando mudar procedimento ou contrato.
4. Acrescente perguntas originais em `content/questions.json` e benchmarks em `content/retrieval_benchmark.json` quando fizer sentido.
5. Rode verificação e testes. Submeta um commit/PR com problema, mudança e evidência.

O catálogo descobre aulas automaticamente. Se criar uma trilha, registre título, descrição e horas sugeridas em `content/tracks.json`. IDs não devem ser reutilizados para temas diferentes. O progresso importado rejeita aulas desconhecidas: mantenha IDs estáveis e documente migrações.

## Alterar código ou notebook

Use os `.py` como fonte canônica; execute `python scripts/export_notebooks.py` depois. As funções copiadas nos notebooks devem permanecer iguais aos módulos originais. Acrescente um teste que detecte o erro real quando alterar um contrato, cálculo ou limite; não crie testes só para repetir a implementação.

```bash
python scripts/verify_project.py
python -m pytest
python scripts/audit_dependencies.py
```

Execução Spark opcional usa `requirements-spark.txt` e Java compatível. Execução Databricks precisa de evidência no registro próprio. A CI não faz deploy e não deve receber tokens pessoais.

## Limpeza e licenças

Não versionar ambientes, caches, logs, arquivos ZIP, progresso pessoal, PDFs/EPUBs de referência, `mlruns`, credenciais ou outputs de notebooks. O empacotador seleciona formatos e pastas explicitamente. Novos formatos exigem revisão do contrato de entrega e licença.

Use a paleta declarada no README e uma marca original. Diagramas devem explicar relações; gráficos devem vir de dados reais do fixture e indicar parâmetros. Consulte SECURITY.md antes de relatar um problema.
