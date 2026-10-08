+++
id = "m11-calibracao"
title = "Probabilidades que significam o que dizem"
track = "machine-learning"
level = "Intermediário"
version = "3.0"
prerequisites = ["m10-validacao-temporal", "m09-instabilidade-selecao"]
sources = ["sklearn", "ml-livro"]
objectives = ["Executar a prática e explicar o resultado", "Identificar um erro e provar a correção"]
lab = "Calibração e decisão e ex10_calibracao"
+++

# Probabilidades que significam o que dizem

## Problema
Seu modelo diz 80% de risco, mas só metade dessas entregas atrasa. Ranking bom não garante que os números representem frequências confiáveis.

## Conceito
Calibração compara probabilidade prevista com frequência observada. A curva de confiabilidade agrupa previsões em intervalos e mostra também o número de exemplos por intervalo. ECE pondera desvios absolutos por suporte; depende dos intervalos e pode esconder erros locais. Brier mede erro quadrático da probabilidade e combina aspectos de calibração e discriminação. Um calibrador sigmoid transforma o score do modelo, mas precisa de um bloco próprio de dados posterior ao treino. Não prometa melhoria: compare resultados e incerteza.

## Exemplo explicado
Separe datas em treino 50%, calibração 10%, validação 20% e teste 20%, com purga do horizonte nas três fronteiras. FrozenEstimator mantém o estimador base já treinado enquanto CalibratedClassifierCV ajusta só o calibrador. Escolha o limiar empírico na validação para cada modelo. O teórico é 5/(5+30)=0,143 quando custos e probabilidades calibradas descrevem a decisão; não é uma constante universal.

## Experimente
Abra Calibração e decisão e compare curva, suporte, Brier e custo no mesmo teste. Faça ex10_calibracao à mão, incluindo p=1 no último intervalo.

## Resultado esperado
Base e sigmoid usam a mesma população final e limiares definidos sem seus rótulos. O app mostra o limiar teórico e o empírico e permite ver quando a calibração piora.

## Erros comuns
Ajustar calibrador no teste; usar o mesmo bloco para calibrar e escolher limiar; comparar ECE com intervalos diferentes; concluir que um gráfico próximo da diagonal prova calibração perfeita com poucos exemplos.

## Desafio
Varia número de intervalos e tamanho do bloco de calibração. Registre quais conclusões mudam e quais permanecem.

## Critério de conclusão
Entregue curva com suporte, exercício aprovado e uma recomendação limitada pelos dados observados.

## Referências
- [scikit-learn 1.8: seleção temporal e calibração](https://scikit-learn.org/1.8/modules/calibration.html)
- Practical Machine Learning on Databricks; material fornecido, não redistribuído.
