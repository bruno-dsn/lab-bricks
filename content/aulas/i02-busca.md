+++
id = "i02-busca"
title = "Recupere trechos com TF-IDF e meça limitações"
track = "ia-recuperacao"
level = "Intermediário"
version = "2.0"
prerequisites = ["i01-llms"]
sources = ["llm-guia", "pesquisa-rag"]
objectives = ["Distinguir busca lexical e embeddings", "Rastrear documento e trecho recuperados"]
lab = "IA e recuperação; notebook 10"
+++

# Recupere trechos com TF-IDF e meça limitações

## Problema

O assistente precisa localizar a aula sobre reprocessamento. Antes de gerar qualquer resposta, teste se o sistema encontra o documento certo para uma pergunta real.

## Conceito

TF-IDF representa termos com pesos que combinam frequência no documento e raridade no corpus. Similaridade de cosseno compara vetores. A busca do Lab Bricks usa palavras e pares de palavras, normalização de acentos e um corpus de aulas próprias. Isso favorece termos compartilhados, mas pode perder sinônimos e paráfrases.

Embeddings densos podem representar semelhanças sem depender do mesmo termo, mas exigem escolher modelo, avaliar domínio, versionar representação e cuidar de acesso aos documentos. O projeto não chama a busca TF-IDF de embedding semântico nem de resposta gerada por LLM. Score de similaridade não é probabilidade de uma resposta correta.

## Exemplo explicado

A pergunta “Como repetir um lote sem duplicar registros?” deve recuperar a aula de ingestão incremental. O resultado mostra ID, título, score e trecho. Uma pergunta sem termos presentes pode retornar nada. Ainda que exista algum overlap, o leitor precisa conferir se o trecho responde à pergunta.

## Experimente

Faça três perguntas com termos exatos e três paráfrases. Compare os resultados. Rode o benchmark original incluído no app e examine acertos por pergunta, não só a média. No notebook 10, o corpus pequeno de notas próprias permite investigar o mecanismo sem importar os livros.

## Resultado esperado

Você obtém evidências com IDs rastreáveis e identifica pelo menos uma limitação lexical. O resultado vazio é tratado como ausência de evidência, em vez de uma autorização para inventar uma resposta.

## Erros comuns

Interpretar score como confiança calibrada; avaliar somente perguntas escritas com o título do documento; recuperar documentos que o usuário não pode ler; usar corpus inteiro de livros protegidos no repositório.

## Desafio

Crie dez perguntas próprias com documento esperado, incluindo sinônimos e duas perguntas sem resposta. Explique como medir acerto e abstenção separadamente.

## Critério de conclusão

Seu conjunto de avaliação permite identificar falhas de recuperação e todos os trechos têm uma fonte verificável.

## Referências

Referências: guia compacto; [artigo RAG](https://arxiv.org/abs/2005.11401) e [TF-IDF scikit-learn](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction).
