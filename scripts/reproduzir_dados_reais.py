"""Reproduz 3.000 linhas públicas, sem CustomerID, a partir do XLSX original."""
from pathlib import Path
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import argparse, csv, hashlib, io, json, urllib.request, zipfile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://archive.ics.uci.edu/static/public/352/online+retail.zip'
SHA = 'f5385cbb54bbebf7196389109c6b0621faab0c304e3702548165e71c84aede8b'
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
FIELDS = ['linha_fonte','fatura','produto','descricao','quantidade','data','preco_gbp','pais']


def reproduzir(archive):
    raw = Path(archive).read_bytes()
    if len(raw) > 30_000_000 or hashlib.sha256(raw).hexdigest() != SHA:
        raise ValueError('Arquivo fonte diverge da versão pública registrada.')
    with zipfile.ZipFile(io.BytesIO(raw)) as outer:
        name = next(n for n in outer.namelist() if n.endswith('.xlsx'))
        if outer.getinfo(name).file_size > 40_000_000:
            raise ValueError('XLSX acima do limite.')
        xlsx = outer.read(name)
    rows=[]
    with zipfile.ZipFile(io.BytesIO(xlsx)) as book:
        shared=[]
        with book.open('xl/sharedStrings.xml') as stream:
            for _, element in ET.iterparse(stream, events=['end']):
                if element.tag == NS+'si':
                    shared.append(''.join(t.text or '' for t in element.iter(NS+'t')));element.clear()
        with book.open('xl/worksheets/sheet1.xml') as stream:
            for _, element in ET.iterparse(stream, events=['end']):
                if element.tag != NS+'row':continue
                if element.attrib['r']=='1':element.clear();continue
                values={}
                for cell in element.findall(NS+'c'):
                    key=''.join(c for c in cell.attrib['r'] if c.isalpha())
                    node=cell.find(NS+'v'); value=node.text if node is not None else ''
                    if cell.attrib.get('t')=='s':value=shared[int(value)]
                    values[key]=value
                date=''
                if values.get('E'):
                    seconds=int((Decimal(values['E'])*86400).to_integral_value())
                    date=(datetime(1899,12,30)+timedelta(seconds=seconds)).isoformat(sep=' ',timespec='seconds')
                rows.append(dict(zip(FIELDS,[element.attrib['r'],values.get('A',''),values.get('B',''),values.get('C',''),values.get('D',''),date,values.get('F',''),values.get('H','')])))
                element.clear()
                if len(rows)==3000:break
    if len(rows)!=3000:raise ValueError('Fonte incompleta.')
    path=ROOT/'data/online_retail_amostra.csv'
    with path.open('w',newline='',encoding='utf-8') as out:
        writer=csv.DictWriter(out,fieldnames=FIELDS,lineterminator='\n');writer.writeheader();writer.writerows(rows)
    meta={'dataset':'Online Retail','autor':'Daqing Chen','ano':2015,'doi':'10.24432/C5BW33',
          'fonte':URL,'fonte_sha256':SHA,'licenca':'CC BY 4.0','licenca_url':'https://creativecommons.org/licenses/by/4.0/',
          'amostra_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'linhas':len(rows),'moeda':'GBP',
          'mudancas':['Primeiras 3.000 linhas de dados, na ordem original','CustomerID removido','Cabeçalhos em português','Datas seriais Excel convertidas para texto sem inventar fuso horário','Sem defeitos artificiais adicionados'],
          'gerado_em':datetime.now(timezone.utc).isoformat()}
    (ROOT/'data/online_retail_meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(meta,ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--archive',type=Path)
    args=parser.parse_args()
    if args.archive:reproduzir(args.archive)
    else:
        target=ROOT.parent/'online-retail-fonte.zip';partial=target.with_suffix('.part')
        try:
            with urllib.request.urlopen(URL,timeout=30) as response,partial.open('wb') as out:
                total=0
                while chunk:=response.read(1024*1024):
                    total+=len(chunk)
                    if total>30_000_000:raise ValueError('Fonte acima do limite.')
                    out.write(chunk)
            partial.replace(target);reproduzir(target)
        finally:partial.unlink(missing_ok=True)
