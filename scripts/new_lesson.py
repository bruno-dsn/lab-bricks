"""Gera uma aula inicial sem sobrescrever arquivos ou sair do catálogo."""
from pathlib import Path
import argparse
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from lab.conteudo import carregar, modelo_aula


def criar(identifier, title, track):
    lessons, tracks, _ = carregar(ROOT / 'content')
    if track not in tracks or identifier in {a.id for a in lessons}:
        raise ValueError('Trilha desconhecida ou ID de aula já existente.')
    text = modelo_aula(identifier, title, track)
    path = ROOT / 'content/aulas' / (identifier + '.md')
    with path.open('x', encoding='utf-8') as file:
        file.write(text)
    return path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--id', required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--track', required=True)
    args = parser.parse_args()
    try:
        print(criar(args.id, args.title, args.track).relative_to(ROOT))
    except (ValueError, FileExistsError) as error:
        parser.error(str(error))
