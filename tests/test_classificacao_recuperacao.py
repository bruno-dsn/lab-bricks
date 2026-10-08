import numpy as np
import pytest
from lab.classificacao import avaliar_entregas, psi, FEATURES
import json
from pathlib import Path
from lab.conteudo import carregar
from lab.recuperacao import buscar, recall_at_k, mrr_at_k, taxa_de_abstencao

DOCS = [
    {'id': 'delta', 'title': 'Delta', 'text': 'MERGE atualiza pedidos por chave e versão. Repetir lotes exige idempotência.'},
    {'id': 'ml', 'title': 'ML', 'text': 'Vazamento temporal usa informação do futuro. Scaler aprende no treino.'},
]


def test_classificacao_temporal_baseline_e_limites_de_decisao():
    low, metrics_low, train = avaliar_entregas(threshold=.2)
    high, metrics_high, _ = avaliar_entregas(threshold=.8)
    assert train.data.max() < low.data.min()
    assert 'duracao_real_min' not in FEATURES
    assert metrics_low['treino'] == 480 and metrics_low['teste'] == 120
    assert low.alerta.sum() >= high.alerta.sum()
    assert metrics_low['brier'] == metrics_high['brier'] and metrics_low['auc'] == metrics_high['auc']
    assert sum(metrics_low[k] for k in ['tn', 'fp', 'fn', 'tp']) == 120
    assert metrics_low['custo_ilustrativo'] == 5 * metrics_low['fp'] + 30 * metrics_low['fn']
    assert np.isfinite(low.probabilidade).all()


def test_psi_mesma_distribuicao_e_constante_sao_finitos():
    reference = np.arange(100.)
    assert psi(reference, reference) == 0
    assert psi(reference, reference + 50) > 0
    assert psi([1, 1, 1], [2, 2, 2]) > 0


@pytest.mark.parametrize('reference,current', [([], [1]), ([1], []), ([float('nan')], [1]), ([[1]], [1])])
def test_psi_rejeita_vetores_invalidos(reference, current):
    with pytest.raises(ValueError):
        psi(reference, current)


def test_busca_rastreavel_e_abstencao_lexical():
    result = buscar('MERGE chave versão', DOCS, 2)
    assert result[0]['id'] == 'delta' and 0 < result[0]['score'] <= 1
    assert result[0]['trecho'] in DOCS[0]['text']
    assert buscar('qzxywvu', DOCS) == []
    score, _ = recall_at_k([{'query': 'vazamento temporal', 'expected': 'ml'}], DOCS, 1)
    assert score == 1


@pytest.mark.parametrize('query,k', [('', 3), ('x' * 501, 3), ('merge', 0), ('merge', 6)])
def test_busca_limita_entradas(query, k):
    with pytest.raises(ValueError):
        buscar(query, DOCS, k)


def test_mrr_e_abstencao_em_corpus_pequeno():
    cases = [{'query': 'vazamento temporal', 'expected': 'ml'}, {'query': 'idempotência lotes', 'expected': 'delta'}]
    assert mrr_at_k(cases, DOCS, 2) == 1
    assert mrr_at_k([{'query': 'zzz inexistente', 'expected': 'ml'}], DOCS, 2) == 0
    assert taxa_de_abstencao(['qzxywvu'], DOCS) == 1
    assert taxa_de_abstencao(['MERGE chave'], DOCS) == 0
    with pytest.raises(ValueError):
        taxa_de_abstencao(['x'], DOCS, 1.5)


def test_benchmarks_literal_e_parafraseado_mostram_a_limitacao_do_tfidf():
    root = Path(__file__).resolve().parents[1] / 'content'
    lessons, _, _ = carregar(root)
    docs = [{'id': a.id, 'title': a.titulo, 'text': a.corpo} for a in lessons]
    literal = json.loads((root / 'retrieval_benchmark.json').read_text())
    parafraseado = json.loads((root / 'retrieval_benchmark_parafraseado.json').read_text())
    fora = json.loads((root / 'retrieval_fora_do_escopo.json').read_text())
    assert len(parafraseado) >= 30 and len(fora) >= 5
    assert recall_at_k(literal, docs, 3)[0] == 1
    # A diferença é o ponto didático: se alguém "consertar" isso copiando palavras das aulas, este teste avisa.
    assert recall_at_k(parafraseado, docs, 1)[0] < recall_at_k(literal, docs, 1)[0] - .25
    assert 0 < recall_at_k(parafraseado, docs, 3)[0] < 1
    assert taxa_de_abstencao(fora, docs, 0) < .5 <= taxa_de_abstencao(fora, docs, .2)
