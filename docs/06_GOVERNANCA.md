# Quem pode fazer o quê

Separar os dados em tabelas organiza o trabalho. A permissão para consultar ou alterar essas tabelas precisa existir no ambiente em que elas rodam.

No Databricks, nomes como `catalogo.schema.tabela` indicam onde o objeto está. O notebook 00 cria um schema de estudo a partir da identidade autenticada obtida por `current_user()`. O nome evita colisões acidentais entre alunos; não concede isolamento por si só.

## Confira na sua conta

- Verifique permissões próprias e herdadas no catálogo, schema, tabelas e volumes usados.
- Diferencie acesso de leitura, criação e alteração. Um leitor de dashboard não precisa necessariamente alterar a Silver.
- Em uma conta compartilhada, teste com outra identidade de estudo se ela acessa um objeto que deveria ser restrito.
- Verifique separadamente o acesso a experimentos MLflow, arquivos exportados e consultas compartilhadas.

Os privilégios necessários variam com a operação. Use a [referência oficial de Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/access-control/privileges-reference) e a política da sua organização. O projeto não aplica grants amplos nem modifica permissões automaticamente.

## Fontes externas

Os notebooks básicos geram a fonte em memória. Para estudar a ingestão de um arquivo, você pode criar um volume de estudo e enviar `data/vendas_sinteticas.csv` pela interface. Um caminho de volume tem a forma `/Volumes/catalogo/schema/volume/arquivo.csv`.

Conferir acesso ao volume é parte desse exercício adicional. Não troque o arquivo por dados de clientes numa conta pessoal sem autorização da organização. O roteiro deste repositório usa apenas dados artificiais.

## Segredos e saídas

Esta versão não precisa de chave de API. Se uma extensão futura conectar um serviço, mantenha o segredo no mecanismo apropriado do ambiente e fora do código, das imagens, dos logs e das saídas de notebooks. Um arquivo ignorado pelo Git ainda pode vazar por uma exportação manual.

Ao exportar para o GitHub, desative a inclusão das saídas de execução. Revise também prints, gráficos, caminhos pessoais e configurações de conexão. Os notebooks entregues aqui estão sem saídas.

## Público e privado

O app local exibe a mesma fonte fictícia para qualquer visitante e não permite guardar dados privados, conectar contas nem administrar outros usuários. Essa decisão torna desnecessário um login para o escopo da demonstração.

Um produto que passe a guardar progresso pessoal, conectar dados reais ou cobrar por acesso precisa de autenticação e autorização no servidor, isolamento e operação própria. O [roadmap](ROADMAP.md) registra essa mudança de escopo.
