import pytest
from ex14_citacoes import validar_citacoes

def answer(citations,abstain=False):return {'resposta':'Texto de exemplo','citacoes':citations,'absteve':abstain}
def test_resposta_citada_e_abstencao():
    assert validar_citacoes(answer(['a']),['a'])['citacoes']==['a'];assert validar_citacoes(answer([],True),[])['resposta']=='Evidência insuficiente para responder.'
def test_id_inventado():
    with pytest.raises(ValueError):validar_citacoes(answer(['x']),['a'])
def test_citacao_repetida_ou_abstencao_contraditoria():
    with pytest.raises(ValueError):validar_citacoes(answer(['a','a']),['a'])
    with pytest.raises(ValueError):validar_citacoes(answer(['a'],True),['a'])
def test_sem_citacao_e_tipo_invalido():
    with pytest.raises(ValueError):validar_citacoes(answer([]),['a'])
    with pytest.raises(ValueError):validar_citacoes({**answer(['a']),'absteve':'false'},['a'])
