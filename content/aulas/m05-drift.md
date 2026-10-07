+++
id = "m05-drift"
title = "Monitore mudança sem confundi-la com falha"
track = "machine-learning"
level = "Avançado"
version = "2.0"
prerequisites = ["m04-mlops"]
sources = ["ml-livro", "mit-relatorio"]
objectives = ["Distinguir data drift e queda de desempenho", "Planejar investigação e retreinamento"]
lab = "ML e classificação"
+++

# Monitore mudança sem confundi-la com falha

## Problema

As entregas atuais passaram a percorrer distâncias maiores. A distribuição mudou, mas isso sozinho não prova que o modelo ficou pior. Para saber, precisamos observar rótulos e resultados no tempo.

## Conceito

Data drift é mudança na distribuição de entradas; concept drift envolve mudança na relação entre entradas e alvo. Monitorar drift pode antecipar investigação, mas qualidade preditiva exige rótulos posteriores e métricas com janelas adequadas. Atraso de rótulo pode deixar a qualidade recente parcialmente desconhecida.

O PSI do laboratório usa faixas definidas na referência e compara proporções. É um sinal exploratório sensível a bins, tamanho da amostra e regularização. Não usamos um limiar universal como prova de falha. Retreinar automaticamente por qualquer alteração pode propagar ruído; investigue fonte, contrato, população e resultados antes.

## Exemplo explicado

O slider desloca a distância do conjunto atual e calcula PSI contra o treino. O modelo e suas probabilidades do teste original permanecem iguais; o app não finge que gerou novos rótulos sob a mudança. Ele mostra uma mudança de entrada, não uma nova avaliação de qualidade.

## Experimente

Compare deslocamentos 0, 5 e 15 km. Observe PSI e histogramas. Escreva quais métricas de resultado precisariam ser acompanhadas quando os rótulos chegarem. Planeje um conjunto de comparação com baseline e aprovação antes de retreinar.

## Resultado esperado

PSI do mesmo vetor contra ele mesmo é zero. Uma mudança artificial pode produzir um indicador maior, mas não modifica automaticamente precision, recall ou Brier do teste já avaliado.

## Erros comuns

Chamar qualquer drift de concept drift; impor thresholds copiadas sem contexto; retreinar em dados com contrato quebrado; avaliar somente médias globais e ignorar regiões ou segmentos.

## Desafio

Crie uma política de monitoramento com frequência, janela, atraso de rótulo, segmentos, responsável e ação para cada tipo de alerta.

## Critério de conclusão

Você distingue alerta de distribuição, diagnóstico e decisão de retreinamento e informa quando faltam rótulos.

## Referências

Referências conceituais: ML e relatório empresarial fornecidos. O PSI e o cenário de distância são implementações didáticas originais do projeto.
