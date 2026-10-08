+++
id = "i07-busca-semantica"
title = "Embeddings locais no mesmo benchmark"
track = "ia-recuperacao"
level = "Intermediário"
version = "3.0"
prerequisites = ["i06-benchmark-parafraseado"]
sources = ["semantica", "pesquisa-rag"]
objectives = ["Executar a prática e explicar o resultado", "Identificar um erro e provar a correção"]
lab = "IA e recuperação e scripts/evaluate_search.py"
+++

# Embeddings locais no mesmo benchmark

## Problema
Você quer substituir busca lexical por embeddings. Sem medir a mesma tarefa, um nome mais avançado pode esconder uma regressão.

## Conceito
Embeddings representam texto em vetores e aproximam formulações diferentes. O modelo multilingual MiniLM roda localmente em ONNX, sem enviar perguntas a APIs. Esta receita divide aulas em trechos de 850 caracteres, sobrepõe 120, inclui o título, limita a 128 tokens, faz média com máscara e normaliza o vetor. A busca usa cosseno e remove documentos repetidos no ranking. Compare com TF-IDF usando o corpus original de 35 aulas congelado antes das dez aulas novas: novas explicações não podem virar treino invisível para as perguntas de avaliação.

## Exemplo explicado
Recall@1 e recall@3 verificam o documento esperado; MRR@5 valoriza posições iniciais. Cobertura mede a fração de perguntas respondidas acima do limiar, e precisão coberta mede quantas dessas respostas têm o documento correto no primeiro lugar. Abstenção fora do escopo usa seis perguntas separadas. Os limiares 0,12 lexical e 0,45 semântico foram fixados antes da medição e não são probabilidades calibradas.

## Experimente
Leia content/search_results.json e compare os rankings pergunta por pergunta. Opcionalmente instale requirements-semantica.txt junto do lock, baixe o modelo por script e execute uma pergunta nova. O cache do benchmark não implementa busca livre: perguntas inéditas exigem inferência do encoder.

## Resultado esperado
As 30 paráfrases e seis perguntas fora do escopo permanecem idênticas às da 2.1. O relatório mostra ganhos e perdas; chunking diferente impede atribuir toda diferença somente ao encoder.

## Erros comuns
Editar perguntas depois de ver falhas; tratar cosseno como confiança; comparar recall com limiares e coberturas diferentes sem declarar; dizer que embeddings sempre vencem.

## Desafio
Congele novas perguntas independentes antes de experimentar outro chunking. Faça uma ablação que mantenha os mesmos trechos para as duas buscas.

## Critério de conclusão
Entregue tabela de métricas, três falhas explicadas e protocolo com hashes que permita reproduzir a medição.

## Referências
- [paraphrase-multilingual-MiniLM-L12-v2 em ONNX](https://huggingface.co/Xenova/paraphrase-multilingual-MiniLM-L12-v2)
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
