"""Inicia o app com o mesmo Python do ambiente ativo."""
from pathlib import Path
import subprocess, sys

if sys.version_info[:2] != (3,12):
    raise SystemExit('O ambiente validado usa Python 3.12. Siga a instalação e ativação do README.')
root=Path(__file__).resolve().parents[1]
print('Abra http://localhost:8501 se o navegador não abrir automaticamente.',flush=True)
raise SystemExit(subprocess.call([sys.executable,'-m','streamlit','run',str(root/'app.py'),'--server.address','localhost','--server.headless','false'],cwd=root))
