+++
id = "f04-contrato"
title = "Escreva um contrato que rejeita ambiguidade"
track = "fundamentos"
level = "Iniciante"
version = "2.0"
prerequisites = ["f03-python"]
sources = ["engenharia-livro", "mit-relatorio"]
objectives = ["Definir regras de validade e quarentena", "Reconhecer dados ausentes e empates de versão"]
lab = "Pipeline e qualidade"
+++

# Escreva um contrato que rejeita ambiguidade

## Problema

Um pedido chega sem valor e uma atualização traz um status desconhecido. Substituir tudo por zero ou descartar silenciosamente pode deixar o painel aparentemente limpo e semanticamente errado.

## Conceito

Um contrato descreve estrutura, tipos, campos obrigatórios, domínios permitidos, chaves e regra de versão. Neste laboratório, nulidade é normalizada para texto vazio antes da conversão; um valor vazio continua inválido. Uma linha inválida recebe motivo e vai para quarentena. Uma versão antiga válida não volta à Silver se a versão vigente é inválida.

Escolher a versão acontece antes da validação final. Assim, o sistema evidencia que a informação corrente do pedido está quebrada. Em produção, a ordem da fonte como desempate não é uma identidade durável: seria melhor receber um identificador de evento ou sequência oficial da origem.

## Exemplo explicado

O pipeline separa Bronze, versões substituídas, rejeitados, Silver e Gold. A igualdade `recebidos = substituídos + rejeitados + Silver` é uma reconciliação de linhas. Já a Gold agrega somente concluídos e exige uma verificação financeira em centavos. As duas verificações respondem perguntas diferentes.

## Experimente

Ative e desative erros da fonte. Inspecione os motivos de rejeição. Compare os registros de um mesmo `venda_id`. Abra os testes de pipeline e localize os casos de `None`, versão nova inválida e empate de timestamp. Depois formule uma nova regra de status antes de alterar qualquer código.

## Resultado esperado

Com dados padrão: 727 = 1 + 6 + 720. Sem erros, a Silver mantém 720 pedidos únicos. A versão nova inválida é evidenciada em rejeitados, em vez de ressuscitar uma versão antiga.

## Erros comuns

Tratar NULL, vazio e zero como equivalentes; validar só depois de publicar; usar `drop_duplicates` sem ordem de versão; aplicar um contrato sem explicar quem corrige o registro rejeitado.

## Desafio

Proponha como aceitar devoluções. Defina status, efeito na receita e tratamento de atualizações. Escreva exemplos válidos e inválidos antes de implementar.

## Critério de conclusão

Você produz um contrato com exemplos, reconcilia todas as linhas e indica o responsável pela correção na fonte.

## Referências

Referências conceituais: guia de engenharia e relatório empresarial de IA fornecidos. Código original: src/lab/pipeline.py e seus testes.
