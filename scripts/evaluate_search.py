"""Mede as mesmas perguntas com corpus congelado; não edita o benchmark."""
from pathlib import Path
import argparse, hashlib, json, sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from lab.benchmark import protocolo,criar_chunks,ranking_semantico,medir
from lab.encoder_local import EncoderLocal,REVISION,FILES
from lab.recuperacao import buscar

parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--model-dir',type=Path,required=True)
args=parser.parse_args();directory=ROOT/'content';protocol=protocolo(directory)
docs=json.loads((directory/'benchmark_corpus.json').read_text())
cases=json.loads((directory/'retrieval_benchmark_parafraseado.json').read_text());outside=json.loads((directory/'retrieval_fora_do_escopo.json').read_text())
chunks=criar_chunks(docs,protocol['chunks_caracteres'],protocol['sobreposicao']);queries=[c['query'] for c in cases]+outside
encoder=EncoderLocal(args.model_dir);cv=encoder.encode([c['text'] for c in chunks]);qv=encoder.encode(queries)
target=directory/'semantica_vetores.npz';np.savez_compressed(target,chunks=cv,queries=qv)
meta={'modelo':'Xenova/paraphrase-multilingual-MiniLM-L12-v2','revision':REVISION,'modelos_sha256':FILES,'vetores_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'chunks':chunks,'queries':queries}
(directory/'semantica_meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
results={'protocol_sha256':hashlib.sha256((directory/'search_protocol.json').read_bytes()).hexdigest(),
 'tfidf':medir(cases,outside,lambda q,i:buscar(q,docs,5),protocol['tfidf_limiar']),
 'semantica':medir(cases,outside,lambda q,i:ranking_semantico(qv[i],cv,chunks,5),protocol['semantica_limiar']),
 'limites':['Perguntas congeladas da 2.1, não independentes desta família de laboratório','Limiar não calibrado','Chunking diferente impede isolar efeito do encoder','Resultados deste recorte, sem promessa de superioridade geral']}
(directory/'search_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:{m:v for m,v in results[k].items() if m!='casos'} for k in ('tfidf','semantica')},indent=2))
