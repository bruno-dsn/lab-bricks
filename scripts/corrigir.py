"""Corrige um exercício local e gera feedback importável no caderno."""
from pathlib import Path
import argparse, hashlib, json, os, re, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]


def main():
    names=sorted(p.stem for p in (ROOT/'exercicios').glob('ex*.py'))
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('exercicio',choices=names)
    args=parser.parse_args();path=ROOT/'exercicios'/f'{args.exercicio}.py'
    env={**os.environ,'LAB_SOLUCOES':'0','PYTHONPATH':str(ROOT/'src')}
    try:
        run=subprocess.run([sys.executable,'-m','pytest','-o','addopts=','-q',f'exercicios/testes/test_{args.exercicio}.py'],cwd=ROOT,env=env,capture_output=True,text=True,timeout=120)
    except subprocess.TimeoutExpired:
        print('Correção interrompida após 120 segundos. Revise loops e tamanho da entrada.');return 2
    print(run.stdout);print(run.stderr,end='')
    counts={key:sum(int(n) for n in re.findall(rf'(\d+) {key}\b',run.stdout)) for key in ('passed','failed','errors')}
    counts['errors']+=sum(int(n) for n in re.findall(r'(\d+) error\b',run.stdout))
    valid=run.returncode==0 and counts['passed']>0 and counts['failed']==counts['errors']==0
    if run.returncode!=0 and counts['failed']==counts['errors']==0:counts['errors']=1
    value={'format':'lab-bricks-feedback','version':1,'exercicio':args.exercicio,**counts,'validado':valid,'codigo_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    directory=ROOT/'artifacts';directory.mkdir(exist_ok=True)
    output=directory/f'{args.exercicio}-feedback.json';output.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    print('Feedback salvo em',output.relative_to(ROOT));return run.returncode


if __name__=='__main__':sys.exit(main())
