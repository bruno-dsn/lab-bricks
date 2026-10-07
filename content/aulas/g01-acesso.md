+++
id = "g01-acesso"
title = "Trate nomes, permissões e segredos como coisas distintas"
track = "governanca"
level = "Intermediário"
version = "2.0"
prerequisites = ["f01-mapa", "e01-medallion"]
sources = ["engenharia-livro", "bi-livro", "oficial"]
objectives = ["Planejar privilégios mínimos no Unity Catalog", "Evitar credenciais no repositório e nas saídas"]
lab = "Notebook 00 e checklist de segurança"
+++

# Trate nomes, permissões e segredos como coisas distintas

## Problema

Dois alunos usam o mesmo catálogo. O schema com um nome diferente evita sobrescrever por engano, mas não determina quem pode ler. Segurança depende de privilégios, identidade e execução.

## Conceito

Unity Catalog organiza catálogo, schema e objetos. Acesso combina privilégios de uso e operações específicas, conforme o objeto. Um processo de leitura não deve receber poderes de escrita só por conveniência. Para automação, use uma identidade apropriada e autenticação recomendada pelo ambiente; para estudo interativo, prefira fluxos OAuth disponíveis.

Nunca salve tokens no código, CSV, screenshots, `.ipynb`, progresso ou logs. A busca limitada de padrões de segredo é um controle auxiliar: não garante encontrar todo segredo. Se houver vazamento, revogue a credencial e trate o histórico; apenas apagar a linha atual não elimina versões antigas.

## Exemplo explicado

O schema `lb_<hash>` isola nomes por usuário. Esse hash não é senha nem autorização. O app local não gerencia contas nem credenciais e o SQL usa cópias sintéticas efêmeras; publicar o app com dados privados demandaria um desenho de autenticação e acesso que não faz parte dessa simulação.

## Experimente

Liste leitores, autores e identidade do Job. Consulte privilégios reais do seu schema antes de executar. Confira SECURITY.md e a auditoria NotKode. Rode a verificação de arquivos/histórico. Teste com outra identidade autorizada somente quando sua conta permitir e registre resultados reais.

## Resultado esperado

Uma matriz de acesso informa quem lê, escreve e administra. O relatório mantém como pendentes controles que dependem da conta ou hospedagem. Nenhum token é solicitado pelo app.

## Erros comuns

Tratar namespace como ACL; copiar exemplos com ALL PRIVILEGES; compartilhar credencial pessoal; testar autorização somente com o proprietário; adicionar dados reais ao gerador sintético.

## Desafio

Descreva como revogar o acesso de alguém ao catálogo e aos artefatos derivados, incluindo modelos e trechos de busca.

## Critério de conclusão

Você distingue identidade, nome e privilégio e pode explicar quais verificações exigem uma conta real.

## Referências

Fontes: engenharia e BI; [privilégios Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges/).
