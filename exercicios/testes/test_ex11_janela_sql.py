import pandas as pd
from ex11_janela_sql import consulta_acumulado
from lab.sql_seguro import consultar_tabelas

def run(rows):return consultar_tabelas({'vendas':pd.DataFrame(rows,columns=['dia','valor_centavos'])},consulta_acumulado())[0]
def test_grupo_diario_antes_de_acumular():
    r=run([('2026-01-01',700),('2026-01-01',500),('2026-01-02',800)]);assert r.acumulado_centavos.tolist()==[1200,2000]
def test_colunas_e_ordem():
    r=run([('2026-01-02',2),('2026-01-01',1)]);assert list(r)==['dia','receita_centavos','acumulado_centavos'] and r.dia.tolist()==['2026-01-01','2026-01-02']
def test_valores_iguais_nao_sao_descartados():
    r=run([('2026-01-01',500),('2026-01-01',500)]);assert r.receita_centavos.tolist()==[1000]
