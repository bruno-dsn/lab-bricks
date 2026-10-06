# Exercícios com critérios de conclusão

Resolva primeiro e depois consulte [SOLUCOES.md](SOLUCOES.md). Alterar uma consulta ou uma regra é parte do exercício. Mantenha uma entrada pequena para provar o comportamento antes de usar a amostra completa.

## 1. Receita por canal

Escreva uma consulta sobre `silver_vendas` que devolva receita e pedidos por canal, apenas para concluídos. A soma das receitas deve coincidir com a receita total de concluídos. Faça o mesmo para unidades por produto.

**Concluído quando:** você explica por que contar pedidos e somar unidades são operações diferentes.

## 2. Taxa de cancelamento

Conte cancelados e divida pelo total de pedidos válidos. Mostre o resultado em porcentagem com duas casas decimais. Não limite o denominador aos pedidos concluídos.

**Concluído quando:** a taxa fica entre 0% e 100% e você consegue explicar o universo da métrica.

## 3. Um canal que a loja não conhece

Acrescente uma linha com `canal = 'Desconhecido'`. O contrato atual exige um canal preenchido; esse registro ainda é válido. Implemente uma regra adicional de canais permitidos e um teste que mostre a nova rejeição.

**Concluído quando:** a quarentena explica a nova falha, a soma dos destinos continua igual à Bronze e pedidos dos três canais originais permanecem válidos.

## 4. Uma correção chegou atrasada

No notebook 03, faça a atualização do lote ser anterior à versão existente. Execute o MERGE. Depois execute o lote recente duas vezes.

**Concluído quando:** a versão antiga não vence e repetir o lote recente não muda a tabela após a primeira execução.

## 5. Preço inválido numa versão nova

Crie duas versões de um pedido. A mais antiga é válida; a recente tem preço negativo. Execute o pipeline local.

**Concluído quando:** a recente vai para a quarentena, a antiga fica entre as versões substituídas e nenhuma vira a versão vigente na Silver.

## 6. Um teste temporal

Compare períodos de teste de 7, 14 e 21 dias. Mantenha as features sem informação do próprio dia previsto. Registre MAE da baseline e do Ridge em cada janela.

**Concluído quando:** o relatório informa os períodos e distingue previsão de um passo de previsão de vários passos.

## 7. Uma entrega sua

Escolha uma melhoria: agregação por categoria, monitor de rejeições ou validação adicional. Escreva o problema, implemente e acrescente uma imagem gerada pela sua execução. Informe se você testou localmente ou também na conta Databricks.

**Concluído quando:** outra pessoa consegue reproduzir o resultado seguindo seu README, e você consegue apontar uma limitação concreta.
