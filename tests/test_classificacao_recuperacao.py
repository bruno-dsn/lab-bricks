import numpy as np
import pytest
from lab.classificacao import avaliar_entregas, psi, FEATURES
from lab.recuperacao import buscar, recall_at_k

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
