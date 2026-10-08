# Continuidade do Lab Bricks 3.0

Leia README, GUIA_ESCOLA, RELATORIO_VALIDACAO, ROADMAP e REGISTRO_EXECUCAO_DATABRICKS antes de propor mudanças.

Objetivo: ensinar construção, investigação de erros e evidência. Escolha uma tarefa por vez. Preserve soluções do aluno e caderno pessoal. Conteúdo em português, próprio e com fontes; não copie livros nem provas.

Já existem 45 aulas, 10 etapas, 14 exercícios, 64 testes de aluno, 63 questões, 23 páginas e 17 notebooks. Dados públicos, validação temporal/calibração, busca semântica, geração exploratória, SCD2 e watermark estão implementados. A execução cloud permanece pendente. O encoder perdeu para TF-IDF neste recorte; todos os sete outputs do pequeno gerador falharam no contrato.

Antes de mudar um benchmark, crie outro protocolo; mantenha o existente congelado. Não prometa generalização de dados sintéticos ou da amostra pública de um dia. Não escreva execução Databricks sem run ID/link.

Se mudar um módulo compartilhado, atualize a fonte do notebook, execute build_school_notebooks.py e export_notebooks.py e confira verify_project.py. Rode testes pertinentes e a suíte completa antes da entrega, auditoria OSV e empacotamento limpo. Atualize docs, contagens e registro de limitações.

Sugestão de tarefa: executar notebooks nativos e corrigir uma falha observada, ou desenvolver um caso ML público com período suficiente e teste final protegido. Defina primeiro o resultado que o estudante deve conseguir produzir.
