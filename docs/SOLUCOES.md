# Soluções orientadas e formas de conferir

Estas orientações ajudam a revisar decisões; não são um gabarito de exame nem substituem a evidência de execução.

## Projeto 01

Fixture padrão: 727 recebidos, 720 chaves válidas, seis rejeitados e uma versão substituída. Reconcilie linhas e receita em centavos. Reaplique um lote e compare conteúdo completo. Uma correção vigente inválida deve aparecer na quarentena, sem restaurar silenciosamente a versão antiga. O gate 07 se aplica ao snapshot do notebook 02; o MERGE 03 usa um destino independente com 721 chaves.

Para uma fonte real, contagens fixas não seriam universais: defina tolerâncias e metadados de lote com significado de negócio. Nome de schema não é controle de acesso.

## Projeto 02

180 pedidos, 16 cancelados e 164 concluídos. Após o JOIN com itens, conte pedidos com DISTINCT; unidades com SUM(quantidade). A montagem muitos-para-um deve recusar chave duplicada em dimensões. Use preço/custo da transação e reconcilie receita por categoria com total. O último acumulado diário deve corresponder ao total dos mesmos filtros. Margem bruta não é lucro líquido.

Os filtros do painel não alteram o editor SQL: replique-os no WHERE da query. No dashboard nativo, confira datasets e controles, além de permissões de publicação.

## Projeto 03

A previsão precisa de baseline e protocolo. O Ridge pode perder: isso não invalida uma avaliação honesta. A classificação padrão separa 480 entregas de treino e 120 de teste por datas. Duração real é vazamento e fica fora das features. Mudar limiar altera matriz/custo, sem alterar Brier/AUC das mesmas probabilidades. Para seleção final, use validação intermediária.

PSI é sinal de distribuição; novos rótulos seriam necessários para medir qualidade depois da mudança. A busca usa TF-IDF e retorna evidências. Recall de documentos não comprova resposta correta de um LLM: o app não executa geração. Um caso sem evidência deve levar a abstenção, não invenção.

## Como conferir seu domínio

Explique uma escolha, uma alternativa e uma limitação para cada entrega. Depois altere o fixture e demonstre que o contrato ainda vale ou que a falha é controlada. Uma screenshot verde sem contexto não comprova o resultado.
