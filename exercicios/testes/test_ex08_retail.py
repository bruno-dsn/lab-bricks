import pandas as pd
import pytest
from ex08_retail import particionar
from lab.retail_real import COLUNAS

def fonte(rows):
    base={'linha_fonte':'1','fatura':'100','produto':'A','descricao':'Caneca','quantidade':'2','data':'2010-12-01 08:00:00','preco_gbp':'1.235','pais':'United Kingdom'}
    return pd.DataFrame([{**base,**r} for r in rows],columns=COLUNAS)

def test_centavos_e_arredondamento():
    s,_,_=particionar(fonte([{}]));assert s.valor_centavos.tolist()==[248]
def test_quarentena_e_reconciliacao():
    data=fonte([{}, {'linha_fonte':'2','descricao':''}, {'linha_fonte':'3'}]);s,r,u=particionar(data)
    assert (len(s),len(r),len(u))==(1,1,1);assert len(data)==len(s)+len(r)+len(u);assert 'motivo' in r
def test_cancelamento_valido_e_sinal_inconsistente():
    s,r,_=particionar(fonte([{'fatura':'C100','quantidade':'-2'},{'linha_fonte':'2','quantidade':'-2'}]))
    assert s.valor_centavos.tolist()==[-248] and len(r)==1
def test_fatura_produto_nao_bastam_para_duplicata():
    s,_,u=particionar(fonte([{}, {'linha_fonte':'2','quantidade':'3'}]));assert len(s)==2 and u.empty
def test_origem_duplicada_e_invalida():
    with pytest.raises(ValueError):particionar(fonte([{},{}]))
