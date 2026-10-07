+++
id = "g02-jobs"
title = "Orquestre tarefas com dependências e contratos"
track = "governanca"
level = "Intermediário"
version = "2.0"
prerequisites = ["e03-incremental", "g01-acesso"]
sources = ["engenharia-livro", "ml-livro", "oficial"]
objectives = ["Definir DAG de tarefas e gate de qualidade", "Planejar retries e evidências de execução"]
lab = "resources/lab_bricks.job.yml; notebook 07"
+++

# Orquestre tarefas com dependências e contratos

## Problema

A Gold não pode ser atualizada se a qualidade da Silver falhou. Executar notebooks em ordem manual não oferece um registro claro de dependências, falhas e tentativas.

## Conceito

Lakeflow Jobs organiza tarefas, dependências, parâmetros e execuções. Um gate de qualidade interrompe tarefas consumidoras quando um contrato falha. Retries precisam de operações idempotentes: repetir uma escrita não deve duplicar dados. A identidade de execução deve ter somente os privilégios necessários.

O bundle de estudo tem três tarefas sequenciais: construir lakehouse, verificar qualidade e construir o caso BI. Não há agenda automática. O destino de desenvolvimento e limite de concorrência reduzem colisões, mas não tornam uma conta de produção um local adequado para treino. Free Edition possui limites que podem mudar; revise antes de executar.

## Exemplo explicado

O notebook 07 lê as tabelas produzidas pelo 02, confere 720 chaves, seis rejeitados, uma versão substituída e reconciliação Gold/Silver. Uma violação gera erro em vez de um painel verde. Contagens fixas aqui são do fixture padrão, não regras universais para toda fonte.

## Experimente

Leia a configuração YAML e o guia de Jobs. Valide o bundle com catálogo explicitamente escolhido. Depois de deploy manual autorizado na sua conta, execute e observe dependências. Registre run ID, duração e estado de cada tarefa. Para testar falha, use somente uma cópia de estudo.

## Resultado esperado

O gate passa para o fixture padrão e bloqueia o fluxo quando seu contrato é quebrado. O repositório oferece a configuração e os testes locais; execução e permissões reais de Jobs exigem evidência da sua conta.

## Erros comuns

Usar retries para esconder falha de contrato; liberar consumidores com “all done” sem intenção; agendar automaticamente ao importar o projeto; compartilhar schema entre execuções concorrentes.

## Desafio

Acrescente uma tarefa de notificação como proposta, sem enviar mensagens. Defina destinatário, condição, conteúdo sem dados sensíveis e autorização necessária.

## Critério de conclusão

Você explica o grafo, a identidade de execução, o gate e o comportamento de retry.

## Referências

Fonte: engenharia e ML; [quickstart de Jobs](https://docs.databricks.com/aws/en/jobs/jobs-quickstart).
