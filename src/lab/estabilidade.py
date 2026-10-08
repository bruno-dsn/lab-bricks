"""Quanto a escolha de modelo e limiar muda quando a amostra muda? Repete o ciclo em várias amostras."""
import numpy as np
import pandas as pd

from .classificacao import gerar_entregas
from .ciclo_ml import avaliar_ciclo

CUSTO_FP, CUSTO_FN = 5, 30


def limiar_teorico(custo_fp=CUSTO_FP, custo_fn=CUSTO_FN):
    """Com probabilidades calibradas, alertar compensa quando p * custo_fn >= (1 - p) * custo_fp."""
    if not all(isinstance(c, (int, float)) and not isinstance(c, bool) and np.isfinite(c) and c > 0 for c in (custo_fp, custo_fn)):
        raise ValueError("Custos precisam ser positivos.")
    return custo_fp / (custo_fp + custo_fn)


def repetir_selecao(amostras=30, entregas=600, seed_modelo=42):
    """Roda o ciclo completo em `amostras` conjuntos sintéticos (sementes 0..amostras-1)."""
    if type(amostras) is not int or not 5 <= amostras <= 60:
        raise ValueError("Use de 5 a 60 amostras.")
    rows = []
    for seed in range(amostras):
        _, board, final, scored = avaliar_ciclo(gerar_entregas(entregas, seed), seed_modelo)
        best_by_model = board.groupby("modelo").custo.min().sort_values()
        negatives = int((scored.atrasou == 0).sum())
        positives = int(scored.atrasou.sum())
        rows.append({
            "amostra": seed, "modelo": final["modelo"], "limiar": final["limiar"],
            "custo_validacao": final["custo_validacao"],
            "margem_validacao": int(best_by_model.iloc[1] - best_by_model.iloc[0]),
            "custo_teste": final["custo"],
            "custo_nunca_alertar": positives * CUSTO_FN,
            "custo_sempre_alertar": negatives * CUSTO_FP,
        })
    return pd.DataFrame(rows)


def intervalo_bootstrap(valores, repeticoes=2000, nivel=0.95, seed=0):
    """Intervalo percentil da média, reamostrando com reposição."""
    values = np.asarray(valores, dtype=float)
    if values.ndim != 1 or not 2 <= len(values) <= 10_000 or not np.isfinite(values).all():
        raise ValueError("Use um vetor finito com pelo menos dois valores.")
    if type(repeticoes) is not int or not 100 <= repeticoes <= 20_000 or not isinstance(nivel, (int, float)) or isinstance(nivel, bool) or not 0.5 <= nivel < 1 or len(values) * repeticoes > 20_000_000:
        raise ValueError("Repetições ou nível fora do intervalo permitido.")
    rng = np.random.default_rng(seed)
    means = np.concatenate([rng.choice(values, size=(min(128, repeticoes-i), len(values)), replace=True).mean(axis=1) for i in range(0, repeticoes, 128)])
    low, high = np.quantile(means, [(1 - nivel) / 2, 1 - (1 - nivel) / 2])
    return float(low), float(high)


def resumir(frame):
    """Números que a aula usa: frequência de escolha, dispersão do limiar e ganho sobre "nunca alertar"."""
    ganho = frame.custo_nunca_alertar - frame.custo_teste
    baixo, alto = intervalo_bootstrap(ganho)
    return {
        "amostras": len(frame),
        "escolhas": frame.modelo.value_counts().to_dict(),
        "limiar_mediana": float(frame.limiar.median()),
        "limiar_min": float(frame.limiar.min()), "limiar_max": float(frame.limiar.max()),
        "margem_mediana": float(frame.margem_validacao.median()),
        "ganho_medio": float(ganho.mean()), "ganho_ic95": (baixo, alto),
        "ganho_sempre_alertar_medio": float((frame.custo_sempre_alertar - frame.custo_teste).mean()),
        "amostras_onde_modelo_perde": int((ganho < 0).sum()),
        "limiar_teorico": limiar_teorico(),
    }
