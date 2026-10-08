"""Gráficos dos resultados registrados, sem inferir desempenho geral."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
NAVY,LAVA,LIGHT='#0B2026','#FF3621','#F9F7F4'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':NAVY,'axes.labelcolor':NAVY,'xtick.color':NAVY,'ytick.color':NAVY})
d=json.loads((ROOT/'content/search_results.json').read_text())
fig,ax=plt.subplots(figsize=(12,5.8),facecolor=LIGHT);ax.set_facecolor(LIGHT)
x=[0,1,2];w=.32
for offset,key,label,color in [(-w/2,'tfidf','TF-IDF',NAVY),(w/2,'semantica','Encoder local',LAVA)]:
 vals=[100*d[key][m] for m in ['recall@1','recall@3','MRR@5']]
 bars=ax.bar([v+offset for v in x],vals,width=w,color=color,label=label)
 ax.bar_label(bars,labels=[f'{v:.1f}%' for v in vals],padding=5)
ax.set_xticks(x,['Recall@1','Recall@3','MRR@5 x 100']);ax.set_ylim(0,100);ax.set_ylabel('Percentual / MRR normalizado')
ax.set_title('O encoder perdeu neste benchmark',loc='left',fontweight='bold',pad=24)
ax.legend(frameon=False,loc='upper right');ax.spines[['top','right']].set_visible(False)
fig.text(.06,.025,'30 paráfrases · corpus congelado · limiares não calibrados · chunking diferente',fontsize=10,color=NAVY)
fig.tight_layout(rect=(0,.055,1,1));fig.savefig(ROOT/'assets/busca.png',dpi=160);plt.close(fig)
d=json.loads((ROOT/'content/estabilidade_results.json').read_text());s=d['resumo']
fig,axes=plt.subplots(1,2,figsize=(12,5.6),facecolor=LIGHT)
for ax in axes:ax.set_facecolor(LIGHT);ax.spines[['top','right']].set_visible(False)
vals=list(s['escolhas'].values())
bars=axes[0].bar(['C = 0,1','C = 1'],vals,color=[LAVA,NAVY]);axes[0].bar_label(bars,padding=5)
axes[0].set_ylim(0,22);axes[0].set_ylabel('Vitórias em 30 amostras');axes[0].set_title('Modelos quase empatados',loc='left',fontweight='bold')
threshold=[r['limiar'] for r in d['amostras']]
axes[1].hist(threshold,bins=[.075,.125,.175,.225,.275,.325],color=NAVY,rwidth=.8)
axes[1].axvline(s['limiar_teorico'],color=LAVA,linestyle='--',label='Teórico: 5/35');axes[1].set_xlabel('Limiar escolhido na validação')
axes[1].set_ylabel('Amostras');axes[1].set_title('A escolha do limiar também varia',loc='left',fontweight='bold');axes[1].legend(frameon=False)
fig.text(.055,.03,'Dados sintéticos · ganho médio vs. nunca alertar: R$ 385 · IC95% bootstrap: R$ 336,50 a R$ 437,00',fontsize=10)
fig.tight_layout(rect=(0,.065,1,1));fig.savefig(ROOT/'assets/estabilidade.png',dpi=160);plt.close(fig)
print('Dois gráficos criados a partir dos relatórios.')

