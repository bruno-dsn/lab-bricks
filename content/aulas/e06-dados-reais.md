+++
id = "e06-dados-reais"
title = "Um caso público: da origem à reconciliação"
track = "engenharia"
level = "Intermediário"
version = "3.0"
prerequisites = ["e01-medallion", "f04-contrato"]
sources = ["uci", "engenharia-livro"]
objectives = ["Executar a prática e explicar o resultado", "Identificar um erro e provar a correção"]
lab = "Dados públicos reais e notebook 12"
+++

# Um caso público: da origem à reconciliação

## Problema
Um gerador limpo não mostra como uma fonte real quebra expectativas. Agora você vai tratar linhas públicas de vendas do UCI Online Retail, com descrições ausentes, devoluções e duplicatas reais.

## Conceito
Bronze preserva oito campos e o identificador da linha de origem. Silver converte quantidade, data e preço com contrato explícito. Valores monetários viram centavos inteiros com Decimal e arredondamento definido. Faturas começadas por C representam cancelamento e exigem quantidade negativa. Valores negativos válidos não são descartados como sujeira: entram como estorno. Uma linha inválida vai à quarentena com motivo. Duplicatas são linhas inteiras idênticas após normalização, não apenas pares fatura/produto: um produto pode aparecer mais de uma vez legitimamente.

## Exemplo explicado
A amostra contém as primeiras 3.000 linhas da planilha pública. CustomerID foi removido. O pipeline reconcilia 3.000 = 2.946 Silver + 10 rejeitadas + 44 substituídas. A receita líquida é 5.682.033 centavos de GBP. Esta amostra cobre um dia e não sustenta previsão sazonal nem resultados gerais sobre o varejo.

## Experimente
Abra Dados públicos reais e inspecione a descrição ausente, a duplicata e o cancelamento. Faça ex08_retail. Reproduza a origem com `python scripts/reproduzir_dados_reais.py --archive caminho/online-retail.zip`. O hash da fonte precisa bater antes da conversão.

## Resultado esperado
Cada linha de origem aparece em exatamente uma saída. Gold apresenta venda bruta, estorno e receita líquida por dia, com moeda GBP declarada. Nenhum erro artificial foi adicionado à amostra.

## Erros comuns
Chamar GBP de reais; remover toda quantidade negativa; contar fatura como identificador único de linha; inventar um fuso horário que a fonte não documenta. Datas mistas adicionais dos testes são fixtures didáticos, não defeitos atribuídos à planilha.

## Desafio
Escolha outro recorte da fonte, registre a regra antes de olhar resultados e compare rejeições. Para expandir para o arquivo inteiro, reveja o orçamento e o contrato de até 10.000 linhas do laboratório.

## Critério de conclusão
Entregue contrato, proveniência, ledger de rejeições, reconciliação e três conclusões com limites do recorte.

## Referências
- [Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)
- Databricks Certified Data Engineer Associate Study Guide; material fornecido, não redistribuído.
