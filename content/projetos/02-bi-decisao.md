# Projeto 02 · Um painel sem receita multiplicada

**Objetivo:** modelar pedidos de vários itens, produzir indicadores e justificar uma decisão comercial. **Trilhas:** SQL/BI e fundamentos. **Tempo sugerido:** 4–6 horas. **Ambiente:** app local; AI/BI dashboard opcional em conta.

## Enunciado

Uma loja tem clientes, produtos, pedidos e itens. Um pedido pode ter até três produtos distintos. A gestão quer receita e margem bruta por categoria e canal, ticket por pedido e evolução diária. Você precisa demonstrar que o JOIN preserva o grão e que cancelados não inflaram o resultado.

## Entregas

1. Mapa de tabelas, chaves e cardinalidades.
2. Dicionário de métricas com filtro, período, unidade e fórmula.
3. Três queries: receita/margem por categoria; ticket por canal; acumulado diário.
4. Verificações de unicidade das dimensões e cobertura de chaves.
5. Painel local ou AI/BI com filtros e totais reconciliados.
6. Uma recomendação comercial e uma limitação dos dados.

## Caminho orientado

Abra BI e modelagem com 180 pedidos e semente 42. Conte 180 pedidos totais e 164 concluídos. Conte linhas de itens separadamente. Inspecione o preço gravado no item: ele preserva o preço praticado, enquanto a dimensão descreve o produto. Use `COUNT(DISTINCT pedido_id)` para contar pedidos depois do JOIN.

Reconcilie receita em centavos antes de arredondar. Margem bruta é receita menos custo de mercadoria; não use o termo lucro líquido. Crie uma janela depois de fixar o grão diário. A última receita acumulada deve coincidir com o total.

Teste um caso negativo: duplique uma chave da dimensão em uma cópia local. A montagem de fatos deve recusar a relação muitos-para-um. Depois filtre uma região/canal no app e confira indicadores com a fato filtrada. As queries livres do editor usam as tabelas completas: inclua seu WHERE quando quiser reproduzir o filtro do painel.

Na conta, execute notebook 05, crie datasets AI/BI e revise credenciais de compartilhamento. Registre o warehouse usado e teste duas combinações de filtro. Não considere publicar uma captura de tela como validação da permissão.

## Rubrica

| Critério | Evidência | Pontos |
|---|---|---|
| Grão e cardinalidades | Modelo e teste de dimensão duplicada | 25 |
| Métricas corretas | Queries reconciliadas | 25 |
| CTE e janela | Último acumulado = total | 15 |
| Leitura do painel | Filtros, unidade e população claras | 20 |
| Decisão e limite | Recomendação sem causalidade inventada | 15 |

**Conclusão recomendada:** pelo menos 80/100 e nenhum total financeiro sem reconciliação.

## Extensão

Acrescente uma promoção com preço praticado diferente do preço atual. Mostre por que reconstruir a receita pelo preço da dimensão erra. Depois planeje histórico de dimensão tipo 2 para região do cliente; explique data de vigência e JOIN temporal sem afirmar que a extensão já está implementada.
