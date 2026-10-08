# Caso público: Online Retail

Fonte: Daqing Chen (2015), UCI Online Retail, DOI [10.24432/C5BW33](https://doi.org/10.24432/C5BW33), licença [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Atribuição e transformações também estão em data/LICENSES.md e data/online_retail_meta.json.

A amostra contém as primeiras 3.000 linhas na ordem do arquivo original. CustomerID foi removido; cabeçalhos foram traduzidos; datas seriais do Excel viraram texto sem inventar um fuso. Não foram acrescentados defeitos artificiais. Datas mistas e outros extremos aparecem em fixtures de teste, identificadas como tal.

## Contrato

Bronze tem oito colunas ordenadas: linha_fonte, fatura, produto, descricao, quantidade, data, preco_gbp e pais. Linha de origem é única e preenchida. Descrição e identificadores textuais são obrigatórios. Quantidade é inteira e não nula; preço é positivo e finito. Fatura iniciada por C deve ter quantidade negativa. Um horário com fuso explícito é rejeitado porque este contrato preserva horário local desconhecido.

Silver normaliza texto, números e data. Decimal e ROUND_HALF_UP convertem preço unitário para pence antes de multiplicar pela quantidade. Essa é uma política didática declarada; outra política de arredondamento exige reconciliação própria.

Quarentena preserva linha e motivo. Uma duplicata é a mesma linha normalizada inteira, exceto o número de origem; repetir produto na mesma fatura não basta para descartá-lo. Linhas substituídas têm registro próprio.

## Resultado observado

3.000 = 2.946 Silver + 10 rejeitadas + 44 substituídas. A união das três partições cobre a entrada. A Gold de 2010-12-01 tem 5.714.556 pence de venda bruta, 32.523 de estornos e 5.682.033 de receita líquida, em GBP.

Esse recorte representa um dia. Não use para validação de previsão, sazonalidade ou generalização de comportamento comercial. A sujeira presente é suficiente para ensinar rejeição e duplicação; não inclui toda a variedade prometida em um dataset maior.

## Reproduzir e praticar

```bash
python scripts/reproduzir_dados_reais.py --help
python scripts/corrigir.py ex08_retail
```

O script confere o hash do ZIP original, extrai somente o subconjunto documentado e verifica a amostra. Veja os parâmetros no help antes de baixar. A amostra já está incluída; o app não baixa dados ao abrir. SHA-256 da amostra: e9b8b91ded2e05b4adfa6cb226a31957547d8be1beedb21b10b58c5669659940.

Explique por que a fatura não identifica uma linha, por que receita pode conter estorno e por que somar antes de validar perde rastreabilidade. Entregue um relatório que reconcilie contagens e valores. Notebook 12 leva a Gold ao Spark; sua execução em Databricks permanece pendente.
