"""Garante que os exercícios são justos: a solução passa e o esqueleto, não."""
import os
import ast
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def executar(solucoes):
    with tempfile.TemporaryDirectory(prefix='lab-bricks-exercicios-') as directory:
        temp=Path(directory)
        shutil.copytree(ROOT/'exercicios',temp/'exercicios',ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(ROOT/'solucoes',temp/'solucoes',ignore=shutil.ignore_patterns('__pycache__'))
        if not solucoes:
            for reference in (temp/'solucoes').glob('ex*.py'):
                tree=ast.parse(reference.read_text())
                for node in tree.body:
                    if isinstance(node,ast.FunctionDef) and not node.name.startswith('_'):
                        node.body=[ast.Raise(exc=ast.Call(func=ast.Name(id='NotImplementedError',ctx=ast.Load()),args=[],keywords=[]),cause=None)]
                ast.fix_missing_locations(tree)
                (temp/'exercicios'/reference.name).write_text(ast.unparse(tree)+'\n')
        env={**os.environ,'LAB_SOLUCOES':'1' if solucoes else '0','PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':str(ROOT/'src')}
        return subprocess.run([sys.executable,'-m','pytest','exercicios/testes','-q','-p','no:cacheprovider'],cwd=temp,env=env,capture_output=True,text=True,timeout=120)


def test_solucoes_de_referencia_passam_em_todos_os_testes():
    result = executar(True)
    assert result.returncode == 0, result.stdout[-1500:]
    assert int(re.search(r"(\d+) passed", result.stdout).group(1)) >= 64


def test_esqueletos_nao_passam_em_nenhum_teste():
    result = executar(False)
    assert result.returncode != 0
    assert " passed" not in result.stdout, "Algum teste passa sem o aluno escrever código: o exercício não ensina nada."
    assert re.search(r"(\d+) failed", result.stdout)


def test_todo_exercicio_tem_solucao_e_teste():
    nomes = sorted(p.stem for p in (ROOT / "exercicios").glob("ex*.py"))
    assert len(nomes) == 14
    for nome in nomes:
        assert (ROOT / "solucoes" / f"{nome}.py").exists() and (ROOT / "exercicios/testes" / f"test_{nome}.py").exists()
