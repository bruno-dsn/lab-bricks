# Seu primeiro contato com o projeto

Você pode começar pelo app mesmo sem conhecer Spark. A primeira tarefa é entender uma receita: quanto entrou em pedidos concluídos, depois de eliminar versões repetidas e rejeitar os registros que não seguem a regra.

## Rodar no computador

Instale Python 3.12. Extraia o projeto para uma pasta e abra o terminal nessa pasta. Crie um ambiente virtual e instale o lockfile seguindo os comandos do [README](../README.md). O comando `streamlit run` inicia um servidor no seu computador; o endereço informado deve começar com `http://localhost` ou `http://127.0.0.1`.

O endereço local não é um site publicado. Para estudar, use `--server.address 127.0.0.1`. Se a porta 8501 estiver ocupada, acrescente `--server.port 8502`.

No menu **Pipeline e qualidade**, deixe os erros ligados. Procure a data impossível, o preço negativo e o produto vazio. Cada registro rejeitado mostra seu motivo. Agora desligue a opção e compare as contagens.

## Levar para a plataforma

1. Crie uma conta de estudo na [Databricks Free Edition](https://docs.databricks.com/aws/en/getting-started/free-edition).
2. No Workspace, crie uma pasta para o projeto e use **Import** para carregar cada arquivo `.py` de `notebooks/`.
3. Importe todos para a mesma pasta. O `%run ./00_configuracao` depende disso.
4. Execute o 00. No widget `catalogo`, escolha um catálogo em que possa criar schemas. O padrão é o catálogo atual da sessão.
5. Use o mesmo catálogo no 01, 02, 03 e 04. Confirme o nome do schema exibido: ele começa com `dbnp_`.
6. Execute em ordem e compare os resultados com [VALIDACAO_DATABRICKS.md](VALIDACAO_DATABRICKS.md).

Os notebooks geram os dados internamente. Você não precisa baixar o CSV da internet, usar DBFS root, montar buckets ou colocar credenciais no código. O CSV do repositório é uma forma adicional de inspecionar a mesma fonte.

## Quando uma execução parar

| Situação | Próximo passo |
|---|---|
| Permissão negada ao criar o schema | Escolha um catálogo de estudo autorizado; em uma conta corporativa, peça o acesso ao responsável |
| `%run` não encontra o 00 | Confirme que os notebooks estão na mesma pasta e mantiveram os nomes |
| Tabela Silver ou Gold inexistente | Execute o 02 no mesmo catálogo e com a mesma identidade |
| Pandas ou scikit-learn ausente no 04 | Adicione a biblioteca pelo ambiente do notebook e reinicie a execução |
| Limite da Free Edition atingido | Aguarde a renovação da cota; continue pelo laboratório local |

Não substitua o schema de estudo por um schema de trabalho com dados reais. Rerodar 02 sobrescreve as tabelas de estudo para reproduzir o exemplo.

## Primeira entrega de estudo

Escreva um parágrafo explicando por que o total da Bronze é diferente do total da Silver. Acrescente uma consulta que calcula a receita. Se você consegue justificar o filtro de status e a escolha da versão, já compreendeu o primeiro problema do projeto.
