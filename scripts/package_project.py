"""Monta o ZIP de entrega sem ambientes, caches, segredos ou arquivos temporários."""
from pathlib import Path
import argparse
import hashlib
import zipfile

from verify_project import ROOT, verify

ROOT_FILES = {
    "README.md", "LICENSE", "CONTRIBUTING.md", "SECURITY.md", "app.py",
    ".gitignore", "pyproject.toml", "requirements.txt", "requirements-dev.txt",
    "requirements.lock", "requirements-spark.txt",
}
FOLDERS = {".github", ".streamlit", "assets", "data", "docs", "notebooks", "scripts", "src", "tests"}
EXTENSIONS = {".py", ".md", ".txt", ".toml", ".yml", ".json", ".ipynb", ".csv", ".svg", ".png"}
SKIP_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache", ".ipynb_checkpoints", "build", "dist", "mlruns", "mlartifacts"}


def release_files():
    files = []
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if any(part in SKIP_PARTS for part in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError(f"Link simbólico fora do contrato de entrega: {relative}")
        if not path.is_file():
            continue
        allowed = (len(relative.parts) == 1 and path.name in ROOT_FILES) or (
            len(relative.parts) > 1 and relative.parts[0] in FOLDERS and path.suffix in EXTENSIONS)
        if allowed:
            files.append(path)
    return files


def package(output):
    output = output.resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError("Salve o ZIP fora da pasta do projeto.")
    if verify():
        raise ValueError("Corrija a verificação do projeto antes de empacotar.")
    files = release_files()
    output.parent.mkdir(parents=True, exist_ok=True)
    # Data e permissões estáveis permitem reproduzir o mesmo ZIP com os mesmos fontes.
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            name = f"{ROOT.name}/{path.relative_to(ROOT).as_posix()}"
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compresslevel=9)
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise RuntimeError("Falha de integridade no ZIP.")
    print(f"ZIP limpo: {len(files)} arquivos. SHA-256: {hashlib.sha256(output.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Caminho do ZIP, fora da pasta do projeto")
    package(parser.parse_args().output)
