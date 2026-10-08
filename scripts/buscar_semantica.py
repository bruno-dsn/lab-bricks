"""Inferência local para uma pergunta nova; cache de benchmark não é busca livre."""
from pathlib import Path
import argparse, json, sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from lab.encoder_local import EncoderLocal
from lab.benchmark import carregar_vetores,ranking_semantico
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--model-dir',type=Path,required=True);parser.add_argument('pergunta')
args=parser.parse_args()
if not 1<=len(args.pergunta.strip())<=500:parser.error('Use pergunta de até 500 caracteres.')
meta,vectors,_=carregar_vetores(ROOT/'content');encoder=EncoderLocal(args.model_dir)
print(json.dumps(ranking_semantico(encoder.encode([args.pergunta])[0],vectors,meta['chunks']),ensure_ascii=False,indent=2))
