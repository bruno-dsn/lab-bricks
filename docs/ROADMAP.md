# Evoluir a trilha e preparar um produto

A versão 1.0 entrega um caso completo de estudo: consulta, tratamento, persistência em notebooks, atualização incremental e avaliação temporal. O app local permite inspecionar as regras. A próxima decisão deve partir do que as pessoas conseguem compreender e reproduzir.

## Melhorias do ensino

- Validar os notebooks numa conta de estudo e registrar a execução.
- Testar a leitura com iniciantes: observar onde param e que regra conseguem explicar depois.
- Acrescentar projetos originais em outros contextos, com fonte, contrato, perguntas e gabaritos próprios.
- Adicionar uma trilha de desempenho depois que houver dados e medições suficientes para discutir partições e shuffle.

## Melhorias de engenharia

- Ingestão de lotes identificados, sem substituir a Bronze inteira.
- Orquestração com dependências e testes entre ingestão, Silver e Gold.
- Monitoramento de rejeições, atraso da fonte e divergências de métricas.
- Testes de equivalência de regras entre Pandas e Spark numa conta autorizada.
- Empacotamento das transformações compartilhadas para reduzir cópias de código nos notebooks.

## Um futuro assistente de dados

Comece definindo quais perguntas pode responder e quais tabelas pode ler. Uma primeira extensão pode mapear perguntas a consultas fixas. Se houver LLM, teste respostas, custo, autorização e tentativas de acessar dados fora do escopo. Registre evidência junto da resposta.

Um assistente por regras não deve ser divulgado como agente com LLM. Nesta versão não há integração de modelo de linguagem nem credencial de serviço de IA.

## Antes de oferecer acesso comercial

Separe o material didático do serviço que armazena contas e atende usuários. Valide uma conta e um ambiente adequados ao uso comercial: a Free Edition é destinada a uso não comercial e não fornece SLA.

Implemente autenticação no servidor, autorização por recurso, proteção de sessão, isolamento entre clientes, limites de uso e operação de suporte. Revise publicação, tratamento de dados e cobrança conforme o produto escolhido. Reexecute o checklist da NotKode sobre essa implementação concreta.

Converse com usuários do material para escolher o formato: uma trilha orientada, exercícios avaliados ou projetos com acompanhamento podem ter necessidades diferentes. O repositório inicial não inclui pagamentos, cadastro, assinatura nem promessa de resultado profissional.
