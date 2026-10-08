"""Referência: partição reconciliada; o normalizador é fornecido pelo laboratório."""
import pandas as pd
from lab.retail_real import COLUNAS, SILVER, _normalizar


def particionar(bronze):
    if list(bronze.columns) != COLUNAS or bronze.linha_fonte.isna().any() or bronze.linha_fonte.astype(str).str.strip().eq('').any() or bronze.linha_fonte.duplicated().any():
        raise ValueError('Contrato de origem inválido.')
    good, rejected, replaced, seen = [], [], [], set()
    for row in bronze.to_dict('records'):
        try:
            normalized = _normalizar(row)
        except ValueError as error:
            rejected.append({**row,'motivo':str(error)});continue
        key = tuple(str(normalized[c]) for c in COLUNAS if c != 'linha_fonte')
        if key in seen:
            replaced.append({**row,'motivo':'linha_identica'})
        else:
            seen.add(key);good.append(normalized)
    return (pd.DataFrame(good,columns=SILVER),pd.DataFrame(rejected,columns=COLUNAS+['motivo']),pd.DataFrame(replaced,columns=COLUNAS+['motivo']))
