+++
id = "f06-estudo-com-evidencias"
title = "Estudar, escrever, errar e demonstrar"
track = "fundamentos"
level = "Intermediário"
version = "3.0"
prerequisites = ["f05-reprodutibilidade"]
sources = ["ebook-original"]
objectives = ["Executar a prática e explicar o resultado", "Identificar um erro e provar a correção"]
lab = "Minha escola e scripts/corrigir.py"
+++

# Estudar, escrever, errar e demonstrar

## Problema
Você entende uma solução pronta, mas trava quando precisa escrever a primeira linha. Ler produz reconhecimento; construir exige recuperar uma regra e decidir como aplicá-la.

## Conceito
Use quatro passos: tente sem consultar a solução, execute o teste, formule uma hipótese sobre a falha e altere uma coisa por vez. Um teste vermelho é uma observação sobre um contrato, não uma nota sobre sua inteligência. Antes de corrigir, escreva qual linha você esperava e qual recebeu. Depois de passar, mude um caso de entrada e explique por que a solução continua correta. Marcar uma aula no app é um registro pessoal; código, resultados e explicação são evidências mais fortes.

## Exemplo explicado
No ex01, calcule receita no grão de item e conte pedidos distintos. Se contar três itens como três pedidos, o teste revela uma diferença concreta. Registre no caderno: "confundi item com pedido; agora agrupo pelo identificador do pedido".

## Experimente
Abra Minha escola, faça uma etapa por vez e edite exercicios/ex01_grao.py no VS Code. Rode `python scripts/corrigir.py ex01_grao`. Importe o feedback em Minha escola e registre sua explicação. O relatório guarda o hash do código que foi testado.

## Resultado esperado
Um feedback aprovado contém testes passados, zero falhas e um hash SHA-256. Se mudar o código, rode o corretor de novo. O arquivo é editável e não funciona como certificado.

## Erros comuns
Consultar a solução antes de tentar; repetir testes sem formular hipótese; guardar só o print verde. A suíte principal usa cópias temporárias e não exige que seu exercício continue vazio.

## Desafio
Refaça o mesmo exercício amanhã sem olhar a implementação e acrescente um teste com pedido sem itens. Escreva por que uma média simples dos tickets de itens não responde ao ticket por pedido.

## Critério de conclusão
Entregue seu código, feedback e uma explicação curta do erro, da correção e da regra aprendida.

## Referências
- E-book introdutório original da conversa; material fornecido, não redistribuído.
