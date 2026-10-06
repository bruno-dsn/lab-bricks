# Entender as peças antes de escrever código

Uma loja recebe pedidos do site, aplicativo e marketplace. No começo, uma planilha ajuda a reunir os valores. Com novas fontes e atualizações, você precisa manter a regra da receita, conferir versões e executar o tratamento de forma repetível.

O problema do nosso projeto é essa confiabilidade. A amostra pequena permite inspecionar tudo. Quando o volume exigir processamento distribuído, a mesma regra de negócio precisa continuar valendo.

## Cada nome resolve uma parte

| Peça | O que faz | No nosso caso |
|---|---|---|
| Databricks | Ambiente para trabalhar com dados e modelos, executar código e organizar acesso | Hospeda os notebooks e as tabelas do projeto |
| Apache Spark | Motor de processamento com DataFrames e SQL | Transforma a fonte e agrega pedidos |
| Delta Lake | Formato de tabela com transações e histórico | Guarda snapshots e permite demonstrar MERGE e versões |
| Unity Catalog | Governa objetos e permissões | Define quem pode consultar ou alterar as tabelas |
| MLflow | Registra experimentos e suas métricas | Pode guardar a comparação entre modelo e baseline |

Pense numa consulta de receita. O Databricks é o ambiente em que você trabalha; Spark executa a transformação; Delta organiza os arquivos e o estado da tabela; Unity Catalog controla o acesso. O mesmo pedido passa por essas responsabilidades sem virar quatro pedidos diferentes.

## Uma ponte a partir de planilhas

| Operação conhecida | Ideia equivalente no exercício |
|---|---|
| Filtrar linhas | `WHERE status = 'concluida'` |
| Criar uma coluna de total | `quantidade * preco_unitario` |
| Tabela dinâmica por canal | `GROUP BY canal` com `SUM` |
| Corrigir o tipo da coluna | Converter texto para data, inteiro ou decimal |
| Conferir duplicatas | Definir uma chave e uma regra de versão |

Essa ponte ajuda a entender a intenção. Spark não executa uma fórmula por célula como uma planilha: você declara operações sobre conjuntos de dados. Muitas transformações só são avaliadas quando uma ação, como salvar ou contar, exige o resultado.

## Distribuição tem custos

Dividir o trabalho entre máquinas pode ajudar com grandes conjuntos. Movimentar dados entre partições também custa tempo. Um `GROUP BY` pode exigir essa movimentação, conhecida como shuffle. Aumentar máquinas não corrige uma métrica mal definida e não garante ganho para uma amostra minúscula.

No laboratório local não há cluster Spark. Ele serve para visualizar as regras. Nos notebooks, Spark e Delta executam na conta Databricks. A distinção permite testar o raciocínio sem confundir uma simulação de camadas com uma medição de desempenho da plataforma.

## Experimento de compreensão

Descreva o percurso de um pedido cancelado. Ele chega à Bronze, passa pela validação e pode ficar na Silver porque cancelamento é um status conhecido. A consulta de receita o exclui. Agora explique onde a permissão de leitura é verificada: isso cabe ao ambiente e ao catálogo, não ao filtro de status.
