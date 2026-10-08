"""Referência: ECE de intervalos uniformes, sem biblioteca de métricas."""
import math


def ece_manual(labels, probability, bins=10):
    if len(labels)!=len(probability) or not labels or type(bins) is not int or not 2 <= bins <= 20 or any(y not in (0,1) for y in labels) or any(not math.isfinite(p) or not 0 <= p <= 1 for p in probability):
        raise ValueError('Entrada de calibração inválida.')
    groups=[[] for _ in range(bins)]
    for y,p in zip(labels,probability):groups[min(int(p*bins),bins-1)].append((y,p))
    total=0.
    for group in groups:
        if group:
            freq=sum(y for y,_ in group)/len(group);avg=sum(p for _,p in group)/len(group)
            total+=len(group)/len(labels)*abs(freq-avg)
    return total
