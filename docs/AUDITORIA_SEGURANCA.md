# Revisão de segurança do Lab Bricks

**Versão 3.0 · 8 de outubro de 2026.** Referência solicitada: [checklist de 21 pontos da NotKode](https://notkode.com.br/pt/recursos/hub-de-conteudos/checklist-de-seguranca).

A inspeção não encontrou falha de segurança confirmada nos caminhos locais exercitados. Isso não é certificação nem comprovação de um serviço hospedado. Cinco temas exigem revisão de conta/hospedagem. O repositório existente foi renomeado preservando histórico, com busca limitada de padrões também nos blobs Git.

## Escopo e evidências

- App com dados sintéticos e amostra pública licenciada; caderno/progresso pessoal na sessão, sem cache compartilhado de informações pessoais.
- Importação **somente de JSON de progresso, caderno e feedback**: até 100 KB no backend, formato/versão/chaves exatos, lista limitada e IDs conhecidos. Não executa código, pickle, caminhos nem URLs e não grava o arquivo no servidor.
- Dois editores SQL com cópia SQLite efêmera. Authorizer permite leitura apenas das tabelas internas e funções aprovadas. Bloqueia escrita, catálogos do SQLite, arquivos, extensões, PRAGMA e recursão; tamanho, linhas e instruções são limitados.
- Busca sobre aulas próprias, benchmark semântico congelado e RAG extrativo com limites. Geração local é um comando opcional, separado do app, sem ferramentas ou chave de API.
- Página Adicionar conteúdo gera download; não inclui arquivos nem modifica o servidor. Mantenedores adicionam arquivos pelo Git.
- **169 testes locais aprovados**, incluindo 23 páginas do app, 14 exercícios com soluções, limites de progresso, SQL com múltiplas tabelas, cardinalidade, reprocessamento e avaliação temporal.
- **Sete cenários Spark 4.0.1 aprovados**: três de qualidade/versões/nulos, um JSON, um BI com janela, Gold público e streaming com replay. Sem Delta ou serviços de conta.
- **69 dependências fixadas consultadas no OSV**, sem advisories retornados nesta consulta. Isso não prova ausência de vulnerabilidades desconhecidas. A CI repete a auditoria e falha se não terminar ou encontrar achados.
- Fonte, sintaxe, links locais, catálogo, pares de notebooks, CSV e histórico inspecionados. A busca de segredos cobre padrões conhecidos, sem imprimir valores; não é universal.

## Checklist aplicado

`OK` indica evidência no escopo descrito. `Manual` exige um ambiente real. `Não aplicável` explicita a ausência do recurso.

| Nº | Tema resumido | Estado | Evidência / pendência |
|---|---|---|---|
| 1 | Credenciais de serviços | OK | App não solicita token nem conecta conta; bundle sem credenciais |
| 2 | Exclusão de `.env` | OK | Ignore/empacotamento excluem arquivos de segredo |
| 3 | Segredos no fonte | OK | Busca limitada de padrões; dados e conteúdo próprios |
| 4 | Acesso autenticado | Manual | Demo sintética local; autenticação de conta/hospedagem não testada |
| 5 | Autorização central | OK | Authorizer SQLite no backend, não só interface |
| 6 | Identidade verificada | OK | Input do navegador não decide acesso; namespace nativo usa current_user |
| 7 | Separação de usuários | Manual | Progresso de sessão; UC/isolamento real precisam de segunda identidade |
| 8 | Privilégios de dados | Manual | Tabelas/volumes/experimentos reais não foram acessados |
| 9 | Regras dos serviços | Não aplicável | Sem Firebase, Supabase ou buckets conectados no app |
| 10 | Áreas administrativas | OK | Gerador só baixa template; não escreve nem concede privilégios |
| 11 | Configuração publicada | OK | Toolbar viewer, erros internos ocultos, telemetria desativada |
| 12 | Respostas de falha | OK | Mensagens controladas para SQL e progresso inválido |
| 13 | Entradas externas | OK | Limites de query/dados/JSON/busca; IDs de template validados |
| 14 | Conteúdo renderizado | OK | Markdown sem HTML arbitrário; único unsafe HTML é CSS constante |
| 15 | Envio de arquivos | OK | JSON restrito, até 100 KB no backend, sem persistir/executar; teste negativo |
| 16 | Consultas e injeção | OK | Leitura autorizada e nomes nativos validados; fontes de bundle sem token |
| 17 | Limites de acesso | Manual | Orçamentos locais existem; IP, concorrência e abuso dependem da hospedagem |
| 18 | Histórico Git | OK | Busca limitada de blobs; checkout CI com histórico completo |
| 19 | Políticas HTTP | Manual | CORS/XSRF ligados; TLS/headers/cookies/proxy não inspecionados |
| 20 | Tentativas de abuso | OK | DDL/DML, catálogo, arquivo, extensão, recursão, JSON excessivo e IDs inválidos testados |
| 21 | Revisão do conjunto | OK | Código, configuração, conteúdo, dependências e pacote; limites registrados |

## Testes negativos relevantes

| Entrada / ação | Comportamento |
|---|---|
| DROP/UPDATE/DELETE/ATTACH/PRAGMA ou sqlite_master | Bloqueio no editor de leitura |
| Consulta recursiva/custosa | Recusa/interrupção por authorizer e orçamento |
| JSON acima de 100 KB, versão bool ou aula desconhecida | Erro controlado; sem restaurar progresso inválido |
| ID de template com caminho ou caracteres inesperados | Recusa antes de gerar nome de arquivo |
| Dimensão duplicada no JOIN | Falha de cardinalidade antes de publicar receita |
| Mesmo ID de lote com outro conteúdo | Falha de contrato, em vez de ignorar correção ambígua |
| Documentos com instruções de ação | São dados de leitura; busca não possui ferramenta de execução |

## Pendências do ambiente concreto

Antes de acrescentar dados privados ou publicar um serviço, confira autenticação/sessão, matriz UC e privilégios herdados, isolamento com outra identidade, limites por IP/concorrência e políticas HTTP/TLS. Execute também recursos nativos e teste falha/reprocessamento. Essas cinco classes de pendência não são apresentadas como controles já validados.

A importação de progresso substituiu o antigo “não há upload”: este caminho novo foi revisado e testado. A página de template é uma ferramenta de preparação, não um cadastro administrativo. Livros/PDFs e outputs de conta continuam fora da entrega. Veja [validação nativa](VALIDACAO_DATABRICKS.md) e [roadmap](ROADMAP.md).

## Ampliação 3.0 e referência externa

Caderno e feedback: JSON de até 100 KB com IDs conhecidos, contagens coerentes e sem execução. Vetores: NPZ sem pickle, checksum e dimensão. Entradas SQL continuam sob authorizer. Downloads opcionais têm revisão/checksum, ficam fora do repositório e não iniciam no app. Geração local não certifica resistência a injeção ou suporte factual.

A tabela de 21 temas foi preservada da revisão anterior e atualizada com evidência local. O endereço solicitado da NotKode respondeu HTTP 404 nesta retomada; seu texto externo não pôde ser reconferido. Autenticação, isolamento de conta, privilégios, limites de hospedagem e políticas HTTP continuam manuais. OSV não cobre engine nativo ou pesos.
