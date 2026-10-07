+++
id = "g03-entrega"
title = "Versione conteúdo e entregue configurações revisáveis"
track = "governanca"
level = "Avançado"
version = "2.0"
prerequisites = ["g02-jobs", "f05-reprodutibilidade"]
sources = ["engenharia-livro", "ml-livro", "oficial"]
objectives = ["Separar validação local, bundle e deploy", "Adicionar uma aula preservando o contrato"]
lab = "Adicionar conteúdo; scripts/new_lesson.py e databricks.yml"
+++

# Versione conteúdo e entregue configurações revisáveis

## Problema

Uma atualização mistura notebook, credencial, PDF de referência e cache no mesmo commit. A revisão fica difícil e a publicação pode vazar dados ou material que não deveria ser redistribuído.

## Conceito

CI verifica um commit; CD entrega recursos em um ambiente. O workflow deste projeto executa validação, testes e auditoria de dependências, com permissões de leitura. Não tem credenciais Databricks nem deploy automático. Declarative Automation Bundles, nome atual da família antes chamada Asset Bundles, descreve recursos em YAML para validar e entregar de modo revisável.

O catálogo usa Markdown com cabeçalho TOML: ID, trilha, versão, fontes, objetivos e pré-requisitos. O app descobre aulas no diretório autorizado. Adicionar conteúdo não requer abrir uma área administrativa pública: um mantenedor altera arquivos e submete a revisão do Git. Os livros anexados permanecem referências privadas, fora do repo e do ZIP.

## Exemplo explicado

```bash
python scripts/new_lesson.py --id g07-nova-pratica   --title "Minha nova prática" --track governanca
python scripts/verify_project.py
```

O gerador recusa IDs inválidos e sobrescrita. Depois preencha as seções e fontes; o verificador detecta referências desconhecidas e ciclos nos pré-requisitos. O template é um começo, não uma aula pronta para declarar domínio.

## Experimente

Use a página Adicionar conteúdo para baixar um template. Preencha exemplo, resultado e critério. Inclua uma fonte no catálogo quando necessário e ajuste a versão. Execute verificação e testes antes do commit. Para recursos nativos, rode `databricks bundle validate` na sua conta antes de deploy.

## Resultado esperado

A nova aula aparece na biblioteca e na trilha sem editar app.py. Uma dependência circular ou ID duplicado falha com mensagem. A validação de bundle e deploy permanecem etapas separadas.

## Erros comuns

Salvar PDFs protegidos no Git; colocar caches ou progresso pessoal no repo; acreditar que AST parse valida uma API remota; configurar token em YAML ou GitHub Actions por conveniência.

## Desafio

Planeje um release que altera contrato de dados: versão, migração, rollback, documentação e evidências. Explique quais mudanças exigem teste novo.

## Critério de conclusão

Seu commit contém somente fontes necessários e a aula possui objetivos verificáveis, referência e procedimento reproduzível.

## Referências

Fontes: engenharia e ML; [Declarative Automation Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/).
