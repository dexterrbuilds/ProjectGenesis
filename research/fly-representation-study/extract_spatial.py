"""Descriptive independent spatial observations; no fit or parameter transfer."""
import hashlib,json
from pathlib import Path
import openpyxl
H=Path(__file__).resolve().parent
def main():
 p=H.parent/'fly-physiology-study/data/amin-fig7.xlsx';s=openpyxl.load_workbook(p,read_only=True,data_only=True)['Fig 7']
 out=[]
 # Bottom panels contain C/H/V measurements for each recording.
 # Preserve all three stimulus sites and both APL response/KC inhibition modalities.
 for letter,start,stop,stim in [('A',261,274,'H'),('B',277,290,'V'),('C',293,303,'C')]:
  for panel,cols,modality in [(1,[1,2,3],'APL calcium'),(4,[10,11,12],'normalized inhibition of odor-evoked KC calcium')]:
   rows=[]
   for row in range(start,stop+1):
    v=[s.cell(row,c).value for c in cols]
    if all(x is None for x in v):continue
    assert all(isinstance(x,(int,float)) for x in v),(letter,panel,row,v)
    rows.append({'source_row':row,'C':v[0],'H':v[1],'V':v[2]})
   means={k:sum(r[k] for r in rows)/len(rows) for k in ['C','H','V']}
   out.append({'panel':f'{letter}{panel}','stimulated_region':stim,'modality':modality,'n_recordings':len(rows),'rows':rows,'regional_mean':means,
    'interpretation':'Within-assay normalized fluorescence; not conductance. Recordings across modalities not assumed paired.'})
 dest=H/'data/apl-figure7-descriptive.json';assert not dest.exists()
 dest.write_text(json.dumps({'source':'https://cdn.elifesciences.org/articles/56954/elife-56954-fig7-data1-v2.xlsx',
  'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'license':'CC-BY 4.0, Amin et al. 2020',
  'selection':'all A/B/C stimulus sites, column1 APL calcium and column4 KC inhibition, bottom panels; no fitting, no row exclusions','panels':out},indent=2)+'\n')
 print(json.dumps([{k:v for k,v in x.items() if k!='rows'} for x in out],indent=2))
if __name__=='__main__':main()
