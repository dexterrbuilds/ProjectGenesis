"""Read-only source workbook extraction, preserving cell provenance and missingness."""
from common import *
import zipfile,xml.etree.ElementTree as ET,gzip,collections,re,math
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def colnum(ref):
 n=0
 for c in re.match('[A-Z]+',ref).group():n=n*26+ord(c)-64
 return n
def extract(path):
 with zipfile.ZipFile(path) as z:
  assert z.testzip() is None
  ss=[]
  if 'xl/sharedStrings.xml' in z.namelist():
   for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',NS):ss.append(''.join(t.text or '' for t in si.findall('.//m:t',NS)))
  sheets=[]
  for name in sorted(z.namelist()):
   if not re.fullmatch(r'xl/worksheets/sheet\d+\.xml',name):continue
   root=ET.fromstring(z.read(name));cells=[];formatted_empty=0
   for c in root.findall('.//m:sheetData/m:row/m:c',NS):
    v=c.find('m:v',NS);inline=c.find('m:is',NS);f=c.find('m:f',NS);typ=c.get('t','n')
    if v is None and inline is None and f is None:formatted_empty+=1;continue
    raw=v.text if v is not None else None
    if typ=='s':val=ss[int(raw)] if raw is not None else None
    elif typ=='inlineStr':val=''.join(t.text or '' for t in inline.findall('.//m:t',NS)) if inline is not None else None
    elif typ in ['str','e','b']:val=raw
    else:
     try:val=float(raw) if raw is not None else None
     except ValueError:val=raw
    cells.append({'ref':c.attrib['r'],'value':val,'source_value_text':raw,'formula':f.text if f is not None else None,'type':typ})
   sheets.append({'xml_sheet':name,'declared_dimension':root.find('m:dimension',NS).get('ref'),'cells':cells,'formatted_empty_cells':formatted_empty})
  return sheets
def main():
 sources=[];inventory=[]
 for u in load(HERE/'SOURCE_URL_INVENTORY.json'):
  p=HERE/'sources'/u.rsplit('/',1)[1];sheets=extract(p);sources.append({'url':u,'path':str(p.relative_to(HERE)),'sha256':sha(p),'bytes':p.stat().st_size,'zip_crc_verified':True})
  target=HERE/'processed'/f'{p.stem}.json.gz';target.parent.mkdir(exist_ok=True)
  with gzip.GzipFile(filename=str(target),mode='wb',mtime=0) as f:f.write(json.dumps(sheets,ensure_ascii=False,allow_nan=False).encode())
  summary=[]
  for s in sheets:
   cols=collections.defaultdict(list)
   for c in s['cells']:cols[re.match('[A-Z]+',c['ref']).group()].append(c)
   cc=[]
   for col,values in sorted(cols.items(),key=lambda kv:colnum(kv[0])):
    nums=[c for c in values if isinstance(c['value'],(int,float))];texts=[c for c in values if isinstance(c['value'],str)]
    cc.append({'column':col,'numeric_cells':len(nums),'first_numeric_ref':nums[0]['ref'] if nums else None,'last_numeric_ref':nums[-1]['ref'] if nums else None,'labels':[{'ref':c['ref'],'text':c['value']} for c in texts[:12]],'formula_count':sum(c['formula'] is not None for c in values)})
   summary.append({'xml_sheet':s['xml_sheet'],'declared_dimension':s['declared_dimension'],'actual_populated_cells':len(s['cells']),'formatted_empty_cells':s['formatted_empty_cells'],'columns':cc})
  inventory.append({'file':p.name,'sha256':sha(p),'processed_path':str(target.relative_to(HERE)),'processed_sha256':sha(target),'sheets':summary})
 write('SOURCE_MANIFEST.json',{'article':{'url':'https://elifesciences.org/articles/85756','sha256':sha(HERE/'sources/article.html')},'workbooks':sources,'acquired_at_utc':now(),'originals_unchanged':True})
 write('WORKBOOK_INVENTORY.json',inventory)
 print(json.dumps({'workbooks':len(sources),'bytes':sum(s['bytes'] for s in sources),'populated_cells':sum(s['actual_populated_cells'] for w in inventory for s in w['sheets'])}))
if __name__=='__main__':main()
