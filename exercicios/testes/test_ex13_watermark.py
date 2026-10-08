from ex13_watermark import aceitar_lote

def event(identifier,time):return {'evento_id':identifier,'instante':f'2026-01-01T{time}:00Z','valor':1}
def test_fronteira_anterior_inclusiva():
    a,r,_=aceitar_lote([event('a','10:10'),event('b','10:11')],'2026-01-01T10:10:00Z',set());assert [e['evento_id'] for e in a]==['b'] and r[0]['resultado']=='atrasado'
def test_futuro_no_mesmo_lote_nao_muda_fronteira():
    a,_,_=aceitar_lote([event('a','10:30'),event('b','10:11')],'2026-01-01T10:10:00Z',set());assert len(a)==2
def test_ids_existentes_e_no_mesmo_lote():
    known={'x'};a,r,new=aceitar_lote([event('x','10:20'),event('a','10:20'),event('a','10:20')],None,known);assert len(a)==1 and [e['resultado'] for e in r]==['duplicado','aceito','duplicado'] and known=={'x'} and new=={'x','a'}
