"""Escolhe de onde importar os exercícios: sua pasta `exercicios/` ou, na CI, `solucoes/`."""
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PASTA = "solucoes" if os.environ.get("LAB_SOLUCOES") == "1" else "exercicios"
sys.path.insert(0, str(RAIZ / PASTA))
