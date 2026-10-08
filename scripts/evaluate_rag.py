"""Sete casos congelados com geração local; contrato não certifica suporte factual."""
from pathlib import Path
import argparse, hashlib, json, math, socket, subprocess, sys, time, urllib.request

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from lab.recuperacao import buscar
from lab.rag import prompt_geracao,validar_resposta,ABSTENCAO
from lab.benchmark import protocolo

MODEL_SHA='74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db'
SCHEMA={'type':'object','properties':{'resposta':{'type':'string'},'citacoes':{'type':'array','items':{'type':'string'}},'absteve':{'type':'boolean'}},'required':['resposta','citacoes','absteve'],'additionalProperties':False}


def run(args):
    if not 1024<=args.port<=65535 or args.preco_cpu_hora is not None and (not math.isfinite(args.preco_cpu_hora) or args.preco_cpu_hora<=0):
        raise ValueError('Porta ou preço inválidos.')
    if args.model_path.is_symlink() or args.model_path.stat().st_size>510_000_000 or hashlib.sha256(args.model_path.read_bytes()).hexdigest()!=MODEL_SHA:
        raise ValueError('Modelo diverge da versão registrada.')
    version=subprocess.check_output([str(args.server_bin),'--version'],stderr=subprocess.STDOUT,text=True,timeout=10)
    if '11429' not in version or 'd81235049' not in version:raise ValueError('Use o engine b11429 registrado no protocolo.')
    with socket.socket() as probe:
        if probe.connect_ex(('127.0.0.1',args.port))==0:raise ValueError('Porta já ocupada. Escolha outra; não usar um servidor desconhecido.')
    directory=ROOT/'content';protocolo(directory)
    path=directory/'rag_protocol.json';protocol=json.loads(path.read_text());docs=json.loads((directory/'benchmark_corpus.json').read_text())
    artifacts=ROOT/'artifacts';artifacts.mkdir(exist_ok=True)
    log=(artifacts/'rag-engine.log').open('w')
    server=subprocess.Popen([str(args.server_bin),'--model',str(args.model_path),'--host','127.0.0.1','--port',str(args.port),'--ctx-size','4096','--threads','2','--n-predict',str(protocol['max_tokens']),'--no-webui'],stdout=log,stderr=log)
    base=f'http://127.0.0.1:{args.port}';rows=[]
    try:
        ready=False
        for _ in range(40):
            if server.poll() is not None:raise RuntimeError('Engine encerrou; consulte artifacts/rag-engine.log localmente.')
            try:
                with urllib.request.urlopen(base+'/health',timeout=1) as response:
                    if response.status==200:ready=True;break
            except OSError:pass
            time.sleep(.5)
        if not ready:raise RuntimeError('Engine não ficou pronto em vinte segundos.')
        for case in protocol['casos']:
            evidence=buscar(case['query'],docs,protocol['k'])
            if 'injecao' in case:evidence=[{'id':'contexto-nao-confiavel','title':'Teste de injeção','score':1.,'trecho':case['injecao']},*evidence[:2]]
            messages=prompt_geracao(case['query'],evidence)
            body={'model':'local','messages':messages,'temperature':protocol['temperature'],'seed':protocol['seed'],'max_tokens':protocol['max_tokens'],'response_format':{'type':'json_schema','json_schema':{'name':'resposta_lab_bricks','strict':True,'schema':SCHEMA}}}
            request=urllib.request.Request(base+'/v1/chat/completions',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
            started=time.perf_counter()
            with urllib.request.urlopen(request,timeout=90) as response:data=json.load(response)
            elapsed=time.perf_counter()-started;raw=data['choices'][0]['message']['content']
            accepted=True;reason='';answer={'resposta':ABSTENCAO,'citacoes':[],'absteve':True}
            try:answer=validar_resposta(json.loads(raw),evidence)
            except (ValueError,TypeError) as error:accepted=False;reason=str(error)[:300]
            usage=data.get('usage',{});tokens=int(usage.get('prompt_tokens',0))+int(usage.get('completion_tokens',0))
            row={'id':case['id'],'pergunta':case['query'],'documento_esperado':case['expected'],'recuperou_esperado':case['expected'] in [e['id'] for e in evidence] if case['expected'] else None,'contrato_aceito':accepted,'motivo_rejeicao':reason,'absteve':answer['absteve'],'citacoes':answer['citacoes'],'resposta':answer['resposta'],'resposta_bruta':raw[:10_000],'latencia_segundos':elapsed,'tokens':tokens,'custo_estimado':elapsed/3600*args.preco_cpu_hora if args.preco_cpu_hora is not None else None,'suporte_factual':'revisão humana pendente'}
            rows.append(row);print(case['id'],': contrato',accepted,'; abstenção',answer['absteve'],flush=True)
    finally:
        server.terminate()
        try:server.wait(timeout=10)
        except subprocess.TimeoutExpired:server.kill();server.wait(timeout=5)
        log.close()
    summary={'casos':len(rows),'contratos_aceitos':sum(r['contrato_aceito'] for r in rows),'contratos_rejeitados':sum(not r['contrato_aceito'] for r in rows),'abstencoes':sum(r['absteve'] for r in rows),'respostas_com_contrato':sum(r['contrato_aceito'] and not r['absteve'] for r in rows),'tokens':sum(r['tokens'] for r in rows),'avaliacao_factual':'pendente','preco_cpu_hora':args.preco_cpu_hora}
    report={'protocol_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'modelo':'Qwen2.5-0.5B-Instruct-Q4_K_M','modelo_sha256':MODEL_SHA,'engine_versao':version.strip(),'engine_binario_sha256':hashlib.sha256(args.server_bin.read_bytes()).hexdigest(),'resumo':summary,'casos':rows}
    (directory/'rag_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--model-path',type=Path,required=True);parser.add_argument('--server-bin',type=Path,required=True);parser.add_argument('--port',type=int,default=8081);parser.add_argument('--preco-cpu-hora',type=float)
    args=parser.parse_args();args.model_path=args.model_path.resolve();args.server_bin=args.server_bin.resolve();run(args)
