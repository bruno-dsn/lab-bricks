+++
id = "f03-python"
title = "Leia e transforme um DataFrame"
track = "fundamentos"
level = "Iniciante"
version = "2.0"
prerequisites = ["f02-grao"]
sources = ["engenharia-livro", "ml-livro"]
objectives = ["Selecionar, filtrar e agregar dados", "Distinguir transformação e efeito de execução"]
lab = "Pipeline e qualidade; notebooks 00 e 02"
+++

# Leia e transforme um DataFrame

## Problema

Uma pessoa recebe a instrução “filtre os concluídos e calcule receita”. Ela precisa traduzir essa frase em operações sem alterar a definição de venda nem converter dinheiro duas vezes.

## Conceito

Um DataFrame representa dados tabulares com nomes e tipos. Em Pandas, as operações são executadas localmente. Em Spark, transformações normalmente constroem um plano; ações como `count`, `collect` ou escrita disparam a execução. Esse comportamento ajuda o otimizador, mas um `collect` de uma tabela grande pode exceder a memória do driver.

Comece com seleção de colunas, filtro, coluna calculada e agregação. O contrato do primeiro gerador usa strings; a Silver normaliza tipos e mantém valores em centavos. Na camada de apresentação, dividimos por 100. Prefira operações vetorizadas ou expressões Spark a loops Python sobre cada linha.

## Exemplo explicado

```python
from lab.dados import gerar_vendas
from lab.pipeline import tratar
r = tratar(gerar_vendas())
concluidas = r.silver.loc[r.silver["status"] == "concluida"]
receita = concluidas["valor_centavos"].sum() / 100
```

O filtro escolhe a população. A soma ocorre em centavos inteiros. A divisão converte o resultado para exibição; não modifica o valor armazenado.

## Experimente

Use o SQL local para obter a mesma soma. No notebook 02, encontre a expressão Spark equivalente e inspecione o schema. Acrescente uma agregação por canal e reconcilie a soma dos canais com o total. Não cole código `lab.*` no Databricks sem importar o projeto: os notebooks nativos já incluem as funções necessárias.

## Resultado esperado

SQL e Pandas retornam o mesmo total de centavos no mesmo conjunto Silver. Cada canal contribui para o total; a soma das partes não depende da ordem de exibição.

## Erros comuns

Somar strings; executar `collect` para milhões de linhas; usar `float` para dinheiro operacional; esquecer que Spark é lazy e interpretar a criação de um plano como tempo de execução completo.

## Desafio

Escreva uma transformação em três passos e uma verificação com `assert` da reconciliação. Descreva que etapa dispararia execução no Spark.

## Critério de conclusão

Você executa filtro, seleção e agregação, identifica os tipos e explica a diferença entre plano e ação.

## Referências

Referências: guias de engenharia e ML fornecidos; [guia de DataFrames Spark](https://spark.apache.org/docs/latest/sql-programming-guide.html).
