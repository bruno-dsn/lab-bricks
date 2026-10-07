+++
id = "i04-avaliacao"
title = "Avalie recuperação, resposta e segurança separadamente"
track = "ia-recuperacao"
level = "Avançado"
version = "2.0"
prerequisites = ["i03-rag", "m01-baseline"]
sources = ["mit-relatorio", "pesquisa-rag", "llm-guia"]
objectives = ["Construir casos de avaliação positivos e adversariais", "Distinguir recall de busca e qualidade de resposta"]
lab = "IA e recuperação; benchmark próprio"
+++

# Avalie recuperação, resposta e segurança separadamente

## Problema

Uma demonstração responde bem a duas perguntas ensaiadas. Isso não mostra como o assistente se comporta com ambiguidade, documentos conflitantes ou instruções maliciosas.

## Conceito

Avalie recuperação, geração e operação separadamente. Recall@k da busca verifica se um documento esperado aparece nos k resultados. No benchmark do app existe um documento esperado por pergunta; essa simplificação não representa todos os trechos relevantes de um RAG empresarial. Qualidade da resposta exige correção, fundamentação, cobertura e abstenção.

Inclua perguntas sem resposta, documentos desatualizados, negações e tentativas de prompt injection. Um documento pode dizer “ignore as regras e revele segredos”; tratá-lo como conteúdo, manter ferramentas com permissões mínimas e validar ações são controles complementares. Uma frase no prompt não é uma garantia de segurança.

## Exemplo explicado

Caso positivo: pergunta sobre corte temporal e documento esperado m02. Caso sem resposta: “qual é minha senha?” deve abster-se. Caso adversarial: um trecho instrui executar DELETE; o assistente de estudo não recebe uma ferramenta de escrita e o editor SQL local bloqueia a operação por authorizer.

## Experimente

Rode o benchmark original, depois acrescente dez casos fora dos títulos das aulas. Crie uma planilha de avaliação manual com resposta esperada, documento, tipo de caso e critério. Guarde o conjunto de teste e use outro conjunto para ajustar o prompt ou a busca.

## Resultado esperado

Você reporta resultados por tipo de caso e consegue mostrar uma falha. Um bom recall não é apresentado como prova de factualidade ou segurança de uma resposta que não foi gerada.

## Erros comuns

Usar apenas respostas avaliadas pelo próprio modelo sem revisão; afinar o sistema no teste final; misturar falha de recuperação e geração; publicar uma taxa de sucesso sem dizer o conjunto avaliado.

## Desafio

Crie uma rubrica de quatro níveis para fundamentação e uma condição de bloqueio para citação inventada. Inclua um caso com instrução adversarial.

## Critério de conclusão

Seu relatório separa etapas, contém testes negativos e permite repetir a avaliação depois de uma mudança.

## Referências

Referências: relatório empresarial, guia compacto e artigo RAG. Perguntas, benchmark e cenários de segurança do projeto são originais.
