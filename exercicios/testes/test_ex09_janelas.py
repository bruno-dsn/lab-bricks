import pandas as pd
import pytest
from ex09_janelas import dividir_datas

DATES=pd.date_range('2026-01-01',periods=100)
def test_gap_e_fronteiras():
    windows,_,test=dividir_datas(DATES,gap=2)
    assert len(windows)==3
    for train,validation in windows:
        assert (validation[0]-train[-1]).days>=3 and set(validation).isdisjoint(test)
def test_datas_inteiras_e_repetidas():
    a=dividir_datas(DATES);b=dividir_datas(list(DATES)*3)
    assert a==b and len(a[2])==20
def test_refit_purga_antes_do_teste():
    _,refit,test=dividir_datas(DATES,gap=3);assert (test[0]-refit[-1]).days==4
def test_gap_menor_que_horizonte():
    with pytest.raises(ValueError):dividir_datas(DATES,gap=1,horizonte=2)
