+++
id = "m03-classificacao"
title = "Escolha o limiar pelo custo da decisão"
track = "machine-learning"
level = "Intermediário"
version = "2.0"
prerequisites = ["m02-temporal"]
sources = ["ml-livro", "mit-relatorio"]
objectives = ["Interpretar precision, recall e matriz de confusão", "Comparar probabilidade e decisão binária"]
lab = "ML e classificação; notebook 09"
+++

# Escolha o limiar pelo custo da decisão

## Problema

A equipe pode contactar clientes com risco de atraso. Alertas desnecessários custam tempo; deixar passar um atraso custa mais. Um limiar de 0,5 não é uma obrigação estatística nem comercial.

## Conceito

Um classificador produz probabilidades ou scores; um limiar transforma score em ação. Precision é a fração de alertas corretos. Recall é a fração de atrasos encontrados. Falsos positivos alertam sem atraso; falsos negativos deixam um atraso sem alerta. F1 combina precision e recall, mas não incorpora automaticamente custos reais.

ROC AUC avalia ordenação ao longo de limiares; Brier mede o erro quadrático das probabilidades. São aspectos diferentes. Compare Brier com uma baseline que usa a prevalência do treino. Para escolher limiar sem contaminar o teste final, use validação intermediária; o slider do app serve para aprender, não para declarar uma otimização imparcial no mesmo teste.

## Exemplo explicado

O cenário ilustrativo atribui R$ 5 a cada falso positivo e R$ 30 a cada falso negativo: custo = 5 × FP + 30 × FN. Esses valores não vêm de uma pesquisa nem representam uma empresa real. O app mantém a mesma partição e varia somente o limiar.

## Experimente

Teste limiares 0,2, 0,5 e 0,8. Registre TP, FP, FN, TN, precision, recall e custo. Observe que AUC e Brier não mudam quando apenas o limiar muda. No notebook 09, leia o corte temporal e a baseline antes de interpretar os números.

## Resultado esperado

Ao elevar o limiar, o número de alertas não aumenta. A curva de custos pode favorecer outro limiar, mas a escolha precisa ser validada fora do teste final. O conjunto padrão contém 480 entregas de treino e 120 de teste.

## Erros comuns

Maximizar accuracy em um alvo raro; tratar probabilidade como certeza; escolher limiar no teste e reportar desempenho sem ressalva; dividir por zero quando não há alertas.

## Desafio

Crie treino, validação e teste temporais. Escolha o limiar na validação e congele antes de abrir o teste. Documente custo por tipo de erro.

## Critério de conclusão

Você explica a matriz de confusão e escolhe uma política de alerta com custo e protocolo explícitos.

## Referências

Fontes: ML e relatório empresarial; [métricas scikit-learn](https://scikit-learn.org/stable/modules/model_evaluation.html).
