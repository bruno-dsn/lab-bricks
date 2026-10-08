"""Downloads opcionais, explícitos, limitados e verificados; fora do projeto."""
from pathlib import Path
import argparse, hashlib, sys, urllib.request
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from lab.encoder_local import FILES,REVISION

parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('modelo',choices=['encoder','qwen']);parser.add_argument('--destino',type=Path,required=True)
args=parser.parse_args();directory=args.destino.resolve()
if directory==ROOT or ROOT in directory.parents:parser.error('Escolha uma pasta fora do repositório.')
directory.mkdir(parents=True,exist_ok=True)
if args.modelo=='encoder':
    jobs=[(name,f'https://huggingface.co/Xenova/paraphrase-multilingual-MiniLM-L12-v2/resolve/{REVISION}/'+('onnx/' if name.endswith('.onnx') else '')+name,sha,130_000_000 if name.endswith('.onnx') else 20_000_000) for name,sha in FILES.items()]
else:
    jobs=[('qwen2.5-0.5b-instruct-q4_k_m.gguf','https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/9217f5db79a29953eb74d5343926648285ec7e67/qwen2.5-0.5b-instruct-q4_k_m.gguf','74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db',510_000_000)]
for name,url,sha,limit in jobs:
    target=directory/name;partial=target.with_suffix(target.suffix+'.part')
    try:
        with urllib.request.urlopen(url,timeout=40) as response,partial.open('wb') as out:
            total=0
            while chunk:=response.read(1024*1024):
                total+=len(chunk)
                if total>limit:raise ValueError('Modelo acima do limite de bytes.')
                out.write(chunk)
        if hashlib.sha256(partial.read_bytes()).hexdigest()!=sha:raise ValueError('SHA divergente. Não aceitar automaticamente uma versão nova.')
        partial.replace(target);print(name,': SHA verificado,',total,'bytes')
    finally:partial.unlink(missing_ok=True)
