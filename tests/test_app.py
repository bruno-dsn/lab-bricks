from pathlib import Path
from streamlit.testing.v1 import AppTest


APP = Path(__file__).resolve().parents[1] / "app.py"


def test_paginas_principais_abrem_sem_excecao():
    app = AppTest.from_file(str(APP)).run(timeout=30)
    assert not app.exception
    for name in ["Pipeline e qualidade", "Laboratório SQL", "Previsão de vendas", "Teste seu raciocínio"]:
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
