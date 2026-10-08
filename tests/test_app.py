from pathlib import Path
from streamlit.testing.v1 import AppTest
from lab.paginas_escola import PAGINAS


APP = Path(__file__).resolve().parents[1] / "app.py"


def test_paginas_principais_abrem_sem_excecao():
    app = AppTest.from_file(str(APP)).run(timeout=30)
    assert not app.exception
    for name in PAGINAS + ["Trilha e progresso", "Biblioteca de aulas", "Pipeline e qualidade", "Laboratório SQL", "BI e modelagem", "Ingestão incremental", "Previsão de vendas", "ML e classificação", "ML e ciclo completo", "Estabilidade da escolha", "IA e recuperação", "Teste seu raciocínio", "Exercícios", "Adicionar conteúdo"]:
        app.radio(key="page").set_value(name).run(timeout=30)
        assert not app.exception, name


def test_editor_exibe_resultado_e_bloqueia_escrita():
    app = AppTest.from_file(str(APP)).run(timeout=30)
    app.radio(key="page").set_value("Laboratório SQL").run(timeout=30)
    app.button[0].click().run(timeout=30)
    assert not app.exception and len(app.success) == 1
    app.text_area[0].set_value("DROP TABLE silver_vendas")
    app.button[0].click().run(timeout=30)
    assert not app.exception and len(app.warning) == 1


def test_ciclo_ml_exibe_rejeicao_de_contrato():
    app = AppTest.from_file(str(APP)).run(timeout=30)
    app.radio(key="page").set_value("ML e ciclo completo").run(timeout=30)
    app.selectbox[0].set_value("Vazamento: duração real").run(timeout=30)
    assert not app.exception
    assert any("Entrada rejeitada" in item.value for item in app.warning)


def test_missao_sql_corrige_uma_solucao_escrita():
    app=AppTest.from_file(str(APP)).run(timeout=30)
    app.radio(key="page").set_value("Missões SQL").run(timeout=30)
    app.text_area[0].set_value("SELECT p.pedido_id,COALESCE(SUM(i.valor_centavos),0) AS receita_centavos FROM pedidos p LEFT JOIN itens i ON p.pedido_id=i.pedido_id GROUP BY p.pedido_id ORDER BY p.pedido_id")
    app.button[0].click().run(timeout=30)
    assert not app.exception and len(app.success)==1


def test_escola_guarda_reflexao_na_sessao():
    app=AppTest.from_file(str(APP)).run(timeout=30)
    app.radio(key="page").set_value("Minha escola").run(timeout=30)
    app.text_area[0].set_value("Aprendi a preservar o grão.")
    app.button[0].click().run(timeout=30)
    assert not app.exception
    assert app.session_state["caderno"]["reflexoes"]["f01-mapa"]["texto"]=="Aprendi a preservar o grão."


def test_rag_extrativo_e_exercicio_final_abrem():
    app=AppTest.from_file(str(APP)).run(timeout=30)
    app.radio(key="page").set_value("RAG com evidências").run(timeout=30)
    app.button[0].click().run(timeout=30)
    assert not app.exception and len(app.text)>0
    app.radio(key="page").set_value("Exercícios").run(timeout=30)
    app.selectbox[0].set_value("ex14_citacoes").run(timeout=30)
    assert not app.exception
