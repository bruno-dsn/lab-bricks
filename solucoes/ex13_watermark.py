"""Referência: uma fronteira anterior explícita, sem avançá-la no próprio lote."""
import pandas as pd


def aceitar_lote(eventos,watermark,ids_conhecidos):
    known=set(ids_conhecidos);accepted=[];audit=[]
    frontier=pd.to_datetime(watermark,utc=True) if watermark is not None else None
    for event in eventos:
        instant=pd.to_datetime(event['instante'],utc=True,errors='raise')
        if pd.isna(instant):raise ValueError('Instante ausente.')
        if event['evento_id'] in known:status='duplicado'
        elif frontier is not None and instant<=frontier:status='atrasado'
        else:
            status='aceito';accepted.append(event.copy());known.add(event['evento_id'])
        audit.append({'evento_id':event['evento_id'],'resultado':status})
    return accepted,audit,known
