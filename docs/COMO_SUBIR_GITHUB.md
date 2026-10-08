# Atualizar o GitHub preservando seu estudo

Use o repositório bruno-dsn/lab-bricks. Guarde antes suas soluções e caderno em um branch ou cópia pessoal. Não copie um ZIP por cima de exercícios resolvidos sem revisar diferenças. O ZIP não contém .git: conserve seu clone e histórico.

```bash
git status
python scripts/verify_project.py
python -m pytest
python scripts/audit_dependencies.py
git diff --stat
git add README.md CHANGELOG.md CONTRIBUTING.md app.py src tests scripts content docs data assets notebooks exercicios solucoes requirements-semantica.txt requirements-rag.txt
git diff --cached --stat
git commit -m "Atualiza escola Lab Bricks"
git push
```

Adicione também arquivos de configuração que tenha alterado após revisão. Não use git add -A sem conferir o que será incluído, nem force push para substituir histórico. Nunca adicione ambientes, artifacts, cadernos pessoais, pesos ou livros.

Na aba Actions, confira o workflow do SHA do seu commit. Só marque CI aprovada depois que esse run terminar verde; um run anterior não valida sua alteração.
