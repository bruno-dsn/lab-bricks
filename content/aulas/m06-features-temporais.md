+++
id = "m06-features-temporais"
title = "Recupere a feature que já existia na previsão"
track = "machine-learning"
level = "Avançado"
version = "2.0"
prerequisites = ["m02-temporal", "e03-incremental"]
sources = ["ml-acao-livro", "oficial"]
objectives = ["Distinguir evento ocorrido de informação disponível", "Testar junções point-in-time sem trazer o futuro"]
lab = "ML e ciclo completo; notebook 11"
+++

# Recupere a feature que já existia na previsão

## Problema

Um histórico de clientes foi corrigido às 12h. Ao reconstruir uma previsão feita às 10h, um JOIN com a tabela atual traz a correção. O modelo parece conhecer algo que só chegaria depois. O split temporal sozinho não resolve esse vazamento.

## Conceito

Uma feature precisa de entidade, valor e instante de disponibilidade. O tempo do evento responde quando algo ocorreu; o tempo de disponibilidade responde quando o sistema poderia usar essa informação. Um evento das 9h publicado às 12h não pode participar de uma previsão das 10h.

Uma junção point-in-time escolhe, para cada entidade e previsão, a versão mais recente disponível até aquele instante. Não havendo versão anterior, o resultado fica ausente. Preservar o pedido e tratar essa ausência explicitamente evita selecionar somente clientes com histórico. Se houver limite de idade, declare-o: histórico disponível também pode ser velho demais.

Feature Engineering em Unity Catalog possui recursos de lookup temporal. A configuração exige uma coluna temporal corretamente declarada e `timestamp_lookup_key` no lookup. Confira a API instalada: a documentação de conceitos e as versões da biblioteca podem apresentar nomes de parâmetros diferentes. O app usa Pandas para ensinar a regra, sem simular uma Feature Store implantada.

## Exemplo explicado

A cliente A tem risco 0,2 disponível desde ontem e correção para 0,8 disponível hoje às 12h. P1, previsto às 10h, recebe 0,2. P2, previsto às 13h, recebe 0,8. O cliente B não tem histórico e recebe valor ausente. A função `juntar_no_instante` preserva três pedidos, rejeita versões ambíguas e usa `merge_asof` na direção backward.

## Experimente

Abra ML e ciclo completo. Mova a disponibilidade da correção de 12h para 14h: P2 volta a usar 0,2. Depois mova para 10h: a informação está disponível exatamente no instante de P1 e pode ser usada. Execute o notebook 11 e compare a tabela resultante.

## Resultado esperado

No cenário padrão, os riscos de P1/P2/B são 0,2/0,8/ausente. Nenhum timestamp escolhido é maior que o timestamp da previsão. As três linhas permanecem presentes.

## Erros comuns

Juntar apenas por cliente; confiar na data do evento sem medir atraso de ingestão; preencher ausências com a versão atual; manter duas correções no mesmo instante sem desempate; tratar ausência de feature como ausência de pedido.

## Desafio

Acrescente um cliente com histórico de trinta dias e desenhe uma política de idade máxima de sete dias. Explique se você rejeita a inferência, usa um fallback ou sinaliza ausência. Implemente essa política como extensão antes de afirmar que ela existe.

## Critério de conclusão

Você demonstra um evento publicado tarde, uma igualdade de instantes, um cliente sem histórico e uma chave ambígua, justificando cada resultado sem usar dados futuros.

## Referências

Referência conceitual: Databricks ML in Action, capítulo 5. [Point-in-time feature joins](https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series) e [API FeatureEngineeringClient](https://api-docs.databricks.com/python/feature-engineering/latest/feature_engineering.client.html). Exemplo e código próprios.
