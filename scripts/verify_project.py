"""Confere artefatos e padrões de segredo sem imprimir valores encontrados."""
from pathlib import Path
import ast
import csv
import json
import re
import sys
import subprocess
import tomllib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lab.dados import gerar_vendas
from lab.conteudo import carregar
from export_notebooks import convert
from lab.benchmark import protocolo, carregar_vetores

SECRET_PATTERNS = [
    re.compile(r"dapi[a-f0-9]{32}"), re.compile(r"sk-[A-Za-z0-9_-]{30,}"),
    re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})"),
    re.compile(r"(?:AKIA|ASIA)[0-9A-Z]{16}"), re.compile(r"AIza[0-9A-Za-z_-]{35}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]


def sensitive_name(path):
    name = Path(path).name
    return name == ".env" or (name.startswith(".env.") and name != ".env.example") or name in {"secrets.toml", "id_rsa", "id_ed25519"}


def verify_history(problems):
    if not (ROOT / ".git").exists():
        return
    result = subprocess.run(["git", "rev-list", "--objects", "--all"], cwd=ROOT,
                            check=True, capture_output=True, text=True)
    for line in result.stdout.splitlines():
        sha, separator, name = line.partition(" ")
        if not separator:
            continue
        if sensitive_name(name):
            problems.append(f"Arquivo sensível no histórico Git: {name}")
        kind = subprocess.run(["git", "cat-file", "-t", sha], cwd=ROOT, check=True,
                              capture_output=True, text=True).stdout.strip()
        if kind != "blob":
            continue
        content = subprocess.run(["git", "cat-file", "blob", sha], cwd=ROOT, check=True,
                                 capture_output=True).stdout.decode("utf-8", errors="replace")
        if any(pattern.search(content) for pattern in SECRET_PATTERNS):
            problems.append(f"Possível segredo no histórico: {name}; revisar sem divulgar o valor")


def verify():
    problems = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(p in {".git", ".venv", "__pycache__", ".pytest_cache"} for p in path.parts):
            continue
        if sensitive_name(path):
            problems.append(f"Arquivo sensível presente: {path.relative_to(ROOT)}")
        if path.suffix not in {".py", ".md", ".txt", ".toml", ".yml", ".json", ".ipynb", ".csv", ".svg"}:
            continue
        content = path.read_text()
        if any(pattern.search(content) for pattern in SECRET_PATTERNS):
            problems.append(f"Possível segredo em {path.relative_to(ROOT)}; revisar sem divulgar o valor")
        if path.suffix == ".md":
            for target in re.findall(r"\]\(([^)]+)\)", content):
                if target.startswith(("https://", "http://", "#", "mailto:")):
                    continue
                resolved = path.parent / target.split("#")[0]
                if not resolved.exists():
                    problems.append(f"Link local inexistente em {path.relative_to(ROOT)}: {target}")
    for path in (ROOT / "notebooks").glob("*.py"):
        if not path.read_text().startswith("# Databricks notebook source"):
            problems.append(f"Cabeçalho de notebook ausente: {path.name}")
        notebook = json.loads(path.with_suffix(".ipynb").read_text())
        if notebook != convert(path):
            problems.append(f"IPYNB diverge da fonte: {path.name}")
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                code = "".join(cell["source"]).strip()
                if cell["outputs"] or cell["execution_count"] is not None:
                    problems.append(f"Saída de execução presente: {path.name}")
                if not code.startswith("%"):
                    ast.parse(code, filename=path.name)
    for path in [ROOT / "app.py", *(ROOT / "src").rglob("*.py"), *(ROOT / "scripts").glob("*.py"), *(ROOT / "tests").glob("*.py"), *(ROOT / "pipelines").glob("*.py"), *(ROOT / "exercicios").rglob("*.py"), *(ROOT / "solucoes").glob("*.py")]:
        ast.parse(path.read_text(), filename=str(path))
    # Cópias nativas precisam permanecer coerentes com a biblioteca local.
    for notebook, original in [("00_configuracao", "dados"), ("04_ml_sem_vazamento", "ml"), ("05_bi_modelagem", "bi"), ("09_classificacao_temporal", "classificacao"), ("10_recuperacao_e_evidencias", "recuperacao"), ("11_ciclo_ml_e_contrato", "ciclo_ml")]:
        if (ROOT / f"src/lab/{original}.py").read_text().strip() not in (ROOT / f"notebooks/{notebook}.py").read_text():
            problems.append(f"Função compartilhada divergente no {notebook}")
    with (ROOT / "data/vendas_sinteticas.csv").open(newline="") as f:
        if list(csv.DictReader(f)) != gerar_vendas():
            problems.append("CSV diverge do gerador padrão")
    # Cópias novas retiram apenas os imports relativos: os módulos já estão na célula.
    for notebook, originals in [
        ('11_ciclo_ml_e_contrato', ['rigor_ml']),
        ('12_dados_publicos_reais', ['retail_real']),
        ('13_validacao_temporal_calibracao', ['classificacao', 'ciclo_ml', 'rigor_ml']),
        ('14_cdc_scd2', ['engenharia_avancada']),
        ('15_streaming_watermark', ['engenharia_avancada']),
        ('16_rag_evidencias', ['recuperacao', 'rag']),
    ]:
        target = ROOT / f'notebooks/{notebook}.py'
        if not target.exists():
            problems.append(f'Notebook da escola ausente: {notebook}')
            continue
        for original in originals:
            shared = '\n'.join(line for line in (ROOT / f'src/lab/{original}.py').read_text().splitlines() if not line.startswith('from .')).strip()
            if shared not in target.read_text():
                problems.append(f'Cópia compartilhada divergente: {notebook}/{original}')
    config = tomllib.loads((ROOT / ".streamlit/config.toml").read_text())
    if config["client"]["showErrorDetails"] != "none" or not config["server"]["enableCORS"] or not config["server"]["enableXsrfProtection"]:
        problems.append("Configuração de proteção da interface divergente")
    try:
        lessons, tracks, sources = carregar(ROOT / "content")
        ids = {a.id for a in lessons}
        questions = json.loads((ROOT / "content/questions.json").read_text())
        if len({q['id'] for q in questions}) != len(questions):
            problems.append("IDs de questões duplicados")
        for question in questions:
            if question['lesson'] not in ids or question['track'] not in tracks or type(question['answer']) is not int or not 0 <= question['answer'] < len(question['choices']):
                problems.append("Questão com referência ou resposta inválida")
        benchmark = json.loads((ROOT / "content/retrieval_benchmark.json").read_text())
        if any(case['expected'] not in ids for case in benchmark):
            problems.append("Benchmark referencia aula inexistente")
        parafraseado = json.loads((ROOT / "content/retrieval_benchmark_parafraseado.json").read_text())
        if any(set(case) != {"query", "expected"} or case["expected"] not in ids for case in parafraseado) or len(parafraseado) < 30:
            problems.append("Benchmark parafraseado inválido ou com menos de 30 casos")
        fora = json.loads((ROOT / "content/retrieval_fora_do_escopo.json").read_text())
        if not fora or not all(isinstance(item, str) and item for item in fora):
            problems.append("Perguntas fora do escopo ausentes ou inválidas")
        starters = {p.stem for p in (ROOT / "exercicios").glob("ex*.py")}
        if starters != {p.stem for p in (ROOT / "solucoes").glob("ex*.py")}:
            problems.append("Exercícios e soluções não têm os mesmos arquivos")
        stages = json.loads((ROOT / 'content/school.json').read_text())['etapas']
        covered = [a for stage in stages for a in stage['aulas']]
        if len(covered) != len(set(covered)) or set(covered) != ids or {e for stage in stages for e in stage['exercicios']} != starters:
            problems.append('Percurso não cobre as aulas e exercícios exatamente.')
        protocolo(ROOT / 'content')
        carregar_vetores(ROOT / 'content')
    except (ValueError, KeyError) as error:
        problems.append(f"Catálogo inválido: {error}")
    verify_history(problems)
    if problems:
        print("\n".join(problems));return 1
    history = "; histórico Git incluído" if (ROOT / ".git").exists() else "; sem histórico Git local"
    print(f"Arquivos, links, sintaxe, saídas, CSV e busca limitada de segredos: OK{history}.")
    return 0


if __name__ == "__main__":
    sys.exit(verify())
