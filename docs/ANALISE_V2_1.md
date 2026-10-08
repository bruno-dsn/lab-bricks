# Revisão técnica da versão 2.1

A 2.1 trouxe correções úteis: one-hot do dia da semana, três baselines, cache, sete exercícios, benchmark parafraseado e análise de instabilidade. A versão recebida passou no verificador e em 120 testes antes das mudanças. Esses itens foram preservados.

## Revisão de cada recomendação

| Tema | Entrega 3.0 | Limite |
|---|---|---|
| Construir do zero | 14 exercícios, 64 testes de aluno e três missões SQL | Solução aprovada não prova autonomia sem explicação |
| Databricks real | 17 notebooks e registro de execução | Conta não executada |
| Baselines e dia da semana | Correções da 2.1 preservadas | Cenário de previsão continua sintético |
| Seleção instável | 30 sementes, margem, limiar e bootstrap | Não é intervalo de uma população real |
| Busca honesta | Mesmo conjunto congelado, lexical e encoder local | Encoder perdeu; chunking não foi isolado |
| Dados públicos | Online Retail, 3.000 linhas sem defeitos artificiais | Um dia de dados, sem previsão real |
| Validação temporal | Janelas por data com gap e teste final separado | Horizonte em datas observadas precisa ser interpretado |
| Calibração | Fit/calibração/validação/teste separados | Calibrar não garante melhor resultado |
| RAG | Extrativo e sete casos de geração local medidos | Todos os contratos do gerador falharam |
| CDC e streaming | SCD2, replay, atrasos e cenários Spark | Simulação limitada; Delta cloud pendente |
| Portfólio | Modelo de relato e gráficos de resultados | Relato pessoal deve ser escrito pelo estudante |

## Correções além da expansão

O teste de manutenção dos exercícios gera esqueletos temporários a partir das interfaces de referência. Não altera os arquivos que o aluno resolveu. Assim, estudar e preencher TODOs não quebra a verificação da distribuição.

A validação reforça a coerência dos módulos copiados nos novos notebooks, as 45 aulas do percurso e o benchmark congelado. Cache de vetores usa NPZ sem pickle, dimensões e checksum verificados. JSON de caderno e feedback tem limite e contrato.

No caso público, normalização monetária usa Decimal, registra motivo de rejeição e preserva moeda/fuso desconhecido. Duplicatas equivalentes em representação de preço são normalizadas. Identificador de origem vazio é inválido.

A resposta extrativa aceita até cinco evidências de entrada e retorna no máximo três trechos para respeitar o orçamento de texto. Citações precisam existir no contexto; isso não demonstra suporte factual.

## Diagnóstico que permanece

Executar serviços nativos é a principal lacuna. O caso público melhora a engenharia, mas não transforma ML sintético em evidência real. A busca semântica e o pequeno gerador perderam ou falharam; trocar modelo só vale depois de congelar outro experimento e medir os mesmos critérios. O próximo ganho deve vir de executar, explicar e revisar esses casos, não de aumentar contagens.
