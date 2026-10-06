# Contribuir com a trilha

Use Python 3.12, instale `requirements.lock` e execute os comandos de validação do README. Abra uma proposta descrevendo o problema observado e um exemplo pequeno.

Uma contribuição de ensino deve explicar a regra, mostrar a entrada, permitir uma alteração e apontar o resultado esperado. Uma contribuição de código deve incluir um teste quando mudar uma regra de dados, acesso ou cálculo.

Edite os notebooks `.py` e gere os `.ipynb` com `python scripts/export_notebooks.py`. Mantenha as funções compartilhadas dos notebooks coerentes com `src/lab/`. O 00 inclui o gerador e o 04 inclui as funções locais de ML; a verificação detecta divergências nessas cópias.

Ao atualizar dependências, revise a compatibilidade no Python 3.12, atualize os requisitos e o lockfile e rode novamente testes e auditoria. Mantenha ações de CI fixadas por commit e permissões mínimas.

Não envie dados reais, tokens ou saídas de notebook com informação privada. Descreva falhas de segurança seguindo [SECURITY.md](SECURITY.md).
