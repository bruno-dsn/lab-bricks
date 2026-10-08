"""Recria a identidade original Lab Bricks, gráficos e o CSV sintético."""
from pathlib import Path
import csv
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from lab.dados import gerar_vendas, COLUNAS
from lab.pipeline import tratar
from lab.ml import comparar
from lab.classificacao import avaliar_entregas

ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
LAVA, NAVY, OAT, LIGHT = '#FF3621', '#0B2026', '#EEEDE9', '#F9F7F4'

(ASSETS/'logo.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 96" role="img" aria-labelledby="t d">
<title id="t">Lab Bricks</title><desc id="d">Marca original: quatro módulos quadrados e o nome Lab Bricks.</desc>
<rect x="3" y="12" width="31" height="31" rx="6" fill="#FF3621"/>
<rect x="41" y="12" width="31" height="31" rx="6" fill="#0B2026"/>
<rect x="3" y="50" width="31" height="31" rx="6" fill="#0B2026"/>
<rect x="41" y="50" width="31" height="31" rx="6" fill="#FF3621"/>
<text x="91" y="64" font-family="Arial,sans-serif" font-size="47" font-weight="700" letter-spacing="-2" fill="#0B2026">Lab Bricks</text></svg>''')

(ASSETS/'capa.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 610" role="img" aria-labelledby="t d">
<title id="t">Lab Bricks: seu laboratório de dados</title><desc id="d">Seis trilhas de estudo: fundamentos, SQL e BI, engenharia, ML, IA e governança. Quarenta e cinco aulas, dez etapas e quatorze exercícios próprios.</desc>
<rect width="1440" height="610" rx="26" fill="#0B2026"/>
<g stroke="#27424A" stroke-width="1" opacity=".65"><path d="M855 0V610M1010 0V610M1165 0V610M1320 0V610M800 110H1440M800 265H1440M800 420H1440M800 575H1440"/></g>
<g font-family="Arial,sans-serif">
<rect x="64" y="60" width="31" height="31" rx="6" fill="#FF3621"/><rect x="104" y="60" width="31" height="31" rx="6" fill="#F9F7F4"/>
<rect x="64" y="100" width="31" height="31" rx="6" fill="#F9F7F4"/><rect x="104" y="100" width="31" height="31" rx="6" fill="#FF3621"/>
<text x="163" y="92" fill="#F9F7F4" font-size="18" letter-spacing="3">ESTUDE. EXPERIMENTE.</text>
<text x="163" y="124" fill="#F9F7F4" font-size="18" letter-spacing="3">EXPLIQUE SUAS DECISÕES.</text>
<text x="60" y="254" fill="#FFFFFF" font-size="100" font-weight="700" letter-spacing="-5">Lab Bricks</text>
<text x="64" y="315" fill="#FF3621" font-size="28" font-weight="700">Do fundamento à evidência.</text>
<text x="64" y="374" fill="#EEEDE9" font-size="24">Um laboratório forte para aprender Databricks.</text>
<text x="64" y="412" fill="#EEEDE9" font-size="22">Conteúdo próprio. Prática guiada. Espaço para evoluir.</text>
<text x="64" y="500" fill="#FFFFFF" font-size="22" font-weight="700">45 aulas · 17 notebooks · 14 exercícios · 3 projetos</text>
<text x="64" y="552" fill="#EEEDE9" font-size="15" letter-spacing="1">BRUNO NUNES · PORTUGUÊS · DADOS SINTÉTICOS E PÚBLICOS · v3.0</text>
<g transform="translate(875 105)"><rect width="220" height="130" rx="16" fill="#F9F7F4"/>
<text x="22" y="40" fill="#FF3621" font-size="15" font-weight="700">01 / 02</text><text x="22" y="80" fill="#0B2026" font-size="25" font-weight="700">Fundamentos</text><text x="22" y="112" fill="#0B2026" font-size="21">SQL e BI</text></g>
<g transform="translate(1120 180)"><rect width="220" height="130" rx="16" fill="#FF3621"/>
<text x="22" y="40" fill="#FFFFFF" font-size="15" font-weight="700">03 / 04</text><text x="22" y="80" fill="#FFFFFF" font-size="25" font-weight="700">Engenharia</text><text x="22" y="112" fill="#FFFFFF" font-size="21">ML e MLOps</text></g>
<g transform="translate(875 340)"><rect width="220" height="130" rx="16" fill="#F9F7F4"/>
<text x="22" y="40" fill="#FF3621" font-size="15" font-weight="700">05 / 06</text><text x="22" y="80" fill="#0B2026" font-size="25" font-weight="700">IA e evidências</text><text x="22" y="112" fill="#0B2026" font-size="21">Governança</text></g>
</g></svg>''')

(ASSETS/'arquitetura.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 840" role="img" aria-labelledby="t d">
<title id="t">Lab Bricks: um destino explicado para cada registro</title><desc id="d">727 entradas: 720 pedidos vigentes na Silver, seis inválidos e uma versão substituída. Gold agrega somente concluídos.</desc>
<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#0B2026"/></marker></defs>
<rect width="1440" height="840" rx="22" fill="#F9F7F4"/>
<g font-family="Arial,sans-serif" fill="#0B2026">
<text x="55" y="65" font-size="18" letter-spacing="2" fill="#B82718">LAB BRICKS / QUALIDADE OBSERVÁVEL</text>
<text x="55" y="118" font-size="39" font-weight="700">Um destino explicado para cada registro.</text>
<rect x="485" y="166" width="470" height="92" rx="15" fill="#0B2026"/>
<text x="510" y="203" font-size="23" font-weight="700" fill="#FFFFFF">BRONZE · 727</text><text x="510" y="237" font-size="20" fill="#EEEDE9">Fonte preservada como chegou</text>
<path d="M720 266V308" stroke="#0B2026" stroke-width="3" marker-end="url(#a)"/>
<rect x="420" y="320" width="600" height="92" rx="15" fill="#EEEDE9" stroke="#FF3621" stroke-width="2"/>
<text x="447" y="356" font-size="23" font-weight="700">ESCOLHER VERSÃO → VALIDAR</text><text x="447" y="389" font-size="20">Chave · atualização · contrato de dados</text>
<g fill="none" stroke="#0B2026" stroke-width="3" marker-end="url(#a)"><path d="M490 420V451H260V478"/><path d="M720 420V478"/><path d="M950 420V451H1180V478"/></g>
<rect x="65" y="491" width="390" height="110" rx="15" fill="#FFFFFF" stroke="#0B2026"/><text x="89" y="530" font-size="25" font-weight="700">SILVER · 720</text><text x="89" y="571" font-size="19">Pedidos vigentes e válidos</text>
<rect x="525" y="491" width="390" height="110" rx="15" fill="#FFFFFF" stroke="#FF3621" stroke-width="2"/><text x="549" y="530" font-size="25" font-weight="700" fill="#B82718">QUARENTENA · 6</text><text x="549" y="571" font-size="19">Fonte e motivo de rejeição</text>
<rect x="985" y="491" width="390" height="110" rx="15" fill="#FFFFFF" stroke="#0B2026"/><text x="1009" y="530" font-size="25" font-weight="700">SUBSTITUÍDAS · 1</text><text x="1009" y="571" font-size="19">Versão anterior preservada</text>
<path d="M260 609V656" fill="none" stroke="#0B2026" stroke-width="3" marker-end="url(#a)"/>
<rect x="65" y="668" width="390" height="110" rx="15" fill="#0B2026"/><text x="89" y="707" font-size="25" font-weight="700" fill="#FFFFFF">GOLD · POR DIA</text><text x="89" y="741" font-size="19" fill="#EEEDE9">Receita de concluídos</text><text x="89" y="765" font-size="16" fill="#EEEDE9">Cancelados ficam fora da receita</text>
<text x="525" y="706" font-size="36" font-weight="700">727 = 720 + 6 + 1</text><text x="525" y="747" font-size="21">App: Pandas · Notebooks: Spark e Delta</text><text x="525" y="779" font-size="17">Fixture padrão: 720 pedidos · semente 42 · erros ativados</text>
</g></svg>''')

rows=gerar_vendas()
with (ROOT/'data/vendas_sinteticas.csv').open('w', newline='') as file:
    writer=csv.DictWriter(file,fieldnames=COLUNAS)
    writer.writeheader();writer.writerows(rows)
predictions, info=comparar(tratar(rows).gold)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'text.color':NAVY,'axes.labelcolor':NAVY,'xtick.color':NAVY,'ytick.color':NAVY})
fig,ax=plt.subplots(figsize=(13,6.2),facecolor=LIGHT)
ax.set_facecolor(LIGHT)
for column,label,color,style in [('real','Receita observada',NAVY,'-'),('baseline','Baseline: ontem','#9B978F','--'),('baseline_semanal','Baseline: semana passada','#C9A227','--'),('baseline_media','Baseline: média do treino','#2E8B8B',':'),('modelo','Modelo Ridge',LAVA,'-')]:
    ax.plot(predictions.index,predictions[column],label=label,color=color,linewidth=2.3,linestyle=style,marker='o',markersize=4)
ax.grid(axis='y',color='#D5D4CF',alpha=.8)
for spine in ax.spines.values():spine.set_visible(False)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{x:,.0f}'.replace(',','.')))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
ax.set_ylabel('Receita fictícia (R$)',labelpad=14)
ax.set_xlabel('Março de 2026 · previsão de um dia à frente',labelpad=12)
ax.legend(loc='upper left',bbox_to_anchor=(0,1.18),ncol=3,frameon=False,fontsize=10)
fig.text(.075,.94,'Toda melhoria precisa enfrentar uma baseline.',fontsize=23,fontweight='bold')
fig.text(.075,.885,f"MAE ontem: R$ {info['mae_baseline']:.2f} | MAE semana passada: R$ {info['mae_baseline_semanal']:.2f} | MAE média: R$ {info['mae_baseline_media']:.2f} | MAE Ridge: R$ {info['mae_modelo']:.2f} | 14 dias de teste",fontsize=11,parse_math=False)
fig.subplots_adjust(left=.09,right=.97,top=.72,bottom=.17)
fig.savefig(ASSETS/'experimento.png',dpi=150,facecolor=LIGHT)
plt.close(fig)
_,metrics,_=avaliar_entregas()
fig,ax=plt.subplots(figsize=(8,5),facecolor=LIGHT)
ax.set_facecolor(LIGHT)
names=['Verdadeiros\nnegativos','Falsos\npositivos','Falsos\nnegativos','Verdadeiros\npositivos']
values=[metrics[k] for k in ['tn','fp','fn','tp']]
bars=ax.bar(names,values,color=[NAVY,LAVA,LAVA,NAVY],width=.65)
ax.bar_label(bars,padding=4)
ax.spines[['top','right']].set_visible(False)
ax.set_ylabel('Entregas fictícias no teste')
ax.set_title('O custo depende do tipo de erro',fontweight='bold',pad=20)
fig.text(.13,.02,'Fixture: 600 entregas · semente 42 · limiar 0,5',fontsize=10)
fig.tight_layout(rect=(0,.06,1,1))
fig.savefig(ASSETS/'classificacao.png',dpi=150,facecolor=LIGHT)
plt.close(fig)
print('Marca original, capa, arquitetura, dois gráficos e CSV gerados.')
