# Validar os notebooks na sua conta

**Estado desta entrega:** 54 testes do app e das regras locais passaram. A função `normalizar` do notebook 00 foi executada em Spark 4.0.1 local e reconciliada com Pandas em três cenários, incluindo campos nulos, ordem invertida da fonte e uma versão recente inválida. Os notebooks tiveram formato, sintaxe das células Python e saídas verificadas. A execução completa em uma conta Databricks, com Delta, Unity Catalog e MLflow, ainda não ocorreu. As caixas abaixo começam vazias por esse motivo.

Use uma conta e um catálogo de estudo. Registre data, tipo de compute, ambiente de bibliotecas e nome do catálogo sem publicar identidade pessoal ou credenciais.

- [ ] 00: importar os cinco `.py` na mesma pasta e escolher o catálogo em que pode criar o schema.
- [ ] 00: verificar o schema `dbnp_...`, derivado da identidade autenticada.
- [ ] 01: executar a consulta por canal e passar o teste de reconciliação.
- [ ] 02: obter Bronze 727, Silver 720, quarentena 6 e versões substituídas 1.
- [ ] 02: confirmar unicidade de `venda_id` na Silver e igualdade da receita em centavos com a Gold.
- [ ] 02: ler as tabelas pelo catálogo e criar a visualização de receita por dia.
- [ ] 03: executar o lote duas vezes, verificar igualdade do conteúdo e total de 721 pedidos.
- [ ] 03: consultar a versão anterior e recuperar os valores originais de V000001.
- [ ] 04: verificar 14 datas de teste, corte temporal e MAE de baseline e modelo.
- [ ] 04: opcionalmente habilitar MLflow e confirmar o experimento em sua pasta pessoal.
- [ ] Segurança: revisar permissões herdadas e testar uma segunda identidade quando o ambiente permitir.
- [ ] Exportação: remover saídas e revisar dados, caminhos e imagens antes de publicar no GitHub.

Um teste que passa em Pandas não comprova uma execução do Spark. Se houver divergência entre os motores, capture uma amostra fictícia mínima, registre a versão do ambiente e crie um teste para a regra envolvida.

## Repetir a verificação Spark local

Com Python 3.12 e Java 17 ou superior, instale `requirements-spark.txt` no ambiente virtual e execute `python scripts/verify_spark.py`. O script usa a função do notebook, sem copiar uma implementação alternativa. A fonte pequena entra por Arrow e a sessão Spark é encerrada ao terminar.

Essa verificação cobre a transformação. Não cria tabelas Delta, não executa o MERGE e não testa privilégios ou a criação do schema no Databricks. O workflow padrão do GitHub executa os 54 testes locais e a auditoria; a verificação Spark permanece opcional.

## Usar o CSV como exercício adicional

Envie `data/vendas_sinteticas.csv` a um volume de estudo pela interface. Confirme o caminho completo e as permissões do volume. Uma leitura com schema explícito deve manter os campos da origem como strings; acrescente uma ordem ou versão de ingestão apropriada antes da deduplicação.

Este caminho é opcional e não substitui os passos dos notebooks, que usam o gerador em memória. Uma posição arbitrária atribuída depois da leitura distribuída não é um desempate estável. Na ingestão real, prefira uma sequência produzida pela origem ou um identificador de evento.
