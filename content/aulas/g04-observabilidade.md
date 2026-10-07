+++
id = "g04-observabilidade"
title = "Observe qualidade, atualização e custo juntos"
track = "governanca"
level = "Avançado"
version = "2.0"
prerequisites = ["g03-entrega", "s05-desempenho"]
sources = ["engenharia-livro", "mit-relatorio", "oficial"]
objectives = ["Definir SLI e ação para uma falha", "Separar tempo de execução e frescor do dado"]
lab = "Notebook 07; guia de operação"
+++

# Observe qualidade, atualização e custo juntos

## Problema

O Job terminou com sucesso, mas o painel ainda usa o arquivo da semana passada. Um estado verde da infraestrutura não prova que a informação está atualizada e correta.

## Conceito

Observe infraestrutura, dados e consumo. Infraestrutura: duração, falhas, retries e compute. Dados: atraso da fonte, volume, nulidade, duplicidade e reconciliação. Consumo: atualização do painel, erro de query e aderência da métrica. Um SLI é uma medida; um SLO define objetivo e janela. Escolha objetivos compatíveis com o uso.

Custos também precisam de contexto: tempo de compute, warehouse, armazenamento, chamadas externas e revisão humana. A Free Edition é um ambiente de aprendizagem com limites, não uma estimativa de custo de produção. Um incidente exige dono, diagnóstico, ação e registro; um alerta sem destinatário vira ruído.

## Exemplo explicado

Para uma fonte diária, um SLI possível é “horas desde o último lote válido”. Outro é “diferença absoluta de receita entre Gold e Silver em centavos”. A segunda deve ser zero no laboratório. O primeiro exige metadados reais de lote: a data fictícia do pedido não é o timestamp da última ingestão.

## Experimente

Crie uma ficha com indicador, fonte de medida, frequência, objetivo, severidade e ação. Inclua um cenário de ausência de lote e um de excesso de rejeitados. Rode o gate 07 e registre uma evidência sem expor linhas privadas. Planeje como investigar sem apagar checkpoint.

## Resultado esperado

A ficha permite distinguir dado atrasado, contrato quebrado e falha de infraestrutura. Você não usa a data fixa da fonte sintética como medida de disponibilidade real.

## Erros comuns

Alertar todo desvio com mesma severidade; medir frescor pelo horário do dashboard; ignorar custo de revisão; publicar log com segredo ou conteúdo sensível.

## Desafio

Escreva um runbook de cinco passos para “receita Gold não reconcilia”. Inclua preservação de evidência, escopo e condição para liberar consumidores.

## Critério de conclusão

Cada sinal tem interpretação, responsável e uma ação segura e reproduzível.

## Referências

Fontes: engenharia e relatório empresarial; [monitoramento de Jobs](https://docs.databricks.com/aws/en/jobs/monitor).
