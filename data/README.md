# Contrato da fonte fictícia

`vendas_sinteticas.csv` foi gerado com semente 42 e 720 pedidos, mais seis linhas inválidas e uma versão adicional. Não contém clientes, emails, endereços ou transações reais.

Cada linha representa a versão de um pedido com um único produto. Os nove campos chegam como texto. A chave lógica é `venda_id`; `atualizado_em` define a versão. A ordem da lista gerada desempata timestamps iguais somente neste exercício.

Na transformação, um campo nulo equivale a um campo vazio para as regras de qualidade; não vira o texto `None`. A Bronze mantém a entrada original e a quarentena registra o motivo.

| Campo | Origem | Regra na versão vigente |
|---|---|---|
| venda_id | Texto | Preenchido; único após deduplicação |
| data_venda | AAAA-MM-DD | Data existente |
| produto | Texto | Preenchido |
| categoria | Texto | Preenchida |
| canal | Texto | Preenchido; canais da fonte: Site, Aplicativo, Marketplace |
| quantidade | Texto numérico | Inteiro entre 1 e 1.000 |
| preco_unitario | Texto decimal em reais | Positivo; até 8 dígitos inteiros e 2 decimais |
| status | Texto | concluida ou cancelada após normalização |
| atualizado_em | AAAA-MM-DD hh:mm:ss | Timestamp existente |

Silver acrescenta `preco_centavos` e `valor_centavos`, ambos inteiros. Gold resume pedidos concluídos por data.

Os preços são representados com ponto decimal na fonte, por exemplo `24.90`. Valores com vírgula exigiriam uma regra explícita de normalização que este contrato não inclui.
