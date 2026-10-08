+++
id = "e07-cdc-scd2"
title = "CDC e SCD tipo 2: preserve a história"
track = "engenharia"
level = "Intermediário"
version = "3.0"
prerequisites = ["e03-incremental"]
sources = ["engenharia-livro", "oficial"]
objectives = ["Executar a prática e explicar o resultado", "Identificar um erro e provar a correção"]
lab = "CDC e histórico e notebook 14"
+++

# CDC e SCD tipo 2: preserve a história

## Problema
O cliente mudou de região. Atualizar a linha atual faz vendas antigas parecerem realizadas na região nova. Você precisa saber qual versão valia no instante de cada fato.

## Conceito
CDC é um log de alterações; SCD tipo 2 guarda versões com início inclusivo e fim exclusivo. Um upsert com valor novo fecha a versão anterior e abre a próxima. Repetir o mesmo ID e conteúdo é replay; repetir ID com conteúdo divergente é conflito. Uma alteração sem mudança de valor não precisa abrir uma versão. Delete fecha a vigente; uma reinserção posterior abre novo intervalo. A referência Pandas reconstrói o histórico a partir do log completo ordenado e rejeita duas alterações da mesma chave no mesmo instante.

## Exemplo explicado
Região A em 1/jan e B em 3/jan geram intervalos [1,3) e [3,infinito). Uma venda em 3/jan pertence a B. Uma alteração atrasada em 2/jan obriga reconstruir os intervalos afetados; não basta sobrescrever a vigente.

## Experimente
Abra CDC e histórico. Inclua delete e replay e confira o audit. Faça ex12_merge, que pratica a versão corrente idempotente. O notebook 14 tem uma opção de MERGE Delta sobre snapshot completo em tabela de estudo dedicada; a execução em conta real precisa ser registrada.

## Resultado esperado
Nenhuma chave tem duas versões atuais e os intervalos não se sobrepõem. O replay preserva o estado; conflitos são explícitos. Na referência local, evento atrasado é tratado pela reconstrução do log completo.

## Erros comuns
Usar só atualizado_em como desempate quando a ordem é ambígua; tratar SCD2 como um MERGE simples de versão corrente; perder deletes no snapshot; generalizar a referência de 1.000 eventos como solução distribuída.

## Desafio
Faça uma junção temporal de três vendas com o histórico e prove a inclusão na fronteira. Defina o que muda quando o log completo não cabe mais em memória.

## Critério de conclusão
Entregue histórico, audit de replay/conflito, junção temporal e explicação dos limites do snapshot.

## Referências
- Databricks Certified Data Engineer Associate Study Guide; material fornecido, não redistribuído.
- [Documentação oficial atual do Databricks](https://docs.databricks.com/aws/en/)
