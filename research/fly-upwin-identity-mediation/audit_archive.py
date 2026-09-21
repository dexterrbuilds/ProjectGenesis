"""Inspect publisher ZIP byte ranges; verify each extracted member against ZIP CRC.
No reconstruction of missing bytes or experimental observations.
"""
from common import *
import struct,zlib,zipfile,io,xml.etree.ElementTree as ET

src=HERE/'sources'
old=src/'elife-85756-supp-v1.zip'
prefix=src/'archive-prefix.partial.bin'
if old.exists():old.rename(prefix)
ranges=[(0,prefix.read_bytes()),(103000000,(src/'archive-data-range.bin').read_bytes())]
a=load(HERE/'ARCHIVE_DIRECTORY.json'); rows=[]
for m in a['members']:
 if not (m['name'].endswith('.xlsx') or m['name'].endswith('.docx') or m['name'].endswith('.pdf')):continue
 for start,data in ranges:
  off=m['local_offset']-start
  if off<0 or off+30>len(data):continue
  h=struct.unpack_from('<4s5H3L2H',data,off)
  assert h[0]==b'PK\x03\x04'
  p=off+30+h[-2]+h[-1];end=p+m['compressed_bytes']
  if end>len(data):continue
  raw=data[p:end];raw=zlib.decompress(raw,-15) if m['compression']==8 else raw
  assert len(raw)==m['bytes'] and hex(zlib.crc32(raw))==m['crc32']
  dest=src/'accepted-manuscript'/m['name'];dest.parent.mkdir(exist_ok=True);dest.write_bytes(raw)
  row=dict(name=m['name'],path=str(dest.relative_to(HERE)),bytes=len(raw),sha256=sha(dest),crc_verified=True)
  if m['name'].endswith('.xlsx'):
   suffix=m['name'].replace('elife_poa_e85756_','').replace('Figure_','fig').replace('_figure_supplement_','-figsupp').replace('_source_data_','-data').replace('.xlsx','-v3.xlsx')
   counterpart=PRIOR/'sources'/('elife-85756-'+suffix)
   row['final_counterpart']=str(counterpart.relative_to(ROOT))
   row['identical_to_final']=counterpart.exists() and sha(counterpart)==sha(dest)
   with zipfile.ZipFile(io.BytesIO(raw)) as z:
    row['internal_members']=z.namelist()
    row['morphology_or_acquisition_parts']=[n for n in z.namelist() if any(k in n.lower() for k in ['media/','comments','customxml','embedding'])]
  if m['name'].endswith('.docx'):
   with zipfile.ZipFile(io.BytesIO(raw)) as z:
    root=ET.fromstring(z.read('word/document.xml'));text='\n'.join(e.text for e in root.iter() if e.tag.endswith('}t') and e.text)
   (HERE/'KEY_RESOURCES_TEXT.txt').write_text(text)
  rows.append(row);break
write('ARCHIVE_AUDIT.json',dict(url=a['archive_url'],total_bytes=a['total_bytes'],directory_members=len(a['members']),
 acquisition='Whole-archive request timed out after 180 s. Original prefix retained; independent HTTP 206 data range and tail retained. Every extracted member verified against original central-directory size/CRC.',
 retrieved_ranges=[dict(start=s,end=s+len(d)-1,bytes=len(d)) for s,d in ranges],
 original_archive_complete=False, extracted=rows,unretrieved=[m['name'] for m in a['members'] if m['name'] not in {r['name'] for r in rows}],
 note='Videos and large TIFF not required for cell identity linkage were not extracted; no claim of raw tracking from videos. Archive filenames contain no extra trial archive, ROI, event log, cell-identity table, or analysis script.'))
print(json.dumps(dict(extracted=len(rows),workbooks=sum(r['name'].endswith('.xlsx') for r in rows),identical_workbooks=sum(r.get('identical_to_final',False) for r in rows)),indent=2))
