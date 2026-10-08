# Como estudar na escola Lab Bricks

Seu objetivo é sair de cada etapa com algo que consegue construir e explicar. Reserve sessões de 45 a 90 minutos. O plano de 57 a 82 horas de aulas e práticas é uma estimativa; exercícios e projetos exigem tempo adicional.

## Um ciclo por aula

Leia o problema antes da solução. Escreva em uma frase o resultado esperado e o grão dos dados. Execute o exemplo, mude um caso de entrada e explique o resultado. Faça o desafio sem consultar a referência. Registre o erro encontrado, sua causa e uma evidência de correção. Revise a aula alguns dias depois usando uma entrada diferente.

Use três níveis pessoais: consigo reconhecer; consigo construir com consulta; consigo explicar e construir sozinho. A confiança informada no caderno não substitui a solução.

## Exercícios no VS Code

Cada arquivo de exercícios contém uma interface e uma tarefa. Implemente somente o que o enunciado pede. Os testes usam entradas variadas e contratos; não altere as verificações para aprovar sua solução.

```bash
python scripts/corrigir.py ex01_grao
python scripts/corrigir.py ex08_retail
```

O comando executa o arquivo correspondente localmente e salva feedback na pasta artifacts, ignorada pelo Git. Código Python do aluno só roda pelo comando local explícito. O app não oferece execução arbitrária de Python. Importe o JSON de feedback e exporte o caderno em Minha escola. O feedback guarda contagens e hash do código, sem enviar o código a serviços externos.

Quando falhar, leia o menor caso que reproduz o erro. Descreva o esperado e o obtido antes de editar. Depois, invente outro caso que possa quebrar sua abordagem. As soluções ficam em solucoes; use-as para comparar decisões após tentar.

## Percurso recomendado

1. **Comece pelo grão**: f01-mapa, f02-grao, f03-python, f04-contrato, f05-reprodutibilidade, f06-estudo-com-evidencias. Exercícios: ex01_grao.
2. **Escreva consultas**: s01-agregacoes, s02-joins, s03-janelas, s06-sql-missoes. Exercícios: ex02_join, ex11_janela_sql.
3. **Construa o pipeline**: e01-medallion, e02-delta, e03-incremental, e04-json-streaming, e05-declarativo. Exercícios: prática guiada.
4. **Investigue dados públicos**: e06-dados-reais, s04-dashboard, s05-desempenho. Exercícios: ex08_retail.
5. **Implemente fundamentos de ML**: m01-baseline, m02-temporal, m03-classificacao, m04-mlops. Exercícios: ex03_metricas, ex04_logistica, ex05_temporal.
6. **Preserve o futuro**: m06-features-temporais, m07-selecao-validacao, m08-contrato-inferencia, m10-validacao-temporal. Exercícios: ex09_janelas.
7. **Decida com incerteza**: m09-instabilidade-selecao, m11-calibracao, m05-drift, m12-monitoramento-decisoes. Exercícios: ex06_limiar, ex10_calibracao.
8. **Meça a recuperação**: i01-llms, i02-busca, i03-rag, i04-avaliacao, i06-benchmark-parafraseado, i07-busca-semantica. Exercícios: ex07_recuperacao.
9. **Avalie a resposta**: i05-valor, i08-rag-avaliado. Exercícios: ex14_citacoes.
10. **Opere e preserve a história**: g01-acesso, g02-jobs, g03-entrega, g04-observabilidade, g05-evolucao, e07-cdc-scd2, e08-watermark. Exercícios: ex12_merge, ex13_watermark.

As etapas do app incluem objetivos e evidências. As seis trilhas continuam disponíveis para revisão temática; os 10 passos organizam a sequência de prática.

## Três projetos

O projeto de lakehouse precisa reconciliar linhas e demonstrar reprocessamento. O projeto de BI precisa declarar população, grão, moeda e comportamento de JOINs. O projeto de ML/IA precisa preservar o teste final, comparar referências e registrar falhas de recuperação ou geração.

Você pode entregar a parte local primeiro. Etapas nativas sem execução ficam explicitamente pendentes. Use [o modelo de relato](ESTUDO_CASO_TEMPLATE.md) e as rubricas em content/projetos.

## Conteúdo novo e caderno pessoal

Exporte o caderno antes de fechar ou atualizar. Guarde suas soluções em um branch próprio. Adicione aulas com o gerador e revise metadados, fontes, questões, pré-requisitos e etapa. Rode o verificador. Atualize notebooks gerados quando alterar módulos compartilhados. O catálogo permite crescer sem transformar o README em uma lista de links sem sequência.

A escola foi concebida para estudo local individual. Publicar para vários usuários exige autenticação, isolamento e políticas de acesso revisadas no ambiente concreto.
