from pathlib import Path
import json
import pytest
from lab.conteudo import carregar, importar_progresso, exportar_progresso, modelo_aula

ROOT = Path(__file__).resolve().parents[1]


def test_catalogo_tem_fontes_requisitos_e_questoes_coerentes():
    lessons, tracks, sources = carregar(ROOT / 'content')
    assert len(lessons) >= 30 and len(tracks) == 6
    ids = {a.id for a in lessons}
    questions = json.loads((ROOT / 'content/questions.json').read_text())
    assert len({q['id'] for q in questions}) == len(questions) >= 36
    for q in questions:
        assert q['lesson'] in ids and q['track'] in tracks
        assert 0 <= q['answer'] < len(q['choices']) and q['explanation']
    assert {'bi-livro', 'engenharia-livro', 'ml-livro', 'llm-guia', 'mit-relatorio'} <= sources.keys()


def test_progresso_round_trip_nao_contem_identidade():
    ids = {'f01-mapa', 'f02-grao'}
    payload = exportar_progresso(ids, ids)
    assert importar_progresso(payload, ids) == ids
    assert set(json.loads(payload)) == {'format', 'version', 'completed'}


@pytest.mark.parametrize('payload', [b'{}', b'not json', b'[]', b'x' * 100001,
    b'{"format":"lab-bricks-progress","version":1,"completed":["desconhecida"]}',
    b'{"format":"lab-bricks-progress","version":true,"completed":[]}',
    b'{"format":"lab-bricks-progress","version":1,"completed":[4]}'])
def test_progresso_rejeita_entradas_fora_do_contrato(payload):
    with pytest.raises(ValueError):
        importar_progresso(payload, {'f01-mapa'})


def test_pre_requisito_circular_e_id_duplicado_falham(tmp_path):
    (tmp_path / 'aulas').mkdir()
    (tmp_path / 'tracks.json').write_text('{"fundamentos":{}}')
    (tmp_path / 'sources.json').write_text('{"oficial":{}}')
    text = modelo_aula('a01-teste', 'Teste', 'fundamentos').replace('prerequisites = []', 'prerequisites = ["a01-teste"]')
    (tmp_path / 'aulas/a.md').write_text(text)
    with pytest.raises(ValueError, match='Ciclo'):
        carregar(tmp_path)
    (tmp_path / 'aulas/a.md').write_text(modelo_aula('a01-teste', 'Teste', 'fundamentos'))
    (tmp_path / 'aulas/b.md').write_text(modelo_aula('a01-teste', 'Duplicado', 'fundamentos'))
    with pytest.raises(ValueError, match='duplicados'):
        carregar(tmp_path)


@pytest.mark.parametrize('identifier', ['../saida', 'a/b', 'UPPER', 'x', 'a`cmd'])
def test_template_rejeita_caminhos(identifier):
    with pytest.raises(ValueError):
        modelo_aula(identifier, 'Título', 'fundamentos')
