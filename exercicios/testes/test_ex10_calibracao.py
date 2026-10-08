import pytest
from ex10_calibracao import ece_manual

def test_probabilidades_perfeitas_incluem_um():
    assert ece_manual([0,1],[0.,1.],2)==0
def test_ece_pondera_por_suporte():
    assert ece_manual([0,0,1],[.1,.2,.8],2)==pytest.approx((2*.15+.2)/3)
def test_grupo_com_calibracao_empirica():
    assert ece_manual([0,1],[.5,.5],2)==0
def test_vetor_invalido():
    with pytest.raises(ValueError):ece_manual([0],[float('nan')],2)
