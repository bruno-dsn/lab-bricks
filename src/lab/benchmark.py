"""Benchmark congelado: rankings semânticos por documento e cache sem pickle."""
from pathlib import Path
import hashlib, json
import numpy as np
from .recuperacao import buscar


def protocolo(directory):
    directory=Path(directory);protocol=json.loads((directory/'search_protocol.json').read_text())
    for name,sha in protocol['hashes'].items():
        if Path(name).name!=name or hashlib.sha256((directory/name).read_bytes()).hexdigest()!=sha:
            raise ValueError('Corpus ou perguntas mudaram após congelar o benchmark.')
    return protocol


def criar_chunks(documents,size=850,overlap=120):
    if type(size) is not int or type(overlap) is not int or not 100<=size<=2000 or not 0<=overlap<size:
        raise ValueError('Chunking inválido.')
    rows=[]
    for doc in documents:
        prefix=doc['title']+'\n'
        width=size-len(prefix)
        if width<=overlap:raise ValueError('Título longo demais para o chunking.')
        for start in range(0,len(doc['text']),width-overlap):
            rows.append({'id':doc['id'],'title':doc['title'],'text':prefix+doc['text'][start:start+width]})
    return rows


def ranking_semantico(vector,vectors,chunks,k=5):
    vector=np.asarray(vector,dtype=float);vectors=np.asarray(vectors,dtype=float)
    if vector.shape!=(384,) or vectors.shape!=(len(chunks),384) or not np.isfinite(vector).all() or not np.isfinite(vectors).all() or type(k) is not int or not 1<=k<=5:
        raise ValueError('Vetores ou k inválidos.')
    scores=vectors@vector;ordered=sorted(range(len(chunks)),key=lambda i:(-scores[i],chunks[i]['id'],i))
    seen=set();rows=[]
    for i in ordered:
        if chunks[i]['id'] in seen:continue
        seen.add(chunks[i]['id'])
        rows.append({'id':chunks[i]['id'],'title':chunks[i]['title'],'score':float(np.clip(scores[i],0,1)),'trecho':chunks[i]['text'][:900]})
        if len(rows)==k:break
    return rows


def carregar_vetores(directory):
    directory=Path(directory);protocol=protocolo(directory)
    meta=json.loads((directory/'semantica_meta.json').read_text());path=directory/'semantica_vetores.npz'
    if path.is_symlink() or path.stat().st_size>2_000_000 or hashlib.sha256(path.read_bytes()).hexdigest()!=meta['vetores_sha256']:
        raise ValueError('Cache de vetores inválido.')
    docs=json.loads((directory/'benchmark_corpus.json').read_text())
    expected=criar_chunks(docs,protocol['chunks_caracteres'],protocol['sobreposicao'])
    cases=json.loads((directory/'retrieval_benchmark_parafraseado.json').read_text())
    outside=json.loads((directory/'retrieval_fora_do_escopo.json').read_text())
    queries=[c['query'] for c in cases]+outside
    if meta['chunks']!=expected or meta['queries']!=queries:raise ValueError('Cache diverge de textos ou perguntas.')
    with np.load(path,allow_pickle=False) as archive:
        if set(archive.files)!={'chunks','queries'}:raise ValueError('Campos de cache inválidos.')
        chunks=archive['chunks'];questions=archive['queries']
    if chunks.shape!=(len(expected),384) or questions.shape!=(len(queries),384) or not np.isfinite(chunks).all() or not np.isfinite(questions).all():
        raise ValueError('Dimensões de cache inválidas.')
    return meta,chunks,questions


def medir(cases,outside,ranker,threshold):
    rows=[];r1=r3=mrr=covered=correct=0
    for i,c in enumerate(cases):
        ranking=ranker(c['query'],i);ids=[r['id'] for r in ranking]
        hit=ids.index(c['expected'])+1 if c['expected'] in ids else None
        r1+=hit==1;r3+=hit is not None and hit<=3;mrr+=1/hit if hit else 0
        response=bool(ranking and ranking[0]['score']>threshold);covered+=response;correct+=response and hit==1
        rows.append({'query':c['query'],'expected':c['expected'],'rank':hit,'respondida':response,'ranking':ids})
    abstentions=sum(not (ranking:=ranker(q,len(cases)+i)) or ranking[0]['score']<=threshold for i,q in enumerate(outside))
    n=len(cases)
    return {'recall@1':r1/n,'recall@3':r3/n,'MRR@5':mrr/n,'cobertura':covered/n,'precisao_coberta':correct/covered if covered else None,'abstencao_fora_escopo':abstentions/len(outside),'limiar':threshold,'casos':rows}
