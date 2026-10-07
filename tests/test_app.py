from pathlib import Path
from streamlit.testing.v1 import AppTest


APP = Path(__file__).resolve().parents[1] / "app.py"


def test_paginas_principais_abrem_sem_excecao():
    app = AppTest.from_file(str(APP)).run(timeout=30)
    assert not app.exception
    for name in ["Trilha e progresso", "Biblioteca de aulas", "Pipeline e qualidade", "Laboratório SQL", "BI e modelagem", "Ingestão incremental", "Previsão de vendas", "ML e classificação", "ML e ciclo completo", "IA e recuperação", "Teste seu raciocínio", "Adicionar conteúdo"]:
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
