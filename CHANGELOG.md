# Histórico

## 3.0 - 2026-10-08
- Escola com 10 etapas, reflexões, caderno e feedback; 45 aulas e 63 questões.
- 14 exercícios/64 testes de aluno e três missões SQL.
- Amostra pública UCI Online Retail com licença, hashes e reconciliação.
- Validação temporal com gap, calibração, monitoramento, SCD2 e watermark.
- Encoder local medido no benchmark congelado; geração local com sete falhas de contrato registradas.
- 23 páginas, 17 notebooks coerentes, 169 testes locais, sete cenários Spark e consulta OSV de 69 pacotes.
- Guia, gráficos e entrega limpos; execução Databricks ainda pendente.

# Changelog

## 2.1.0 · 7 de outubro de 2026

Foco: o laboratório ensinar de verdade, corrigindo falhas encontradas em uma revisão técnica da v2.0.

### Adicionado
- **7 exercícios com correção automática** em `exercicios/`, com soluções de referência em `solucoes/`. A CI exige que a solução passe e que o esqueleto não passe em nenhum teste.
- **Aula m09** (estabilidade da escolha) e **aula i06** (benchmark de busca com paráfrases): 35 aulas no total, mais 4 perguntas (43).
- **Módulo `lab.estabilidade`** (repetição do ciclo em várias amostras, bootstrap, limiar teórico) e página **Estabilidade da escolha**.
- **Benchmark parafraseado** (30 casos) e **perguntas fora do escopo** (6); funções `mrr_at_k` e `taxa_de_abstencao`.
- Página **Exercícios** no app; `docs/PROMPT_MELHORIAS.md`; `docs/REGISTRO_EXECUCAO_DATABRICKS.md`.

### Corrigido
- **Dia da semana tratado como número ordenado** nos modelos de previsão e classificação; agora é categoria (one-hot) dentro do `Pipeline`. O scaler continua aprendendo só no treino.
- **Baseline fraca na previsão de vendas:** além de "ontem", o laboratório compara com "mesmo dia da semana passada" e com "média do treino". Nos dados sintéticos padrão, a média do treino é difícil de bater.
- **Benchmark de recuperação inflado:** os 6 casos copiados continuam, mas agora aparecem ao lado das paráfrases e mostram a diferença.
- **Desempenho do app:** o pipeline Bronze → Gold é guardado em cache entre interações.

### Alterado
- App com 15 páginas; trilhas de ML (16–22 h) e IA (9–14 h) com horas revisadas.
- Notebooks 04, 09, 10 e 11 ressincronizados com `src/lab` (o verificador exige a cópia idêntica).

### Ainda não feito
- Execução dos notebooks em uma conta Databricks. Ver `docs/REGISTRO_EXECUCAO_DATABRICKS.md`.
- Terceiro caso com dados públicos reais. Ver `docs/PROMPT_MELHORIAS.md`.

## 2.0.0 · 7 de outubro de 2026

Primeira versão publicada: 33 aulas, 12 notebooks, três projetos, app com 13 páginas.
