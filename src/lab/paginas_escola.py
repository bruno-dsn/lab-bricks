"""Experiências da escola; dados públicos em cache, caderno só na sessão."""
import hashlib
import json
import pandas as pd
import streamlit as st
from .escola import importar_caderno, exportar_caderno, importar_feedback
from .retail_real import carregar_amostra, limpar_retail, gold_retail
from .rigor_ml import janelas_temporais, selecionar_temporal, comparar_calibracao, decidir_monitoramento
from .classificacao import gerar_entregas
from .missoes_sql import MISSOES, tabelas_missao, corrigir_missao
from .sql_seguro import ConsultaInvalida
from .engenharia_avancada import historico_scd2, simular_watermark
from .recuperacao import buscar
from .rag import responder_extrativo

PAGINAS=['Minha escola','Missões SQL','Dados públicos reais','Validação temporal','Calibração e decisão','CDC e histórico','Streaming e atrasos','RAG com evidências']

@st.cache_data(show_spinner=False)
def _retail(directory,version):
    bronze=carregar_amostra(directory);silver,rejected,replaced,counts=limpar_retail(bronze)
    return bronze,silver,rejected,replaced,counts,gold_retail(silver)


@st.cache_data(show_spinner=False)
def _temporal(seed,gap):
    frame=gerar_entregas(600,seed);_,board,final=selecionar_temporal(frame,gap=gap)
    windows,refit,test=janelas_temporais(frame,gap=gap)
    bounds=pd.DataFrame([{'janela':i+1,'treino_inicio':str(t.data.min().date()),'treino_fim':str(t.data.max().date()),'validacao_inicio':str(v.data.min().date()),'validacao_fim':str(v.data.max().date()),'linhas_treino':len(t),'linhas_validacao':len(v)} for i,(t,v) in enumerate(windows)])
    return board,final,bounds,len(refit),len(test)


@st.cache_data(show_spinner=False)
def _calibracao(seed):return comparar_calibracao(gerar_entregas(600,seed))


def render(page,root,lessons):
    by_id={a.id:a for a in lessons}
    exercises={p.stem for p in (root/'exercicios').glob('ex*.py')}
    if page=='Minha escola':
        st.title('Sua escola: uma tentativa, uma evidência, uma explicação.')
        st.write('Siga dez etapas. Use as aulas para entender, os exercícios para construir e os testes para investigar erros. As marcas e o caderno são registros pessoais.')
        stages=json.loads((root/'content/school.json').read_text())['etapas']
        if 'caderno' not in st.session_state:
            st.session_state.caderno={'format':'lab-bricks-caderno','version':1,'reflexoes':{},'exercicios':{}}
        notebook=st.session_state.caderno
        cols=st.columns(3)
        cols[0].metric('Etapas',len(stages));cols[1].metric('Reflexões registradas',len(notebook['reflexoes']))
        cols[2].metric('Exercícios com feedback aprovado',sum(f['validado'] for f in notebook['exercicios'].values()))
        selected=st.selectbox('Sua etapa',range(len(stages)),format_func=lambda i:f"{i+1:02d} · {stages[i]['titulo']}",key='escola_stage')
        stage=stages[selected]
        st.info('Entrega desta etapa: '+stage['entrega'])
        for identifier in stage['aulas']:
            lesson=by_id[identifier]
            st.write(f'**{identifier} · {lesson.titulo}**')
            if lesson.requisitos:st.caption('Revise antes: '+', '.join(lesson.requisitos))
        for name in stage['exercicios']:
            st.code(f'python scripts/corrigir.py {name}',language='bash')
        identifier=st.selectbox('Aula da reflexão',stage['aulas'],key='nota_aula')
        saved=notebook['reflexoes'].get(identifier,{'texto':'','confianca':0})
        with st.form('reflexao'):
            note=st.text_area(stage['reflexao'],saved['texto'],max_chars=2000,key=f'nota_{identifier}')
            confidence=st.slider('Consigo refazer sem consultar?',0,3,saved['confianca'])
            if st.form_submit_button('Guardar reflexão'):
                notebook['reflexoes'][identifier]={'texto':note,'confianca':confidence};st.success('Reflexão guardada nesta sessão. Exporte o caderno para conservar.')
        st.download_button('Baixar meu caderno',exportar_caderno(notebook,by_id,exercises),'lab-bricks-caderno.json','application/json')
        uploaded=st.file_uploader('Importar caderno ou feedback de exercício · até 100 KB',type=['json'],key='school_import')
        if uploaded is not None and st.button('Importar registro'):
            try:
                payload=uploaded.getvalue()
                if len(payload)>100_000:raise ValueError('Arquivo acima de 100 KB.')
                try:head=json.loads(payload)
                except (ValueError,UnicodeDecodeError,RecursionError):raise ValueError('JSON inválido.') from None
                if isinstance(head,dict) and head.get('format')=='lab-bricks-feedback':
                    value=importar_feedback(payload,exercises);notebook['exercicios'][value['exercicio']]=value
                else:st.session_state.caderno=importar_caderno(payload,by_id,exercises)
                st.success('Registro importado. O JSON é pessoal e editável; não certifica autoria.');st.rerun()
            except ValueError as error:st.warning(str(error))
        st.caption('Caderno e reflexões ficam só na sua sessão e no arquivo que você baixar. Nunca entram no cache compartilhado de dados.')
    elif page=='Missões SQL':
        st.title('Escreva a consulta e prove o grão.')
        identifier=st.selectbox('Missão',list(MISSOES),format_func=lambda x:MISSOES[x]['titulo'])
        spec=MISSOES[identifier];st.write(spec['enunciado'])
        with st.expander('Tabelas e contrato'):
            for name,frame in tabelas_missao().items():st.write(name);st.dataframe(frame,hide_index=True)
            st.write('Colunas esperadas: '+', '.join(spec['colunas']))
        with st.form('missao_sql'):
            query=st.text_area('Sua solução SQL','-- Escreva sua consulta aqui\nSELECT * FROM pedidos',height=220,max_chars=6000,key=f'missao_{identifier}')
            if st.form_submit_button('Corrigir consulta'):
                try:
                    feedback=corrigir_missao(identifier,query)
                    (st.success if feedback['ok'] else st.warning)(feedback['feedback']);st.dataframe(feedback['resultado'],hide_index=True)
                except ConsultaInvalida as error:st.warning(str(error))
        with st.expander('Referência · consulte depois de tentar'):st.code(spec['exemplo'],language='sql')
        st.caption('Execução de leitura no SQLite; não executa Python nem instala pacotes a partir da interface.')
    elif page=='Dados públicos reais':
        st.title('Da fonte pública à conta que fecha.')
        version=hashlib.sha256((root/'data/online_retail_amostra.csv').read_bytes()).hexdigest()
        bronze,silver,rejected,replaced,counts,gold=_retail(str(root/'data'),version)
        for col,(label,value) in zip(st.columns(4),counts.items()):col.metric(label,value)
        st.info('3.000 = Silver + rejeitadas + substituídas. Valores em GBP; CustomerID removido. Esta amostra cobre um dia e não serve para inferir sazonalidade.')
        choice=st.selectbox('Etapa real',['Bronze','Silver','Rejeitadas','Substituídas','Gold'])
        frame={'Bronze':bronze,'Silver':silver,'Rejeitadas':rejected,'Substituídas':replaced,'Gold':gold}[choice]
        st.dataframe(frame.head(200),hide_index=True);st.caption('Exibição limitada a 200 linhas.')
        st.download_button('Baixar etapa pública',frame.to_csv(index=False).encode(),'retail-etapa.csv','text/csv')
        meta=json.loads((root/'data/online_retail_meta.json').read_text())
        st.write('Fonte: Daqing Chen, UCI Online Retail, 2015. Licença CC BY 4.0; DOI 10.24432/C5BW33.');st.link_button('Proveniência oficial',meta['fonte'])
        st.code('python scripts/corrigir.py ex08_retail',language='bash')
    elif page=='Validação temporal':
        st.title('Escolha antes de ver o futuro.')
        seed=int(st.number_input('Semente temporal',0,1000,42));gap=st.slider('Gap em datas observadas',1,5,1)
        board,final,bounds,refit,test=_temporal(seed,gap)
        st.dataframe(bounds,hide_index=True);st.write('Refit purgado:',refit,'linhas; teste final:',test,'linhas.')
        st.dataframe(board.head(8),hide_index=True);st.json(final)
        st.caption('C e limiar vêm apenas das validações. O teste final mede a escolha congelada. Gap cobre um horizonte de uma data observada neste caso sintético.')
        st.code('python scripts/corrigir.py ex09_janelas',language='bash')
    elif page=='Calibração e decisão':
        st.title('Probabilidade, custo e uma ação explicada.')
        seed=int(st.number_input('Semente da calibração',0,1000,42));results,curves=_calibracao(seed)
        st.dataframe(results,hide_index=True)
        plot=pd.concat([f.assign(modelo=k) for k,f in curves.items()],ignore_index=True)
        st.scatter_chart(plot,x='probabilidade_media',y='frequencia_observada',color='modelo')
        st.dataframe(plot,hide_index=True);st.caption('Suporte n importa. Calibração não garante melhoria; o limiar teórico 5/35 exige probabilidades calibradas e custos coerentes.')
        st.subheader('Qual decisão o monitoramento provoca?')
        psi=st.slider('PSI observado',0.,1.,.1,.01);prior=st.slider('Brier de referência',0.,1.,.15,.01);now=st.slider('Brier atual',0.,1.,.16,.01)
        labels=int(st.number_input('Rótulos maduros',0,10000,120));st.info(decidir_monitoramento(psi,prior,now,labels))
        st.caption('Limites 80 / 0,2 / 0,02 são exemplos didáticos; adaptar ao negócio. Promoção de candidato exige revisão.')
    elif page=='CDC e histórico':
        st.title('Uma alteração não deve apagar a história.')
        events=[{'evento_id':'e1','chave':'cliente-A','instante':'2026-01-01','operacao':'upsert','valor':'Norte'},{'evento_id':'e2','chave':'cliente-A','instante':'2026-01-03','operacao':'upsert','valor':'Sul'}]
        if st.toggle('Incluir delete e reinserção',True):events.extend([{'evento_id':'e3','chave':'cliente-A','instante':'2026-01-05','operacao':'delete','valor':None},{'evento_id':'e4','chave':'cliente-A','instante':'2026-01-07','operacao':'upsert','valor':'Leste'}])
        if st.toggle('Repetir o mesmo evento',True):events.append(events[0].copy())
        history,audit=historico_scd2(events);st.dataframe(history,hide_index=True);st.dataframe(audit,hide_index=True)
        st.caption('Referência reconstrói o log completo, até 1.000 eventos. Intervalos [início,fim); MERGE Delta do notebook precisa de execução real registrada.')
    elif page=='Streaming e atrasos':
        st.title('Observe o evento e a fronteira do lote anterior.')
        delay=st.slider('Tolerância de atraso em minutos',1,30,10)
        def event(key,time,value):return {'evento_id':key,'instante':f'2026-01-01T{time}:00Z','valor':value}
        batches=[[event('a','10:02',10),event('b','10:20',20)],[event('c','10:15',15),event('d','10:02',99),event('e','10:30',30)],[]]
        if st.toggle('Repetir ID já recebido',True):batches[1].append(batches[0][1].copy())
        audit,windows=simular_watermark(batches,delay);st.dataframe(audit,hide_index=True);st.dataframe(windows,hide_index=True)
        st.warning('Simplificação por timestamp individual. O Spark pode descartar pelo fim da janela e pelo operador; IDs locais não reproduzem toda expulsão de estado nativa.')
    elif page=='RAG com evidências':
        st.title('Responda com evidência ou reconheça a falta dela.')
        docs=json.loads((root/'content/benchmark_corpus.json').read_text())
        with st.form('rag_form'):
            question=st.text_input('Sua pergunta','Como repetir um lote sem duplicar dados?',max_chars=500)
            threshold=st.slider('Similaridade mínima para extrair',0.,.3,.12,.01)
            if st.form_submit_button('Recuperar e responder'):
                try:
                    evidence=buscar(question,docs,3);answer=responder_extrativo(question,evidence,threshold)
                    st.text(answer['resposta']);st.write('Citações:',answer['citacoes']);st.caption('Resposta extrativa: sem LLM, sem API externa e sem ferramentas.')
                except ValueError as error:st.warning(str(error))
        report=root/'content/rag_results.json'
        if report.exists():
            value=json.loads(report.read_text());st.subheader('Experimento local de geração, separado da resposta extrativa')
            st.json(value['resumo']);st.caption('Contrato aceito não prova suporte factual. Revisão independente das afirmações permanece pendente.')
            with st.expander('Saídas e latências'):st.dataframe(pd.DataFrame(value['casos']),hide_index=True)
        else:st.info('O avaliador de geração opcional ainda precisa ser executado nesta cópia.')
