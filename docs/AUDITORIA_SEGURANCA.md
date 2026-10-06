# Resumo da auditoria de segurança

**Versão:** 1.0. **Data:** 6 de outubro de 2026. **Referência solicitada:** [os 21 pontos da NotKode](https://notkode.com.br/pt/recursos/hub-de-conteudos/checklist-de-seguranca).

| Gravidade | Falhas confirmadas no escopo inspecionado |
|---|---|
| Crítico | 0 |
| Alto | 0 |
| Médio | 0 |
| Baixo | 0 |

Isso significa que esta inspeção não encontrou uma falha de segurança confirmada nos caminhos exercitados. **Não é uma certificação de segurança.** Há cinco temas com revisão manual pendente, descritos abaixo. Não foram inspecionados um serviço publicado ou uma conta Databricks. A entrega usa um repositório novo, com o histórico de publicação revisado.

## Escopo e evidência

O app permite estudar dados fictícios gerados internamente. Não recebe arquivos, conecta contas, mantém usuários, executa pagamentos nem armazena dados privados. O editor cria uma cópia SQLite em memória para cada consulta; somente leitura de `silver_vendas` e funções aprovadas são permitidas.

Foram inspecionados `app.py`, `src/lab/`, notebooks, configuração Streamlit, requisitos, lockfile, scripts e workflows. Os testes locais passaram: **54 testes** em Python 3.12, incluindo reconciliação, versões inválidas, campos nulos, formato da fonte, corte temporal, páginas do app e tentativas de abuso do SQL. A transformação do notebook 00 passou também por **três cenários Spark 4.0.1**, reconciliados com Pandas.

As 52 versões fixadas no lockfile e as duas dependências opcionais de validação Spark, incluindo dependências transitivas e ferramentas de teste e imagem, foram consultadas no OSV: **54 pacotes, nenhum advisory retornado** na data da consulta. Uma resposta vazia não comprova ausência de vulnerabilidades desconhecidas; a CI repete a consulta e falha se houver achados ou se a auditoria não terminar.

A busca limitada de segredos cobre padrões de tokens Databricks, GitHub, chaves de API, identificadores de acesso AWS e chaves privadas, sem imprimir os valores. O script inspeciona também todos os blobs do histórico quando existe um repositório Git local. Não é um detector universal. Os notebooks entregues não têm saídas de execução.

## Os 21 pontos aplicados à versão

`[OK]` indica evidência no escopo local. Quando o recurso não existe, isso está explicitado. `[PRECISA DE REVISÃO MANUAL]` indica que falta observar a conta, o histórico ou a hospedagem. Nenhum item ficou marcado como `[FALHOU]` nesta inspeção.

| Nº | Tema resumido | Estado | Evidência ou pendência |
|---|---|---|---|
| 1 | Credenciais de serviços | [OK] | Nenhuma integração precisa de token; o app não faz chamadas a uma conta Databricks |
| 2 | Exclusão de `.env` | [OK] | `.gitignore` cobre `.env`, variantes e `secrets.toml`; esses arquivos não estão no pacote |
| 3 | Segredos no fonte | [OK] | Inspeção e busca limitada de padrões sem imprimir valores; dados artificiais |
| 4 | Acesso autenticado | [PRECISA DE REVISÃO MANUAL] | Demo local pública; não há dados privados. Login e sessão na conta Databricks e num futuro produto não foram testados |
| 5 | Autorização central | [OK] | Authorizer no servidor bloqueia operações SQLite; não depende de esconder botões |
| 6 | Identidade verificada | [OK] | Nenhum ID de usuário recebido do navegador decide acesso. O schema nativo usa `current_user()` |
| 7 | Separação de usuários | [PRECISA DE REVISÃO MANUAL] | Não há dados pessoais no app. Permissões e isolamento entre identidades no Unity Catalog precisam de teste real |
| 8 | Privilégios dos dados | [PRECISA DE REVISÃO MANUAL] | SQLite é temporário; privilégios próprios e herdados das tabelas Delta não foram acessados |
| 9 | Regras dos serviços | [OK] | Não aplicável ao app: não há Firebase, Supabase nem buckets conectados |
| 10 | Áreas administrativas | [OK] | Não aplicável: não existem páginas ou ações administrativas |
| 11 | Configuração publicada | [OK] | Configuração usa toolbar de visualização, logs em warning e detalhes de exceção desativados |
| 12 | Respostas de falha | [OK] | Erros SQL são convertidos em uma mensagem controlada; detalhes internos não são exibidos |
| 13 | Entradas externas | [OK] | Limites no backend; formato da fonte validado; nulos vão para a quarentena; testes de entradas fora do contrato |
| 14 | Conteúdo renderizado | [OK] | SQL fica em textarea e tabelas. O único HTML permitido é CSS constante; nenhuma entrada é interpolada nele |
| 15 | Envio de arquivos | [OK] | Não aplicável ao app: não há upload. O CSV sintético pode ser baixado; upload a volumes é um exercício manual na conta |
| 16 | Consultas e injeção | [OK] | Escrita, PRAGMA, arquivos, extensões e recursão bloqueados. Nomes de catálogo e tabela nos notebooks são validados antes da interpolação |
| 17 | Limites de acesso | [PRECISA DE REVISÃO MANUAL] | Consulta e dados têm orçamento local. Não há login; limites por IP, concorrência e proteção contra abuso dependem da hospedagem futura |
| 18 | Histórico do repositório | [OK] | Repositório novo; README inicial conferido e blobs dos commits de entrega inspecionados. A CI baixa o histórico completo e repete a busca limitada de padrões |
| 19 | Políticas HTTP | [PRECISA DE REVISÃO MANUAL] | CORS e XSRF estão ligados no Streamlit. TLS, headers, WebSocket, cookies e proxy precisam ser conferidos no ambiente publicado |
| 20 | Tentativas de abuso | [OK] | Testes tentam alteração, leitura de arquivo, extensão, recursão e join custoso; a próxima consulta continua intacta |
| 21 | Revisão do conjunto | [OK] | Código, configuração, dependências e limites foram revistos; as lacunas estão registradas neste relatório |

## Os cenários efetivamente testados

| Papel | Ação | Resultado ou limite |
|---|---|---|
| Visitante sem login | Ler dados da demonstração | Permitido por intenção: todos são fictícios |
| Visitante malicioso | DROP, DELETE, UPDATE, ATTACH, PRAGMA | Bloqueados pelo backend e pelos testes |
| Visitante malicioso | Ler `sqlite_master`, carregar extensão ou arquivo | Bloqueado; não há caminho externo autorizado |
| Visitante malicioso | Recursão ou join que ultrapassa o orçamento | Rejeitado ou interrompido |
| Usuário de outra conta | Ler ou modificar tabela privada no Databricks | Não testado; depende dos privilégios reais do catálogo |
| Administrador | Gerenciar usuários ou recursos privados no app | Fora do escopo; não existem esses recursos |

## Achados confirmados

Foi corrigida uma falha de qualidade: valores nulos podiam virar o texto `None` no caminho local, enquanto a lógica de três valores do Spark podia perder uma chave nula antes da quarentena. Os dois caminhos agora normalizam nulos para vazio na validação, preservam a Bronze e reconciliam as contagens. Estruturas fora do contrato da fonte recebem erro controlado. Essa falha não demonstrou acesso indevido nem exposição de dados.

O empacotamento passou a usar uma seleção explícita de pastas e formatos, com exclusão de ambientes, caches e artefatos temporários. A verificação do projeto é obrigatória antes de gerar o ZIP, e a integridade do arquivo é conferida depois.

## Cinco verificações antes de oferecer um produto publicado

1. **Ambiente e público:** decidir quais dados serão públicos e quais ações serão privadas; testar autenticação e sessão para qualquer recurso privado implementado.
2. **Conta e dados:** revisar Unity Catalog, volumes e experimentos; testar leitura e alteração com uma segunda identidade autorizada para o teste.
3. **Hospedagem:** verificar TLS, headers, cookies, CORS e WebSocket, além de limites por IP e concorrência em um ambiente concreto.
4. **Publicação no Git:** inspecionar o histórico de destino e as saídas exportadas. Trocar qualquer credencial eventualmente descoberta no serviço que a emitiu.
5. **Revalidação:** executar os notebooks na conta, repetir testes e consulta de dependências e auditar as novas funções de cadastro, upload, IA ou pagamento se forem adicionadas.

O roteiro de [validação Databricks](VALIDACAO_DATABRICKS.md) registra os passos que ainda precisam da conta. O [roadmap](ROADMAP.md) descreve o que muda quando o material vira serviço comercial.
