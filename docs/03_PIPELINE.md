# Um pipeline que explica seus números

Recebemos 727 registros. A lista contém 720 pedidos, uma nova versão de um deles e seis registros inválidos. A fonte guarda campos como texto, reproduzindo um CSV exportado de outra ferramenta.

## Bronze preserva a entrada

Salvar o que chegou permite investigar uma divergência. Se uma linha trouxe uma quantidade zero, a Bronze mantém esse valor. Ela também recebe `_ordem`, a posição do registro na fonte, para tornar o desempate das versões determinístico neste exercício.

Os notebooks recriam esse snapshot pequeno a cada execução. Um sistema real pode preservar lotes com identificadores e histórico de ingestão, em vez de substituir a Bronze. Esse comportamento é uma extensão de engenharia, não está implementado como streaming aqui.

## Silver escolhe a versão e valida

Primeiro, uma chave vazia ou uma atualização ilegível é rejeitada. Entre os demais registros da mesma chave, vence a atualização mais recente; a ordem da fonte desempata. As versões antigas seguem para uma tabela separada. Aplicamos então as regras de negócio na versão vigente.

Campos nulos são tratados como vazios na validação, enquanto a Bronze conserva o valor recebido. A biblioteca local exige uma lista de dicionários com as nove colunas e valores de texto ou nulos; estruturas fora desse contrato produzem um erro controlado.

| Regra | Exemplo de rejeição |
|---|---|
| Data ISO existente | `2026-02-30` |
| Quantidade inteira entre 1 e 1.000 | `0` |
| Preço positivo, com até duas casas | `-9.90` |
| Produto, categoria e canal preenchidos | Produto vazio |
| Status `concluida` ou `cancelada` | `desconhecida` |
| Chave e atualização válidas | ID vazio |

Se uma versão recente tiver preço inválido, o pedido é rejeitado. A versão antiga não reaparece como se fosse a atual. Isso evita esconder uma falha da origem.

Os rejeitados guardam os campos da fonte e o motivo. Corrigir a origem e reenviar o registro é uma ação diferente de ignorar o erro.

## Gold responde uma pergunta específica

A Gold agrega pedidos concluídos por dia. Guarda a contagem de pedidos, a receita em centavos, a receita em reais e o ticket médio. Não calcula lucro, pois o contrato não inclui custos nem tributos.

Um dia sem pedidos concluídos não aparece nessa agregação. No experimento de ML, reindexamos o calendário e preenchemos dias ausentes com receita zero para que um atraso de um dia continue significando um dia de calendário.

## Reconciliação

```text
727 recebidos = 720 na Silver + 6 rejeitados + 1 versão substituída
```

Essa igualdade trata o destino dos registros, inclusive cancelamentos válidos. Outra igualdade trata a receita: a soma em centavos da Gold precisa coincidir com a soma dos pedidos concluídos na Silver.

Alterar uma regra sem revisar os testes pode tornar um pipeline consistente com o código e errado para o negócio. Antes de incluir uma regra nova, escreva uma entrada pequena com o resultado que você espera.
