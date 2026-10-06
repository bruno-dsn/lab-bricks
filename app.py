from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from lab.dados import gerar_vendas
from lab.pipeline import tratar, indicadores
from lab.sql_seguro import consultar, ConsultaInvalida
from lab.ml import comparar

st.set_page_config(page_title="Databricks na prática", page_icon="🧱", layout="wide")
st.markdown("""<style>
.block-container { max-width: 1220px; padding-top: 2rem; }
h1 { letter-spacing: -0.04em; }
[data-testid="stMetric"] { background: #14263a; border: 1px solid #294157;
border-radius: 14px; padding: 18px; }
[data-testid="stSidebar"] { border-right: 1px solid #294157; }
</style>""", unsafe_allow_html=True)  # CSS fixo; nenhuma entrada do usuário.

with st.sidebar:
    st.markdown("### 🧱 Databricks\nna prática")
    st.caption("UM LABORATÓRIO PARA ENTENDER FAZENDO")
    page = st.radio("Sua próxima experiência", ["Visão geral", "Pipeline e qualidade", "Laboratório SQL", "Previsão de vendas", "Teste seu raciocínio"], key="page")
    st.divider()
    n = st.slider("Pedidos fictícios", 360, 2000, 720, 40)
    seed = st.number_input("Semente dos dados", 0, 1000, 42)
    dirty = st.toggle("Incluir erros na fonte", True)
    st.caption("O app roda localmente com Pandas e SQLite. Os notebooks da pasta notebooks executam Spark e Delta no Databricks.")

try:
    result = tratar(gerar_vendas(int(n), bool(dirty), int(seed)))
except ValueError:
    st.error("As opções de geração dos dados são inválidas.")
    st.stop()

def money(value):
    return "R$ " + f"{value:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")

def metrics(frame):
    values = indicadores(frame)
    cols = st.columns(3)
    cols[0].metric("Receita de pedidos concluídos", money(values["receita"]))
    cols[1].metric("Pedidos concluídos", f"{values['pedidos']:,}".replace(",", "."))
    cols[2].metric("Ticket médio por pedido", money(values["ticket_medio"]))

if page == "Visão geral":
    st.caption("APRENDA • EXPERIMENTE • EXPLIQUE")
    st.title("O caminho do dado\naté uma decisão.")
    st.write("Uma loja precisa saber quanto vendeu. Você recebe a fonte, encontra os erros, constrói tabelas confiáveis e testa suas próprias consultas.")
    st.info("Todos os pedidos são fictícios. Neste caso, cada pedido tem um único produto; pedidos cancelados não entram na receita.")
    metrics(result.silver)
    st.subheader("Receita por dia")
    st.line_chart(result.gold.set_index("data_venda")[["receita"]], color="#ff795d")
    cards = st.columns(3)
    cards[0].markdown("#### 01 · Receber\nBronze preserva os registros recebidos, inclusive os erros.")
    cards[1].markdown("#### 02 · Conferir\nSilver escolhe a versão mais recente e aplica regras de qualidade.")
    cards[2].markdown("#### 03 · Responder\nGold resume a receita e os pedidos por dia.")
    st.subheader("Investigue um canal")
    canais = st.multiselect("Canais", sorted(result.silver["canal"].unique()), default=sorted(result.silver["canal"].unique()))
    filtered = result.silver.loc[result.silver["canal"].isin(canais)]
    metrics(filtered)
    st.dataframe(filtered.head(15), hide_index=True, width="stretch")

elif page == "Pipeline e qualidade":
    st.title("Um número só merece confiança\nquando você conhece a fonte.")
    st.write("Compare a origem com o resultado. Desative os erros na barra lateral e observe a contagem mudar.")
    cols = st.columns(4)
    for col, label, value in zip(cols, ["Recebidos", "Versões substituídas", "Rejeitados", "Pedidos na Silver"], [len(result.bronze), len(result.substituidas), len(result.rejeitadas), len(result.silver)]):
        col.metric(label, value)
    st.caption("Recebidos = versões substituídas + rejeitados + pedidos na Silver. A Silver inclui concluídos e cancelados.")
    stage = st.segmented_control("Qual tabela você quer inspecionar?", ["Bronze", "Rejeitados", "Substituídos", "Silver", "Gold"], default="Rejeitados")
    frames = {"Bronze": result.bronze, "Rejeitados": result.rejeitadas, "Substituídos": result.substituidas, "Silver": result.silver, "Gold": result.gold}
    frame = frames.get(stage, result.bronze)
    st.dataframe(frame.head(200), hide_index=True, width="stretch")
    st.caption("Exibição limitada aos primeiros 200 registros.")
    with st.expander("Por que não apagar simplesmente os erros?"):
        st.write("A quarentena conserva o motivo da rejeição para investigar e corrigir a fonte. Uma versão antiga do mesmo pedido fica em Substituídos. Se a versão mais recente for inválida, o pedido é rejeitado; uma versão antiga não volta silenciosamente para a Silver.")
    st.download_button("Baixar amostra sintética desta etapa", frame.to_csv(index=False).encode("utf-8"), file_name="amostra_sintetica.csv", mime="text/csv")

elif page == "Laboratório SQL":
    st.title("Faça uma pergunta.\nVeja a consulta responder.")
    st.write("Edite o SQL e rode sobre a mesma Silver do pipeline. Este editor usa SQLite; os notebooks ensinam Spark SQL.")
    presets = {
        "Receita por canal": "SELECT canal, ROUND(SUM(valor_centavos) / 100.0, 2) AS receita\nFROM silver_vendas\nWHERE status = 'concluida'\nGROUP BY canal\nORDER BY receita DESC;",
        "Produtos mais vendidos": "SELECT produto, SUM(quantidade) AS unidades\nFROM silver_vendas\nWHERE status = 'concluida'\nGROUP BY produto\nORDER BY unidades DESC;",
        "Pedidos cancelados": "SELECT venda_id, data_venda, canal, status\nFROM silver_vendas\nWHERE status = 'cancelada'\nLIMIT 20;",
    }
    preset = st.selectbox("Comece por um exemplo", list(presets), key="preset")
    with st.form("sql_form"):
        query = st.text_area("Sua consulta", presets[preset], height=185, max_chars=6000, key=f"query_{preset}")
        run = st.form_submit_button("Executar consulta", type="primary")
    if run:
        try:
            data, truncated = consultar(result.silver, query)
            st.success(f"{len(data)} linhas retornadas.")
            st.dataframe(data, hide_index=True, width="stretch")
            if truncated:
                st.info("Resultado limitado a 200 linhas. Refine os filtros para investigar outra parte dos dados.")
        except ConsultaInvalida as e:
            st.warning(str(e))
    with st.expander("Colunas disponíveis"):
        st.code(", ".join(result.silver.columns), language="text")
    st.caption("Dica: inclua WHERE status = 'concluida' ao calcular receita. valor_centavos guarda o total do pedido em centavos.")

elif page == "Previsão de vendas":
    st.title("Uma previsão precisa\nde uma comparação justa.")
    st.write("A baseline repete a receita de ontem. O modelo Ridge usa somente informações disponíveis antes do dia previsto.")
    days = st.slider("Dias finais reservados para teste", 7, 21, 14)
    try:
        comparison, info = comparar(result.gold, int(days))
        cols = st.columns(2)
        cols[0].metric("Erro médio absoluto · baseline", money(info["mae_baseline"]))
        cols[1].metric("Erro médio absoluto · modelo", money(info["mae_modelo"]))
        st.line_chart(comparison, color=["#f2eee8", "#54c4b8", "#ff795d"])
        st.caption(f"Treino: {info['treino_inicio']} a {info['treino_fim']}. Teste: {info['teste_inicio']} a {info['teste_fim']}.")
        st.info("Avaliação de um dia à frente: em cada dia de teste, as vendas dos dias anteriores já são conhecidas. Este gráfico não representa uma previsão de várias semanas feita de uma só vez.")
        with st.expander("Como evitar usar o futuro sem perceber"):
            st.code("df['lag_1'] = receita.shift(1)\ndf['media_7'] = receita.shift(1).rolling(7).mean()", language="python")
            st.write("O shift vem antes da média: a receita do próprio dia previsto fica fora das features. O scaler é ajustado somente no conjunto de treino. Se o modelo perder para a baseline, registre esse resultado também.")
    except ValueError:
        st.warning("A amostra precisa de mais dias válidos para comparar os modelos.")

else:
    st.title("Você consegue explicar\na escolha que fez?")
    questions = [
        ("Um pedido foi cancelado. Onde ele deve ficar?", ["Na Silver, fora da receita de concluídos", "Apagado de todas as camadas", "Contado como receita"], 0, "Cancelamento é um status válido. Preservar o pedido permite analisar cancelamentos sem inflar a receita."),
        ("Chegaram duas versões do mesmo pedido. Qual fica na Silver?", ["A primeira que apareceu", "A versão com atualização mais recente", "As duas"], 1, "O horário de atualização define a versão vigente; a ordem da fonte desempata. O MERGE precisa de uma única versão por chave."),
        ("Para prever a receita de hoje, qual média pode ser usada?", ["A média incluindo hoje", "A média de amanhã", "A média dos sete dias até ontem"], 2, "Uma informação só pode entrar no modelo se estiver disponível no momento da previsão."),
    ]
    for i, (question, options, answer, explanation) in enumerate(questions):
        st.subheader(f"{i+1}. {question}")
        selected = st.radio("Escolha uma resposta", options, index=None, key=f"answer_{i}", label_visibility="collapsed")
        if st.button("Conferir raciocínio", key=f"check_{i}"):
            if selected is None:
                st.info("Escolha uma resposta primeiro.")
            elif selected == options[answer]:
                st.success(explanation)
            else:
                st.warning("Releia a regra e tente de novo. " + explanation)

st.divider()
st.caption("Databricks na prática · projeto educacional independente · dados sintéticos · versão 1.0")
