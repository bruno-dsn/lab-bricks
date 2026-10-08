+++
id = "m10-validacao-temporal"
title = "Validação temporal com gap e teste preservado"
track = "machine-learning"
level = "Intermediário"
version = "3.0"
prerequisites = ["m07-selecao-validacao"]
sources = ["sklearn", "ml-acao-livro"]
objectives = ["Executar a prática e explicar o resultado", "Identificar um erro e provar a correção"]
lab = "Validação temporal, ex09_janelas e notebook 13"
+++

# Validação temporal com gap e teste preservado

## Problema
Você separou treino e teste por data, mas um rótulo leva dias para ficar disponível. O último treino ainda pode usar informação que não existiria no início da validação.

## Conceito
Separe os últimos 20% de datas para o teste final e use TimeSeriesSplit apenas nos 80% de desenvolvimento. Faça os cortes sobre datas distintas, não sobre linhas: todas as entregas do mesmo dia pertencem à mesma partição. O gap remove as últimas datas observadas do treino antes de cada validação e antes do refit final. Neste laboratório, horizonte e gap são contados em datas observadas. Em produção, disponibilidade é um timestamp e pode exigir uma purga por tempo de calendário ou por evento.

## Exemplo explicado
Com 100 datas, reserve 80 a 99 para o teste. A primeira janela de desenvolvimento treina até uma fronteira anterior à sua validação, deixando ao menos uma data de intervalo. As probabilidades fora do treino escolhem C e limiar; rótulos do teste não entram nessa escolha.

## Experimente
Abra Validação temporal. Compare gap 1 e 3, leia cada fronteira e implemente ex09_janelas sem chamar TimeSeriesSplit. Rode o teste que altera só os rótulos finais e mantém a escolha.

## Resultado esperado
Nenhuma data entra em treino e validação da mesma janela; nenhuma validação toca o teste final. Mudar os rótulos finais pode alterar o custo reportado, mas não C, limiar nem ranking de validação.

## Erros comuns
Aplicar TimeSeriesSplit diretamente a linhas de um dia; ajustar gap depois de olhar o teste; confundir a média das janelas com uma prova de estabilidade em toda população. Features também precisam respeitar o instante de disponibilidade.

## Desafio
Simule datas ausentes e explique a diferença entre três datas observadas e três dias de calendário. Implemente purga por disponível_em em um caso próprio.

## Critério de conclusão
Entregue diagrama ou tabela das janelas, exercício aprovado e teste de invariância da seleção ao futuro.

## Referências
- [scikit-learn 1.8: seleção temporal e calibração](https://scikit-learn.org/1.8/modules/calibration.html)
- Databricks ML in Action; material fornecido, não redistribuído.
