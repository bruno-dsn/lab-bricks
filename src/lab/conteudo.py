"""Catálogo versionado de aulas próprias; sem carregar código ou URLs externas."""
from dataclasses import dataclass
from pathlib import Path
import json
import re
import tomllib

ID = re.compile(r"[a-z][a-z0-9_-]{2,60}\Z")
MAX_PROGRESSO = 100_000


@dataclass(frozen=True)
class Aula:
    id: str
    titulo: str
    trilha: str
    nivel: str
    versao: str
    requisitos: tuple
    fontes: tuple
    objetivos: tuple
    laboratorio: str
    corpo: str
    arquivo: Path


def ler_aula(path):
    path = Path(path)
    if path.is_symlink() or path.stat().st_size > 80_000:
        raise ValueError("Aula fora do contrato de tamanho ou tipo de arquivo.")
    text = path.read_text(encoding="utf-8")
    parts = text.split("+++", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError(f"Metadados TOML ausentes: {path.name}")
    meta = tomllib.loads(parts[1])
    required = {"id", "title", "track", "level", "version", "prerequisites", "sources", "objectives"}
    if required - meta.keys():
        raise ValueError(f"Metadados incompletos: {path.name}")
    for key in ("id", "track"):
        if not isinstance(meta[key], str) or not ID.fullmatch(meta[key]):
            raise ValueError(f"Identificador inválido: {path.name}")
    for key in ("title", "level", "version"):
        if not isinstance(meta[key], str) or not 1 <= len(meta[key]) <= 160:
            raise ValueError(f"Campo inválido: {path.name}")
    for key in ("prerequisites", "sources", "objectives"):
        if not isinstance(meta[key], list) or len(meta[key]) > 12 or not all(isinstance(v, str) and 1 <= len(v) <= 300 for v in meta[key]):
            raise ValueError(f"Lista inválida: {path.name}")
    body = parts[2].strip()
    headings = ("Problema", "Conceito", "Exemplo explicado", "Experimente", "Resultado esperado", "Erros comuns", "Desafio", "Critério de conclusão", "Referências")
    if any(f"## {h}" not in body for h in headings):
        raise ValueError(f"Seções pedagógicas incompletas: {path.name}")
    lab = meta.get("lab", "Leitura e prática guiada")
    if not isinstance(lab, str) or len(lab) > 160:
        raise ValueError("Laboratório inválido.")
    return Aula(meta["id"], meta["title"], meta["track"], meta["level"], meta["version"], tuple(meta["prerequisites"]), tuple(meta["sources"]), tuple(meta["objectives"]), lab, body, path)


def carregar(root):
    root = Path(root)
    tracks = json.loads((root / "tracks.json").read_text())
    sources = json.loads((root / "sources.json").read_text())
    lessons = [ler_aula(p) for p in sorted((root / "aulas").glob("*.md"))]
    by_id = {a.id: a for a in lessons}
    if len(by_id) != len(lessons):
        raise ValueError("IDs de aulas duplicados.")
    for a in lessons:
        if a.trilha not in tracks or set(a.fontes) - sources.keys() or set(a.requisitos) - by_id.keys():
            raise ValueError(f"Referência desconhecida na aula {a.id}.")
    visiting, done = set(), set()

    def visit(key):
        if key in visiting:
            raise ValueError("Ciclo nos pré-requisitos.")
        if key in done:
            return
        visiting.add(key)
        for previous in by_id[key].requisitos:
            visit(previous)
        visiting.remove(key)
        done.add(key)

    for key in by_id:
        visit(key)
    return lessons, tracks, sources


def exportar_progresso(completed, valid_ids):
    if not set(completed) <= set(valid_ids):
        raise ValueError("Progresso contém aulas desconhecidas.")
    return json.dumps({"format": "lab-bricks-progress", "version": 1, "completed": sorted(set(completed))}, ensure_ascii=False, indent=2).encode("utf-8")


def importar_progresso(payload, valid_ids):
    if not isinstance(payload, bytes) or len(payload) > MAX_PROGRESSO:
        raise ValueError("Arquivo de progresso deve ter até 100 KB.")
    try:
        value = json.loads(payload)
    except (ValueError, UnicodeDecodeError, RecursionError):
        raise ValueError("JSON de progresso inválido.") from None
    if not isinstance(value, dict) or set(value) != {"format", "version", "completed"} or value["format"] != "lab-bricks-progress" or type(value["version"]) is not int or value["version"] != 1:
        raise ValueError("Formato de progresso incompatível.")
    completed = value["completed"]
    if not isinstance(completed, list) or len(completed) > 500 or not all(isinstance(x, str) for x in completed):
        raise ValueError("Lista de progresso inválida.")
    if set(completed) - set(valid_ids):
        raise ValueError("O arquivo contém aulas ausentes nesta versão do catálogo.")
    return set(completed)


def modelo_aula(identifier, title, track):
    if not isinstance(identifier, str) or not ID.fullmatch(identifier) or not ID.fullmatch(track):
        raise ValueError("Use um identificador simples em minúsculas.")
    if not isinstance(title, str) or not 1 <= len(title.strip()) <= 160 or any(ord(c) < 32 for c in title):
        raise ValueError("Informe um título de até 160 caracteres.")
    # Strings JSON também são strings básicas TOML: impedem quebra do cabeçalho.
    quote = lambda x: json.dumps(x, ensure_ascii=False)
    return f'''+++
id = {quote(identifier)}
title = {quote(title.strip())}
track = {quote(track)}
level = "Intermediário"
version = "1.0"
prerequisites = []
sources = ["oficial"]
objectives = ["Descreva uma habilidade observável ao concluir"]
lab = "Leitura e prática guiada"
+++

# {title.strip()}

## Problema
Apresente uma situação concreta.

## Conceito
Explique a técnica com suas próprias palavras.

## Exemplo explicado
Inclua um exemplo pequeno e reproduzível.

## Experimente
Escreva passos e indique local ou Databricks.

## Resultado esperado
Defina contagens, métricas ou evidências verificáveis.

## Erros comuns
Explique um erro e como diagnosticá-lo.

## Desafio
Proponha uma variação que exija uma decisão.

## Critério de conclusão
Liste a evidência que demonstra aprendizado.

## Referências
Inclua links oficiais e atribua as fontes utilizadas.
'''
