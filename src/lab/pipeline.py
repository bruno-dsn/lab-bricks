"""Bronze -> validação -> Silver -> métricas, com valores em centavos."""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import re

import pandas as pd
from .dados import COLUNAS


@dataclass
class Resultado:
    bronze: pd.DataFrame
    silver: pd.DataFrame
    rejeitadas: pd.DataFrame
    substituidas: pd.DataFrame
    gold: pd.DataFrame


def _centavos(value):
    text = str(value).strip()
    if not re.fullmatch(r"[0-9]{1,8}(\.[0-9]{1,2})?", text):
        return None
    try:
        value = Decimal(text)
        return int(value * 100) if value > 0 else None
    except (InvalidOperation, ValueError):
        return None


def tratar(rows):
    if not isinstance(rows, list) or not rows or len(rows) > 2010:
        raise ValueError("A fonte deve ter entre 1 e 2010 registros.")
    if any(not isinstance(row, dict) or set(row) != set(COLUNAS) for row in rows):
        raise ValueError("A fonte deve seguir o contrato de colunas.")
    if any(value is not None and not isinstance(value, str)
           for row in rows for value in row.values()):
        raise ValueError("Os campos da fonte devem ser texto ou nulos.")
    bronze = pd.DataFrame(rows, columns=COLUNAS).copy()
    latest = {}
    rejected, superseded = [], []
    # A versão é a data de atualização; a ordem da fonte desempata.
    for ordem, raw in enumerate(rows):
        row = {k: "" if v is None else v.strip() for k, v in raw.items()}
        row["status"] = row["status"].lower()
        updated = pd.to_datetime(row["atualizado_em"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
        if not row["venda_id"] or pd.isna(updated) or not re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", row["atualizado_em"]):
            rejected.append({**row, "motivo": "chave ou atualização inválida"})
            continue
        rank = (updated, ordem)
        old = latest.get(row["venda_id"])
        if old is None or rank > old[0]:
            if old is not None:
                superseded.append(old[1])
            latest[row["venda_id"]] = (rank, row)
        else:
            superseded.append(row)
    clean = []
    for _, row in latest.values():
        dia = pd.to_datetime(row["data_venda"], format="%Y-%m-%d", errors="coerce")
        reasons = []
        if pd.isna(dia) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["data_venda"]):
            reasons.append("data inválida")
        qty = int(row["quantidade"]) if re.fullmatch(r"[0-9]{1,4}", row["quantidade"]) else 0
        if not 1 <= qty <= 1000:
            reasons.append("quantidade inválida")
        cents = _centavos(row["preco_unitario"])
        if cents is None:
            reasons.append("preço inválido")
        if not row["produto"] or not row["categoria"] or not row["canal"]:
            reasons.append("dimensão vazia")
        if row["status"] not in {"concluida", "cancelada"}:
            reasons.append("status inválido")
        if reasons:
            rejected.append({**row, "motivo": "; ".join(reasons)})
        else:
            clean.append({**row, "quantidade": qty, "preco_centavos": cents,
                          "valor_centavos": qty * cents})
    silver = pd.DataFrame(clean, columns=COLUNAS + ["preco_centavos", "valor_centavos"])
    gold = gold_diario(silver)
    return Resultado(bronze, silver,
                     pd.DataFrame(rejected, columns=COLUNAS + ["motivo"]),
                     pd.DataFrame(superseded, columns=COLUNAS), gold)


def gold_diario(silver):
    completed = silver.loc[silver["status"].eq("concluida")]
    if completed.empty:
        return pd.DataFrame(columns=["data_venda", "pedidos", "receita_centavos", "receita", "ticket_medio"])
    result = completed.groupby("data_venda", as_index=False).agg(
        pedidos=("venda_id", "count"), receita_centavos=("valor_centavos", "sum"))
    result["receita"] = result["receita_centavos"] / 100
    result["ticket_medio"] = result["receita"] / result["pedidos"]
    return result


def indicadores(silver):
    df = silver.loc[silver["status"].eq("concluida")]
    pedidos = len(df)
    receita = int(df["valor_centavos"].sum()) / 100 if pedidos else 0.0
    return {"pedidos": pedidos, "receita": receita,
            "ticket_medio": receita / pedidos if pedidos else 0.0}
