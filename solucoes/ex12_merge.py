"""Referência de versão corrente: replay, chegada antiga e conflito."""
import pandas as pd


def atualizar(estado,lote):
    fields=['id','versao','valor'];current={}
    for frame in (estado,lote):
        if list(frame.columns)!=fields or len(frame)>1000:
            raise ValueError('Contrato de lote inválido.')
        for row in frame.to_dict('records'):
            if type(row['id']) is not int or row['id']<=0 or type(row['versao']) is not int or row['versao']<=0 or not isinstance(row['valor'],str):
                raise ValueError('Identificador ou versão inválidos.')
            old=current.get(row['id'])
            if old and old['versao']==row['versao'] and old['valor']!=row['valor']:
                raise ValueError('Conflito de versão.')
            if old is None or row['versao']>old['versao']:current[row['id']]=row.copy()
    return pd.DataFrame(sorted(current.values(),key=lambda r:r['id']),columns=fields)
