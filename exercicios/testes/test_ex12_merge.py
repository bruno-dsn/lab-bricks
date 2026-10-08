import pandas as pd
import pytest
from ex12_merge import atualizar

def frame(rows):return pd.DataFrame(rows,columns=['id','versao','valor'])
def test_replay_idempotente():
    base=frame([(1,1,'A')]);lot=frame([(1,2,'B'),(2,1,'C')]);once=atualizar(base,lot);pd.testing.assert_frame_equal(once,atualizar(once,lot))
def test_chegada_antiga_nao_reverte():
    assert atualizar(frame([(1,3,'C')]),frame([(1,1,'A')])).valor.tolist()==['C']
def test_versao_igual_com_payload_divergente():
    with pytest.raises(ValueError):atualizar(frame([(1,1,'A')]),frame([(1,1,'B')]))
def test_entradas_preservadas_e_estado_vazio():
    b=frame([]);l=frame([(2,1,'B'),(1,1,'A')]);old=l.copy();r=atualizar(b,l);assert r.id.tolist()==[1,2];pd.testing.assert_frame_equal(l,old)
