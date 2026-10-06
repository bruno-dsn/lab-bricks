"""Recria imagens originais e o CSV, sem buscar recursos externos."""
from pathlib import Path
import csv
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from lab.dados import gerar_vendas, COLUNAS
from lab.pipeline import tratar
from lab.ml import comparar

ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

capa = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 570" role="img" aria-labelledby="title desc">
<title id="title">Databricks na prática</title>
<desc id="desc">Trilha de dados em português, com SQL, lakehouse, Delta e machine learning. Um percurso visual de dados recebidos até uma decisão.</desc>
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#102438"/><stop offset="1" stop-color="#0a1420"/></linearGradient></defs>
<rect width="1440" height="570" rx="28" fill="url(#bg)"/>
<g stroke="#274056" opacity=".45"><path d="M920 0V570M1060 0V570M1200 0V570M1340 0V570M880 90H1440M880 230H1440M880 370H1440M880 510H1440"/></g>
<g font-family="Arial, sans-serif"><rect x="70" y="58" width="327" height="36" rx="18" fill="#22364a"/>
<text x="92" y="82" font-size="15" font-weight="700" letter-spacing="2" fill="#8ee0d4">APRENDA COM UM PROJETO</text>
<text x="70" y="194" font-size="76" font-weight="700" letter-spacing="-3" fill="#f2eee8">Databricks</text>
<text x="70" y="278" font-size="76" font-weight="700" letter-spacing="-3" fill="#ff795d">na prática.</text>
<text x="74" y="339" font-size="25" fill="#b0c1d1">Do primeiro dado à primeira decisão.</text>
<text x="74" y="378" font-size="21" fill="#b0c1d1">Leia a regra. Mude o exemplo. Confira o resultado.</text>
<text x="74" y="463" font-size="16" font-weight="700" letter-spacing="2" fill="#f2eee8">SQL  /  LAKEHOUSE  /  DELTA  /  ML</text>
<text x="74" y="514" font-size="14" fill="#7e98af">BRUNO NUNES · TRILHA EM PORTUGUÊS · DADOS FICTÍCIOS</text>
<g transform="translate(1000 84)"><rect width="338" height="107" rx="18" fill="#22364a" stroke="#48647a"/>
<circle cx="36" cy="33" r="6" fill="#8ee0d4"/><text x="56" y="39" font-size="16" fill="#8ee0d4">01 · RECEBER</text>
<text x="30" y="80" font-size="25" fill="#f2eee8">Pedidos e suas versões</text></g>
<path d="M1169 201V233" stroke="#8ee0d4" stroke-width="3"/><path d="M1162 225L1169 233L1176 225" fill="none" stroke="#8ee0d4" stroke-width="3"/>
<g transform="translate(941 244)"><rect width="338" height="107" rx="18" fill="#22364a" stroke="#ff795d"/>
<circle cx="36" cy="33" r="6" fill="#ff795d"/><text x="56" y="39" font-size="16" fill="#ff795d">02 · CONFERIR</text>
<text x="30" y="80" font-size="25" fill="#f2eee8">Qualidade e métricas</text></g>
<path d="M1110 362V394" stroke="#8ee0d4" stroke-width="3"/><path d="M1103 386L1110 394L1117 386" fill="none" stroke="#8ee0d4" stroke-width="3"/>
<g transform="translate(1000 405)"><rect width="338" height="107" rx="18" fill="#22364a" stroke="#48647a"/>
<circle cx="36" cy="33" r="6" fill="#8ee0d4"/><text x="56" y="39" font-size="16" fill="#8ee0d4">03 · RESPONDER</text>
<text x="30" y="80" font-size="25" fill="#f2eee8">Análise e previsão</text></g></g></svg>'''
(ASSETS / "capa.svg").write_text(capa)

arquitetura = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 850" role="img" aria-labelledby="t d">
<title id="t">Arquitetura do projeto de vendas</title><desc id="d">727 registros chegam à Bronze. Escolha de versão e validação encaminham 720 pedidos à Silver, seis à quarentena e uma versão à tabela de substituídas. A Gold agrega somente concluídos.</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#809bb2"/></marker></defs>
<rect width="1440" height="850" rx="22" fill="#0d1b2a"/>
<g font-family="Arial, sans-serif">
<text x="56" y="62" font-size="18" fill="#8ee0d4" letter-spacing="2">O CAMINHO DE CADA REGISTRO</text>
<text x="56" y="110" font-size="35" font-weight="700" fill="#f2eee8">Qualidade que você consegue inspecionar.</text>
<g transform="translate(500 157)"><rect width="440" height="92" rx="15" fill="#23364a" stroke="#aa8c71"/><text x="24" y="36" font-size="21" font-weight="700" fill="#e9c5a0">BRONZE · 727</text><text x="24" y="69" font-size="20" fill="#f2eee8">Fonte preservada como chegou</text></g>
<g stroke="#809bb2" stroke-width="3" marker-end="url(#arrow)" fill="none"><path d="M720 253V303"/></g>
<g transform="translate(440 314)"><rect width="560" height="95" rx="15" fill="#23364a" stroke="#ff795d"/><text x="24" y="37" font-size="23" font-weight="700" fill="#ff795d">ESCOLHER VERSÃO E VALIDAR</text><text x="24" y="72" font-size="19" fill="#f2eee8">Chave → atualização → contrato do pedido</text></g>
<g stroke="#809bb2" stroke-width="3" marker-end="url(#arrow)" fill="none"><path d="M500 417V447H250V484"/><path d="M720 417V484"/><path d="M940 417V447H1190V484"/></g>
<g transform="translate(55 495)"><rect width="390" height="110" rx="15" fill="#23364a" stroke="#c5d1dc"/><text x="24" y="38" font-size="23" font-weight="700" fill="#c5d1dc">SILVER · 720</text><text x="24" y="77" font-size="19" fill="#f2eee8">Pedidos vigentes e válidos</text></g>
<g transform="translate(525 495)"><rect width="390" height="110" rx="15" fill="#23364a" stroke="#ff795d"/><text x="24" y="38" font-size="23" font-weight="700" fill="#ff795d">QUARENTENA · 6</text><text x="24" y="77" font-size="19" fill="#f2eee8">Campos originais e motivo</text></g>
<g transform="translate(995 495)"><rect width="390" height="110" rx="15" fill="#23364a" stroke="#839bb1"/><text x="24" y="38" font-size="23" font-weight="700" fill="#aac0d3">SUBSTITUÍDAS · 1</text><text x="24" y="77" font-size="19" fill="#f2eee8">Versão anterior do pedido</text></g>
<path d="M250 613V663" fill="none" stroke="#809bb2" stroke-width="3" marker-end="url(#arrow)"/>
<g transform="translate(55 677)"><rect width="390" height="110" rx="15" fill="#23364a" stroke="#e9c77b"/><text x="24" y="38" font-size="23" font-weight="700" fill="#e9c77b">GOLD · POR DIA</text><text x="24" y="72" font-size="19" fill="#f2eee8">Receita e pedidos concluídos</text><text x="24" y="97" font-size="16" fill="#aac0d3">Cancelados ficam fora da receita</text></g>
<text x="525" y="707" font-size="22" fill="#f2eee8">727 = 720 + 6 + 1</text><text x="525" y="746" font-size="19" fill="#aac0d3">Uma entrada, um destino explicado.</text><text x="525" y="778" font-size="16" fill="#aac0d3">App: Pandas · Notebooks: Spark e Delta</text>
</g></svg>'''
(ASSETS / "arquitetura.svg").write_text(arquitetura)

rows = gerar_vendas()
with (ROOT / "data/vendas_sinteticas.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=COLUNAS)
    writer.writeheader();writer.writerows(rows)

predictions, info = comparar(tratar(rows).gold)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12, "text.color": "#f2eee8", "axes.labelcolor": "#a8bbcc", "xtick.color": "#a8bbcc", "ytick.color": "#a8bbcc"})
fig, ax = plt.subplots(figsize=(13, 6.2), facecolor="#0d1b2a")
ax.set_facecolor("#0d1b2a")
for col, label, color, style in [("real", "Receita observada", "#f2eee8", "-"), ("baseline", "Baseline: ontem", "#54c4b8", "--"), ("modelo", "Modelo Ridge", "#ff795d", "-")]:
    ax.plot(predictions.index, predictions[col], label=label, color=color, linewidth=2.3, linestyle=style, marker="o", markersize=4)
ax.grid(axis="y", color="#2a3c4e", alpha=.8)
for spine in ax.spines.values():spine.set_visible(False)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x:,.0f}".replace(",", ".")))
ax.set_ylabel("Receita fictícia (R$)", labelpad=14)
import matplotlib.dates as mdates
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
ax.set_xlabel("Março de 2026 · previsão de um dia à frente", labelpad=12)
ax.legend(loc="upper left", bbox_to_anchor=(0, 1.18), ncol=3, frameon=False, labelcolor="#f2eee8")
fig.text(.075, .94, "O modelo precisa enfrentar uma baseline.", fontsize=23, fontweight="bold", color="#f2eee8")
fig.text(.075, .885, f"MAE baseline: R$ {info['mae_baseline']:.2f}   |   MAE Ridge: R$ {info['mae_modelo']:.2f}   |   14 dias de teste", fontsize=12, color="#a8bbcc", parse_math=False)
fig.subplots_adjust(left=.09, right=.97, top=.72, bottom=.17)
fig.savefig(ASSETS / "experimento.png", dpi=150, facecolor=fig.get_facecolor())
plt.close(fig)
print("Imagens e CSV gerados a partir da amostra padrão.")
