"""Gera os .ipynb a partir dos notebooks .py (fonte canônica)."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def convert(path):
    cells = []
    for n, part in enumerate(path.read_text().split("# COMMAND ----------")):
        part = part.replace("# Databricks notebook source", "", 1).strip()
        if not part:
            continue
        if part.startswith("# MAGIC"):
            part = "\n".join(line.removeprefix("# MAGIC ").removeprefix("# MAGIC") for line in part.splitlines())
        kind = "markdown" if part.startswith("%md") else "code"
        if kind == "markdown":
            part = part[3:].strip()
        cell = {"id": hashlib.sha256(f"{path.stem}:{n}".encode()).hexdigest()[:12],
                "cell_type": kind, "metadata": {}, "source": (part + "\n").splitlines(True)}
        if kind == "code":
            cell.update(execution_count=None, outputs=[])
        cells.append(cell)
    return {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}


if __name__ == "__main__":
    for path in sorted((ROOT / "notebooks").glob("*.py")):
        path.with_suffix(".ipynb").write_text(json.dumps(convert(path), ensure_ascii=False, indent=2) + "\n")
    print("Notebooks exportados sem saídas de execução.")
