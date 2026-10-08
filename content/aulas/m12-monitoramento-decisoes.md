+++
id = "m12-monitoramento-decisoes"
title = "Drift com uma decisão verificável"
track = "machine-learning"
level = "Intermediário"
version = "3.0"
prerequisites = ["m05-drift", "m11-calibracao"]
sources = ["ml-acao-livro", "mit-relatorio"]
objectives = ["Executar a prática e explicar o resultado", "Identificar um erro e provar a correção"]
lab = "Calibração e decisão"
+++

# Drift com uma decisão verificável

## Problema
Um gráfico de drift ficou vermelho. Você deve investigar a fonte, esperar rótulos, treinar um candidato ou promover outro modelo?

## Conceito
PSI compara distribuições de entrada e depende dos intervalos escolhidos; ele não mede desempenho nem causalidade. Desempenho exige rótulos maduros e uma população comparável. O laboratório demonstra uma política didática: com menos de 80 rótulos, investigue e colete; se Brier piora pelo menos 0,02, treine um candidato e valide temporalmente; PSI pelo menos 0,2 isolado pede investigação. Esses limites são exemplos para estudar decisões, não recomendações universais de operação.

## Exemplo explicado
PSI=0,25 com Brier estável e 120 rótulos leva a investigar a distribuição. PSI=0,05 com Brier 0,12 para 0,17 leva a avaliar um candidato. Uma falha na regra de cálculo da feature pode exigir corrigir o pipeline em vez de retreinar.

## Experimente
Na página Calibração e decisão, mude PSI, Brier e número de rótulos. Escreva qual ação seria tomada, o responsável, o prazo e a evidência para encerrar o alerta.

## Resultado esperado
Toda condição aponta uma ação explicada. Nenhuma condição promove automaticamente um modelo. Acompanhamento de custo e grupos precisa fazer parte da revisão.

## Erros comuns
Usar PSI como prova de perda de qualidade; ignorar atraso dos rótulos; comparar períodos com populações diferentes; repetir treino até melhorar o teste antigo.

## Desafio
Acrescente uma mudança de composição por canal e compare desempenho global e por grupo. Especifique um plano de rollback e um teste futuro para o candidato.

## Critério de conclusão
Entregue uma pequena política com gatilho, suporte mínimo, ação, aprovação e registro de resultado.

## Referências
- Databricks ML in Action; material fornecido, não redistribuído.
- Relatório sobre adoção empresarial de IA, versão portuguesa fornecida; material fornecido, não redistribuído.
