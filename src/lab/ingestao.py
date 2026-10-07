"""Simulador limitado de lotes; não emula um checkpoint do Spark."""
from dataclasses import dataclass
import hashlib
import json
import re
from lab.pipeline import tratar


@dataclass(frozen=True)
class Ingestao:
    resultado: object
    eventos: tuple


def processar_lotes(lotes):
    if not isinstance(lotes, list) or not 1 <= len(lotes) <= 20:
        raise ValueError("Informe de 1 a 20 lotes.")
    manifest, rows, events = {}, [], []
    for identifier, batch in lotes:
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-zA-Z0-9_-]{1,60}", identifier) or not isinstance(batch, list):
            raise ValueError("Lote inválido.")
        if len(batch) > 2000:
            raise ValueError("Lote muito grande.")
        # Valida a estrutura mesmo se o lote for uma repetição.
        tratar(batch)
        digest = hashlib.sha256(json.dumps(batch, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        if identifier in manifest:
            if manifest[identifier] != digest:
                raise ValueError("O mesmo ID de lote chegou com conteúdo diferente.")
            events.append({"lote": identifier, "estado": "repetido: ignorado", "recebidos": len(batch), "adicionados": 0})
            continue
        if len(rows) + len(batch) > 2000:
            raise ValueError("A demonstração aceita até 2.000 registros acumulados.")
        rows.extend(batch)
        manifest[identifier] = digest
        events.append({"lote": identifier, "estado": "aceito", "recebidos": len(batch), "adicionados": len(batch)})
    return Ingestao(tratar(rows), tuple(events))
