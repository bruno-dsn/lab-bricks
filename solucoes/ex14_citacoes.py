"""Referência de contrato; suporte factual exige revisão além do JSON."""


def validar_citacoes(resposta,ids_contexto):
    if not isinstance(resposta,dict) or set(resposta)!={'resposta','citacoes','absteve'} or not isinstance(resposta['resposta'],str) or not 1<=len(resposta['resposta'])<=3000 or type(resposta['absteve']) is not bool or not isinstance(resposta['citacoes'],list) or not all(isinstance(x,str) for x in resposta['citacoes']):
        raise ValueError('Formato inválido.')
    citations=resposta['citacoes']
    if len(citations)>5 or len(set(citations))!=len(citations) or set(citations)-set(ids_contexto):
        raise ValueError('Citações inválidas.')
    if resposta['absteve']:
        if citations:raise ValueError('Abstenção contraditória.')
        return {'resposta':'Evidência insuficiente para responder.','citacoes':[],'absteve':True}
    if not citations:raise ValueError('Resposta sem evidência.')
    return resposta
