"""Consulta o OSV para todas as versões do lockfile; falha se não puder auditar."""
from pathlib import Path
import json
import urllib.request
import sys

ROOT = Path(__file__).resolve().parents[1]


def audit():
    versions = {}
    for path in [ROOT / "requirements.lock", ROOT / "requirements-spark.txt"]:
        for line in path.read_text().splitlines():
            if line.strip() and not line.startswith(("#", "-r")):
                name, version = line.split("==", 1)
                versions[name] = version
    packages = sorted(versions.items())
    queries = [{"package": {"name": name, "ecosystem": "PyPI"}, "version": version} for name, version in packages]
    request = urllib.request.Request("https://api.osv.dev/v1/querybatch", data=json.dumps({"queries": queries}).encode(),
                                     headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)
    results = data["results"]
    if len(results) != len(packages):
        raise RuntimeError("Resposta incompleta da auditoria.")
    findings = [{"pacote": name, "versao": version, "advisories": [v["id"] for v in result.get("vulns", [])]}
                for (name, version), result in zip(packages, results) if result.get("vulns")]
    print(json.dumps({"consultados": len(packages), "achados": findings}, ensure_ascii=False, indent=2))
    return bool(findings)


if __name__ == "__main__":
    try:
        sys.exit(1 if audit() else 0)
    except Exception:
        print("A auditoria de dependências não pôde ser concluída. Tente novamente com acesso ao OSV.")
        sys.exit(2)
