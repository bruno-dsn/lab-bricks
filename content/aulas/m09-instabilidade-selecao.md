+++
id = "m09-instabilidade-selecao"
title = "Meça o quanto a sua escolha de modelo balança"
track = "machine-learning"
level = "Avançado"
version = "2.1"
prerequisites = ["m07-selecao-validacao"]
sources = ["ml-livro", "oficial"]
objectives = ["Repetir um protocolo de seleção em várias amostras", "Separar ganho real de vitória por acaso", "Derivar o limiar a partir dos custos"]
lab = "Estabilidade da escolha; exercício 06; módulo lab.estabilidade"
+++

# Meça o quanto a sua escolha de modelo balança

## Problema

O ciclo da aula m07 escolheu "logística com C = 1 e limiar 0,15". Você publica a decisão. Alguém gera outra amostra do mesmo problema, roda o mesmo código e o vencedor passa a ser "C = 0,1 e limiar 0,25". Qual das duas escolhas estava certa? Talvez nenhuma: com poucos dados, a validação mede ruído junto com desempenho.

## Conceito

Uma seleção é um **estimador**: como qualquer estimador, tem variância. Você não observa essa variância rodando o protocolo uma vez; precisa repeti-lo em amostras diferentes e olhar a distribuição das escolhas.

Três perguntas ajudam a ler o resultado.

1. **O ganho sobre uma política trivial é estável?** Compare o custo da política escolhida com "nunca alertar" (custo de todos os atrasos) e "sempre alertar" (custo de todos os falsos alarmes). Um intervalo de confiança por bootstrap mostra se o ganho médio é distinguível de zero.
2. **A diferença entre candidatos é maior que o ruído?** Se o segundo colocado fica a poucos reais do primeiro na validação, a ordem entre eles não é informação.
3. **O limiar combina com a teoria?** Se as probabilidades são razoavelmente calibradas, alertar compensa quando `p × custo_fn ≥ (1 − p) × custo_fp`, ou seja, `p ≥ custo_fp / (custo_fp + custo_fn)`. Com R$ 5 e R$ 30, o corte teórico é 5/35 ≈ 0,143. O limiar empírico deve orbitar esse valor; ficar longe dele é um sinal para investigar calibração.

## Exemplo explicado

O laboratório gera 30 conjuntos sintéticos (sementes 0 a 29, 600 entregas cada) e roda `avaliar_ciclo` em cada um. Dois candidatos logísticos, C = 0,1 e C = 1, disputam a escolha e dividem as vitórias de forma parecida: nenhum domina. Os limiares escolhidos ficam em torno de 0,15, perto do valor teórico, mas variam de 0,10 a 0,30. Ao mesmo tempo, a política escolhida custa bem menos que "nunca alertar" em todas as amostras, e o intervalo bootstrap de 95% para o ganho médio fica longe de zero.

A leitura honesta combina as duas coisas: **o modelo vale a pena; a escolha fina entre C = 0,1 e C = 1 não é um achado**.

## Experimente

Abra **Estabilidade da escolha** e use o controle de amostras. Observe a barra de vencedores, a faixa de limiares e o intervalo do ganho. Depois rode, em Python, `repetir_selecao(30)` e `resumir(...)` de `lab.estabilidade`. Faça o **exercício 06** (`exercicios/ex06_limiar.py`): implemente o limiar teórico e o empírico e compare.

## Resultado esperado

Você descreve, em poucas frases, o que mudou entre amostras (vencedor e limiar) e o que não mudou (ganho sobre "nunca alertar" e limiar mediano próximo de 0,14). Também explica por que a margem de validação pequena entre candidatos não autoriza escolher um deles como "o melhor".

## Erros comuns

Anunciar o vencedor de uma única execução. Comparar o modelo só com ele mesmo em vez de uma política trivial. Trocar a semente até o resultado agradar. Tratar o limiar do teste como se tivesse sido planejado. Confundir "o ganho é estável" com "a escolha do hiperparâmetro é estável".

## Desafio

Aumente o custo de falso negativo para R$ 100, recalcule o limiar teórico e verifique se a mediana empírica o acompanha. Depois reduza o histórico para 360 entregas e documente o que acontece com a variação dos limiares.

## Critério de conclusão

Você entrega um parágrafo com (a) a distribuição das escolhas, (b) o intervalo de confiança do ganho sobre a política trivial, (c) o limiar teórico comparado ao empírico e (d) uma recomendação que não dependa de uma diferença menor que o ruído.

## Referências

Conceito de variância de estimadores e bootstrap: [scikit-learn, validação cruzada](https://scikit-learn.org/stable/modules/cross_validation.html). Protocolo, dados sintéticos e custos próprios do Lab Bricks.
