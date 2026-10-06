# Uma trilha com entregas pequenas

Avance quando conseguir explicar o resultado e resolver o desafio, no seu ritmo. As leituras complementam os notebooks; os exercícios usam a mesma loja fictícia para evitar trocar de contexto a cada aula.

| Sessão | Leia | Faça | Entregue |
|---|---|---|---|
| 1. Contexto | [Fundamentos](01_FUNDAMENTOS.md) | Abra o app e mude a fonte | Um desenho ligando fonte, tratamento e análise |
| 2. Perguntas | [SQL](02_SQL.md) | Execute o notebook 01 e edite consultas no app | Receita por canal, unidades por produto e taxa de cancelamento |
| 3. Confiança | [Pipeline](03_PIPELINE.md) | Execute o 02 e confira a quarentena | A reconciliação dos 727 registros e uma regra nova |
| 4. Novas versões | [Delta](04_DELTA.md) | Execute o 03 e repita o MERGE | Prova de que o lote entrou uma vez e um teste com versão antiga |
| 5. Previsão | [ML](05_MACHINE_LEARNING.md) | Execute o 04 ou use a tela de previsão | Comparação com baseline e explicação do corte temporal |
| 6. Compartilhar | [Governança](06_GOVERNANCA.md) | Revise saídas e siga a auditoria | Um README de portfólio com evidências e limites |

Depois de cada sessão, responda sem consultar o texto:

- Qual problema esta etapa resolve?
- Qual informação entra e qual resultado sai?
- Qual erro o teste procura?
- Qual mudança faria este exemplo precisar de outra regra?

Se uma resposta ficar vaga, volte ao registro específico que exemplifica a regra. No pipeline, uma data impossível esclarece a validação; duas versões de V000001 esclarecem a deduplicação.

## Como usar este trabalho no portfólio

Faça um fork ou crie seu repositório a partir do pacote. Mantenha a atribuição e acrescente uma seção **O que eu desenvolvi** com as suas alterações. Reproduzir a trilha é estudo; propor e validar uma regra nova é uma contribuição que você consegue demonstrar numa entrevista.

Uma entrega pequena pode incluir: questão de negócio, decisão de modelagem, consulta, resultado, teste e limitação. Evite afirmar que o exemplo processou milhões de registros ou rodou em produção: a amostra é pequena e fictícia.
