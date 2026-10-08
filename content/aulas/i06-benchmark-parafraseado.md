+++
id = "i06-benchmark-parafraseado"
title = "Meça a busca com perguntas de gente de verdade"
track = "ia-recuperacao"
level = "Intermediário"
version = "2.1"
prerequisites = ["i02-busca", "i04-avaliacao"]
sources = ["llm-guia", "oficial"]
objectives = ["Construir um benchmark que não copia o texto das aulas", "Medir recall@k e MRR", "Entender o custo de se abster de responder"]
lab = "IA e recuperação; exercício 07"
+++

# Meça a busca com perguntas de gente de verdade

## Problema

Seu sistema de busca acerta 100% do benchmark. Na primeira semana de uso, as pessoas reclamam que ele não acha nada. As seis perguntas do teste repetiam palavras das aulas; as pessoas escrevem com outras palavras. O benchmark media a memória do índice, não a utilidade.

## Conceito

A busca lexical (TF-IDF) compara palavras. Se a pergunta diz "faturamento" e a aula diz "receita", não há ponto de contato. Por isso um benchmark honesto precisa de **paráfrases**: perguntas escritas como alguém que ainda não leu o material.

Duas medidas resumem a qualidade:

- **recall@k**: em que fração das perguntas o documento esperado aparece entre os k primeiros.
- **MRR**: média de 1/posição do documento esperado. Acertar em primeiro vale 1; em terceiro, 1/3; fora do top-k, 0. Premia quem coloca o certo no topo.

Há uma terceira pergunta que quase ninguém mede: **e quando não existe resposta?** TF-IDF devolve algo sempre que houver uma palavra em comum, até em perguntas como "receita de bolo". Para se abster, é preciso um **limiar mínimo de similaridade**, e esse limiar tem custo: quanto mais alto, mais respostas certas, mas com poucas palavras em comum, também são descartadas.

## Exemplo explicado

O laboratório tem três conjuntos: seis perguntas copiadas das aulas, 30 perguntas parafraseadas e seis perguntas fora do escopo. Com as perguntas copiadas, o recall@3 é 100%. Com as parafraseadas, o recall@1 cai para perto de metade e o recall@3 fica na casa dos 70% a 80%. Nas perguntas fora do escopo, sem limiar, a busca nunca se abstém. Subir o limiar faz a abstenção aparecer, mas derruba o recall das perguntas legítimas, porque as similaridades TF-IDF dessas perguntas curtas já são baixas.

## Experimente

Abra **IA e recuperação** e use "Avalie a recuperação". Mova o limiar mínimo e observe as duas métricas juntas. Depois escreva cinco perguntas suas, sem copiar termos das aulas, e veja onde a busca erra. Faça o **exercício 07** (`exercicios/ex07_recuperacao.py`) para calcular recall e MRR por conta própria.

## Resultado esperado

Uma tabela com recall@1, recall@3 e MRR para os dois conjuntos de perguntas, o gráfico mental (ou real) do trade-off entre abstenção e recall, e uma lista de pelo menos três falhas explicadas por vocabulário diferente.

## Erros comuns

Escrever perguntas depois de ler a resposta. Ajustar o índice até acertar o benchmark e continuar chamando de "teste". Usar um limiar sem medir o que se perde. Concluir que busca semântica resolve tudo sem medir no mesmo benchmark.

## Desafio

Proponha uma melhoria (sinônimos, reescrita da pergunta, busca semântica) e meça-a no mesmo conjunto de 30 paráfrases, antes e depois, sem editar as perguntas.

## Critério de conclusão

Você mostra a melhoria com recall@k, MRR e taxa de abstenção medidos no mesmo benchmark congelado, e declara o que piorou.

## Referências

[scikit-learn: TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html). Perguntas, medidas e protocolo próprios do Lab Bricks.
