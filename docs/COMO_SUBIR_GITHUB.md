# Colocar o projeto no seu GitHub

O repositório desta entrega é [bruno-dsn/lab-bricks](https://github.com/bruno-dsn/lab-bricks). Os passos abaixo também servem para criar uma cópia ou publicar uma evolução.

O pacote contém a pasta `lab-bricks`. Extraia e coloque o **conteúdo dessa pasta** na raiz do repositório: o GitHub deve encontrar `README.md` na primeira página. O ZIP é um meio de transporte, não o único arquivo a publicar.

## Criar o repositório

No GitHub, escolha **New repository**, informe `lab-bricks`, descreva o projeto e escolha a visibilidade. Como os arquivos já vêm preparados, crie o repositório vazio, sem gerar outro README, licença ou gitignore.

Descrição sugerida: `Laboratório em português para aprender Databricks com 33 aulas, 12 notebooks, três projetos e app de SQL, BI, engenharia, ML, IA e governança.`

## Enviar pelo terminal

Dentro da pasta extraída, revise os arquivos e execute:

```bash
git init
git add .
git status
git commit -m "Adiciona laboratório Lab Bricks"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/lab-bricks.git
git push -u origin main
```

Substitua `SEU_USUARIO` pelo seu usuário e use o nome de repositório que criou. Esses comandos são para uma pasta nova; se já houver um repositório, preserve o histórico e revise o remote antes de adicionar os arquivos.

Antes do envio, execute `python scripts/verify_project.py`: quando existe `.git`, ele procura os padrões de segredo também nos blobs de todo o histórico local. A busca é limitada; revise os alertas e recursos de detecção de segredos disponíveis na sua conta.

O Git pode pedir configuração de autoria e autenticação. Use os mecanismos do GitHub no seu computador; não coloque um token dentro da URL nem no código.

Você também pode usar **Add file → Upload files** na página do repositório. Preserve as pastas e inclua os arquivos de configuração que começam com ponto. O terminal ou o GitHub Desktop ajudam a enviar a estrutura completa.

## Conferir a primeira publicação

- Abra o README e veja se capa, arquitetura e gráfico carregam.
- Abra um `.ipynb` e confira a leitura das células.
- Veja a aba Actions: o workflow foi fornecido, mas a execução no GitHub só acontece após o envio.
- Revise alertas de segurança e as pendências registradas na auditoria.
- Acrescente suas próprias melhorias e indique quais execuções validou na conta Databricks.

## Gerar outro ZIP limpo

Execute `python scripts/package_project.py ../lab-bricks-v2.0.zip`. O script confere o projeto e inclui seus fontes, dados, imagens e configuração. Ambientes virtuais, `.git`, caches, logs e outros ZIPs ficam fora. O arquivo gerado usa datas e permissões estáveis; o terminal informa a quantidade de arquivos e seu SHA-256.

Instruções oficiais: [criar repositório](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) e [adicionar arquivos](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).
