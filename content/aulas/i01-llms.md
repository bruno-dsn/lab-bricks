+++
id = "i01-llms"
title = "Entenda o que um LLM faz e onde ele falha"
track = "ia-recuperacao"
level = "Intermediário"
version = "2.0"
prerequisites = ["f05-reprodutibilidade"]
sources = ["llm-guia", "pesquisa-transformer", "mit-relatorio"]
objectives = ["Distinguir tokens, contexto e fatos", "Escolher um uso com critérios de qualidade"]
lab = "IA e recuperação; leitura guiada"
+++

# Entenda o que um LLM faz e onde ele falha

## Problema

Você quer um assistente que responda perguntas do laboratório. Um modelo pode produzir uma frase convincente mesmo quando a informação não está disponível ou está incorreta. A fluência não é evidência.

## Conceito

Um modelo de linguagem aprende padrões para prever tokens. Tokens são unidades definidas pelo tokenizer; não equivalem sempre a palavras. Transformers usam mecanismos de atenção para relacionar posições do contexto. Esta aula explica o papel geral, sem prometer ensinar treinamento de um modelo de grande porte.

A janela de contexto limita o material que entra em uma chamada. Um modelo pode ter conhecimento desatualizado, responder com confiança a uma premissa falsa ou obedecer uma instrução indesejada presente em um documento. Temperatura altera amostragem em sistemas que a oferecem; reduzir temperatura não garante factualidade.

## Exemplo explicado

Pergunta: “Quantos pedidos válidos existem no cenário padrão?” Uma resposta verificável deve consultar o contrato e a contagem do pipeline. Uma resposta que inventa um número a partir de plausibilidade falha, mesmo que explique muito bem. Para essa pergunta, uma consulta estruturada pode ser superior a um LLM.

## Experimente

Classifique cinco tarefas: calcular receita, resumir uma aula, localizar referência, aprovar reembolso e executar SQL livre. Para cada uma, escolha regra determinística, busca ou assistência de linguagem e indique validação. No app, observe que IA e recuperação usa TF-IDF e não chama um LLM.

## Resultado esperado

Você distingue transformação determinística, recuperação e geração. O catálogo continua acessível sem API, chave, cobrança ou envio de dados a provedores.

## Erros comuns

Tratar um modelo como base de dados; prometer que temperatura zero elimina erro; copiar cronologias antigas de materiais promocionais; usar o mesmo controle para tarefas de baixo e alto impacto.

## Desafio

Defina uma tarefa adequada para um assistente de estudo e duas ações que exigem confirmação humana ou devem ser feitas por código determinístico.

## Critério de conclusão

Seu caso de uso tem entrada, saída, evidência e critério de falha, sem confundir texto plausível com verdade.

## Referências

Referências: guia compacto e relatório fornecidos; [Attention Is All You Need, 2017](https://arxiv.org/abs/1706.03762).
