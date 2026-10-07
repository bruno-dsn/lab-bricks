# Prática nativa do Lab Bricks

Este guia prepara uma execução em ambiente de estudo. As APIs foram conferidas na documentação oficial em 7 de outubro de 2026; a conta, seus recursos e privilégios ainda precisam ser validados.

## Preparação

1. Use uma conta de estudo. Confira [Free Edition](https://docs.databricks.com/aws/en/getting-started/free-edition) e suas limitações atuais. Recursos disponíveis podem variar por cloud, conta e políticas.
2. Importe `.py` ou `.ipynb` de `notebooks`, mantendo nomes e a mesma pasta. Não importe os dois formatos como duplicatas de nomes distintos.
3. Use compute compatível. Os exercícios Spark/Delta pressupõem suporte a Unity Catalog. Os notebooks ML/busca também precisam de Pandas e scikit-learn disponíveis no ambiente.
4. Execute 00 e escolha `catalogo` onde você possa criar schemas/tabelas. O valor padrão é o catálogo atual, que você deve revisar.
5. Confira o schema `lb_<hash>` exibido. O nome reduz colisão; autorização depende de privilégios. Não execute em catálogo de produção.

Se a biblioteca ML não estiver no ambiente, configure dependências pelo mecanismo suportado no compute escolhido. As versões locais de referência são Pandas 2.2.3 e scikit-learn 1.8.0, com Python 3.12. Não instale o lock inteiro do app cegamente sobre um Databricks Runtime: pacotes preinstalados e compatibilidade do ambiente precisam ser considerados.

## Ordem e efeitos

| Arquivo | Pré-requisito | Efeito | Resultado a conferir |
|---|---|---|---|
| 00 | Catálogo autorizado | Cria schema e funções | Namespace e identidade |
| 01 | 00 via `%run` | Queries/fonte temporária | Agregações reconciliadas |
| 02 | 00 via `%run` | Recria cinco tabelas Delta do fixture | 727/720/6/1 e receita |
| 03 | 00 via `%run` | Recria destino incremental próprio; aplica MERGE | 721 chaves; reaplicação estável |
| 04 | Bibliotecas e conta para Tracking opcional | Treina modelo; pode registrar run | Datas, baseline, MAE |
| 05 | 00 via `%run` | Recria quatro tabelas `bi_*` | 164 pedidos concluídos e métricas |
| 06 | Spark | Transformações em memória | 4 mensagens, 2 rejeitadas, 3 itens e 17.600 centavos |
| 07 | 02 executado | Leitura e asserts; falha se contrato quebra | Gate aprovado |
| 08 | Volume e Auto Loader autorizados | Cria volume/arquivos/checkpoint/tabela próprios | Dez registros; reexecução estável |
| 09 | Pandas e scikit-learn | Classificação local no notebook | 480 treino/120 teste e métricas |
| 10 | scikit-learn | Busca lexical em notas próprias | IDs, trechos e recall |

O 02 e 03 são aulas com snapshots reinicializados deliberadamente. Não use essa prática como ingestão incremental de produção. O 08 usa checkpoint persistente próprio e não remove estado. Se você acrescentar arquivos na entrada, a contagem fixa de dez deixa de descrever o fixture; investigue e documente a extensão.

## Job com bundle

A configuração cria um Job com três tarefas sequenciais: 02 → 07 → 05. Usa parâmetro de Job `catalogo`, sem misturar `base_parameters` de tarefas. Não define agenda nem envia notificações. Notebook tasks sem cluster explícito usam serverless quando disponível; confira a configuração real da sua conta.

Instale a CLI Databricks atual pelo [guia oficial](https://docs.databricks.com/aws/en/dev-tools/cli/install). Autentique com o fluxo suportado, preferindo OAuth para uso interativo. Não cole token em código ou YAML.

```bash
# Troque o host pelo workspace de estudo e escolha um perfil local.
databricks auth login --host https://SEU_WORKSPACE --profile lab-bricks

# Da raiz do projeto; catalogo_estudo é um exemplo, não um destino existente.
databricks bundle validate --target dev --profile lab-bricks --var catalogo=catalogo_estudo

# Só depois de revisar o resultado e o destino na sua conta:
databricks bundle deploy --target dev --profile lab-bricks --var catalogo=catalogo_estudo
databricks bundle run lab_bricks_estudo --target dev --profile lab-bricks --var catalogo=catalogo_estudo
```

O bundle tem um destino de desenvolvimento e variável sem default, exigindo escolha explícita. O hash do namespace deriva da identidade de execução; se ela diferir da identidade interativa, o schema será diferente. Uma única execução concorrente evita colisão entre runs desse Job, mas notebooks manuais no mesmo schema ainda podem interferir.

**Limite de validação:** arquivos foram conferidos estruturalmente; não foi executado `bundle validate/deploy/run` autenticado neste trabalho. Registre CLI, workspace, identidade, catálogo, run ID e resultados depois da execução. Se `%run` relativo ou parâmetros não forem resolvidos no ambiente, confirme a pasta sincronizada e os widgets antes de alterar a configuração.

## Pipeline declarativa

`pipelines/qualidade_declarativa.py` é fonte de **Lakeflow Spark Declarative Pipelines**, não um notebook comum. Crie uma pipeline de estudo com catálogo/schema autorizados e acrescente o arquivo como fonte. O código usa `pyspark.pipelines`, materialized views e expectativas atuais.

Esperado: quatro linhas Bronze, duas Silver, duas quarentena; Gold = 1.200 centavos de concluídos. Abra o grafo e métricas depois de atualizar. A expectativa de valor é aplicada sobre as linhas já filtradas; a quarentena mantém os inválidos. Esse exemplo demonstra batch declarativo, não streaming/CDC. A disponibilidade do serviço e execução precisam de validação da conta.

## Erros e recuperação

| Sinal | O que investigar |
|---|---|
| Falha ao criar schema/tabela/volume | Catálogo, identidade e privilégios; não peça ALL PRIVILEGES automaticamente |
| Notebook não encontrado no `%run` | Nomes e mesma pasta importada/sincronizada |
| scikit-learn indisponível | Ambiente e dependências suportadas pelo compute |
| Contagem do fixture mudou | Fonte, tabelas, sequência de execução e extensões; não esconda o erro |
| Auto Loader reingere ou falha | Identidade, checkpoint, destino e mudanças de origem; preserve estado |
| Tracking não disponível | Permissão de experimento e ambiente; a avaliação local pode ser registrada manualmente |

## Migração da primeira versão

O prefixo do schema mudou de `dbnp_` para `lb_`. O código não remove tabelas antigas. Consulte o namespace novo; qualquer limpeza do anterior é uma ação separada a ser revisada pelo proprietário na conta. Não renomeie tabelas de outras pessoas para ajustar o tutorial.

Registre tudo em [VALIDACAO_DATABRICKS.md](VALIDACAO_DATABRICKS.md).
