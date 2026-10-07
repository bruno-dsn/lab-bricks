+++
id = "i03-rag"
title = "Planeje um RAG com citações e abstenção"
track = "ia-recuperacao"
level = "Intermediário"
version = "2.0"
prerequisites = ["i02-busca"]
sources = ["pesquisa-rag", "llm-guia", "mit-relatorio"]
objectives = ["Separar recuperação, geração e avaliação", "Definir como citar e quando não responder"]
lab = "IA e recuperação; roteiro sem chamadas externas"
+++

# Planeje um RAG com citações e abstenção

## Problema

Recuperar uma aula não garante que um gerador a use corretamente. O sistema precisa separar as evidências, as instruções da tarefa e a resposta, além de mostrar de onde veio cada afirmação.

## Conceito

RAG combina recuperação de contexto com geração condicionada. Uma arquitetura inclui ingestão e controle de acesso, divisão em trechos, índice, recuperação, montagem de contexto, geração e avaliação. Chunking muito pequeno perde contexto; muito grande ocupa a janela com material irrelevante. Preservar ID, título, versão e posição ajuda a auditar citações.

O laboratório executa a recuperação e apresenta um rascunho de instrução; a geração fica como extensão opcional e não é executada pelo app. Isso permite estudar o desenho sem assumir custo, credenciais ou acesso a serviços. Um RAG real deve respeitar permissões também no momento de recuperar, e não apenas na tela final.

## Exemplo explicado

O rascunho diz: use somente as evidências fornecidas, cite o ID da aula para afirmações factuais e informe quando o contexto for insuficiente. Cada trecho é um dado citado. Uma instrução dentro de um trecho não deve substituir a tarefa nem conceder privilégios.

## Experimente

Pergunte sobre MERGE e confira se a evidência contém a regra de chave e versão. Depois pergunte um valor ausente, como orçamento real da empresa. Escreva como seria uma resposta com abstenção. Se futuramente conectar um modelo, mantenha conjunto de testes congelado e não salve chaves em código ou progresso.

## Resultado esperado

Você produz uma resposta manual sustentada por trechos e uma recusa por ausência de evidência. Não há no app uma alegação de que o rascunho de prompt foi executado por um LLM.

## Erros comuns

Confundir citar um documento com sustentar a afirmação; colocar todos os livros no contexto; deixar o gerador escolher qualquer URL; filtrar acesso só depois de buscar.

## Desafio

Desenhe um RAG para notas pessoais. Defina metadados, revogação de acesso, atualização do índice, exclusão de documentos e como detectar citação inventada.

## Critério de conclusão

Sua arquitetura separa recuperação e geração, preserva versões e inclui uma política explícita de abstenção.

## Referências

Fontes: guia e relatório fornecidos; [RAG, Lewis et al., 2020](https://arxiv.org/abs/2005.11401).
