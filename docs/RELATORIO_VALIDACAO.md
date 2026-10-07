# Evidências da versão 2.0

**Data:** 7 de outubro de 2026. **Ambiente local:** Python 3.12, dependências do lock, PySpark 4.0.1 opcional.

| Verificação executada | Resultado | Limite |
|---|---|---|
| pytest | 105 testes aprovados | Funções locais e Streamlit AppTest |
| AppTest | 13 páginas sem exceção; editor lê e bloqueia escrita | Não simula toda infraestrutura de hospedagem |
| Verificador do projeto | Sintaxe, links locais, catálogo, pares, CSV e padrões de segredo aprovados | Busca limitada de segredo |
| Spark local | Cinco cenários: pipeline padrão/invertido/nulos, JSON e BI com janela | Sem Delta, UC ou serviços remotos |
| OSV | 54 pacotes consultados; nenhum advisory retornado | Base e momento da consulta |
| Notebook 11 · parte sem Tracking | Quatro células de código executadas localmente; asserts aprovados | Sem Feature Store, registry ou endpoint |
| Exportação notebooks | Doze pares sem saídas | Exportar não executa no Databricks |

A CI no GitHub repete a validação local e OSV. Seu estado final pode ser conferido na aba Actions do repositório. Não incluímos um estado de CI futuro como resultado prévio.

## Resultados de referência

- Primeiro caso: 727 Bronze = 720 Silver + seis rejeitados + uma versão substituída.
- BI: 180 pedidos totais, 164 concluídos; linhas de itens e unidades são grãos distintos. SQL/Pandas/Spark reconciliam métricas e última receita acumulada.
- JSON: quatro mensagens, duas rejeitadas, três itens válidos; receita dos itens = 17.600 centavos.
- Classificação: 480 entregas em treino e 120 em teste, sem sobreposição de datas; duração real excluída das features.
- Ciclo ML: 360/120/120 em treino/validação/teste; 51 políticas comparadas na validação; lookup temporal preserva ausência e contrato rejeita entradas incompatíveis.
- Progresso: round-trip JSON restrito sem identidade pessoal.

Confira [pendências de conta](VALIDACAO_DATABRICKS.md) e [segurança](AUDITORIA_SEGURANCA.md).
