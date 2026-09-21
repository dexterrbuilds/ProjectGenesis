"""Descriptive measurements; no physiological parameter, decoder or model fitted."""
from common import *
import gzip,numpy as np,re,collections

def cells(stem):return json.loads(gzip.decompress((HERE/'processed'/f'elife-85756-{stem}-v3.json.gz').read_bytes()))[0]['cells']
def table(stem):return {c['ref']:c['value'] for c in cells(stem)}
def cols(stem):
 d=collections.defaultdict(list)
 for c in cells(stem):d[re.match('[A-Z]+',c['ref']).group()].append(c)
 return d
def numbers(cs):return [c['value'] for c in cs if isinstance(c['value'],(float,int))]
def summary(v):return {'n_source_rows':len(v),'mean':float(np.mean(v)),'sample_sem':float(np.std(v,ddof=1)/np.sqrt(len(v))) if len(v)>1 else None,'min':min(v),'max':max(v)}
def main():
 condition=[]
 for stem,n,paired in [('fig5-data3',6,'OCT'),('fig5-figsupp2-data3',5,'MCH')]:
  t=table(stem);measures={};rs=list(range(5,5+n));obs=[]
  for col in ['B','C','E','F']:
   v=[t[f'{col}{r}'] for r in rs];s=summary(v);s.update({'source_range':f'{col}5:{col}{4+n}','reported_mean':t[f'{col}3'],'reported_sem':t[f'{col}4'],'mean_error':float(np.mean(v)-t[f'{col}3']),'sem_error':float(np.std(v,ddof=1)/np.sqrt(n)-t[f'{col}4'])});measures[col]=s
  for r in rs:obs.append({'source_row':r,'source_label':t[f'A{r}'],'animal_id':None,'recording_id':None,'OCT_pre_mV':t[f'B{r}'],'OCT_post_mV':t[f'C{r}'],'MCH_pre_mV':t[f'E{r}'],'MCH_post_mV':t[f'F{r}']})
  effects={odor:summary([t[f'{post}{r}']-t[f'{pre}{r}'] for r in rs]) for odor,pre,post in [('OCT','B','C'),('MCH','E','F')]}
  condition.append({'file':f'elife-85756-{stem}-v3.xlsx','paired_odor':paired,'unit':'baseline-subtracted membrane potential mV','window':'mean 0–1.2 s after odor onset (article Methods)','repeated_measures':'Four values paired within source row only; no cross-workbook fly joins','groups':measures,'observations':obs,'post_minus_pre':effects})
 traces=[]
 for stem,gray,response,sourcecolor,papercolor,animals in [('fig4-data1',list('BCDEFGHI'),list('KLM'),'Green','orange',7),('fig4-data2',list('BCDEFGHIJKLMN'),list('PQRS'),'Orange','green',12)]:
  d=cols(stem);t=np.array(numbers(d['A']))*1e-4;rows=[]
  for col in gray+response:
   v=numbers(d[col]);rows.append({'column':col,'source_label':[c['value'] for c in d[col] if isinstance(c['value'],str)],'source_group':'Gray' if col in gray else sourcecolor,'paper_responder':col in response,'animal_id':None,'cell_id':None,'n_samples':len(v),'min_mV_full_trace':min(v),'max_mV_full_trace':max(v),'mean_mV_full_trace':float(np.mean(v)),'numeric_sha256':hashlib.sha256(np.array(v,dtype='<f8').tobytes()).hexdigest()})
  traces.append({'file':f'elife-85756-{stem}-v3.xlsx','paper_animals':animals,'paper_neurons':len(rows),'responders':len(response),'nonresponders':len(gray),'source_group_color':sourcecolor,'caption_color':papercolor,'color_discrepancy_unresolved':True,'time_seconds_first':float(t[0]),'time_seconds_last':float(t[-1]),'sample_interval_seconds':float(np.median(np.diff(t))),'onset_from_workbook':None,'baseline_window_from_workbook':None,'units':'baseline-subtracted membrane potential mV','response_metric_not_inferred_from_trace_extrema':True,'traces':rows})
 # Check only exact array duplication, not a claim of biological independence when different.
 duplicates=[]
 for a,b in [('fig5-data1','fig5-figsupp2-data1'),('fig5-data2','fig5-figsupp2-data2')]:
  ca,cb=cols(a),cols(b);checks=[]
  for col in ca:
   va=np.array(numbers(ca[col]),dtype='<f8');vb=np.array(numbers(cb.get(col,[])),dtype='<f8')
   if len(va):checks.append({'column':col,'n_a':len(va),'n_b':len(vb),'identical_numeric_values':bool(np.array_equal(va,vb)),'sha256_a':hashlib.sha256(va.tobytes()).hexdigest(),'sha256_b':hashlib.sha256(vb.tobytes()).hexdigest()})
  duplicates.append({'a':a,'b':b,'columns':checks})
 # Summary-only observation grids; do not reconstruct individual animals from SEM.
 grids=[]
 for stem in ['fig4-data3','fig4-figsupp1-data1','fig5-data2','fig5-figsupp2-data2']:
  d=cols(stem);t=np.array(numbers(d['A']));scale=1e-4 if stem.startswith('fig5') else 1;dt=np.diff(t)*scale
  grids.append({'file':stem,'samples':len(t),'time_first_seconds':float(t[0]*scale),'time_last_seconds':float(t[-1]*scale),'median_interval_seconds':float(np.median(dt)),'individual_trials_present':False,'individual_animal_traces_present':False,'means_reconstructable':False})
 # Source scalar behavior values retain source locators, not fictitious animal/trial identity.
 behavior=[]
 for stem,firstrow in [('fig6-data1',3),('fig6-data2',3),('fig6-data3',3),('fig6-data6',2),('fig6-data7',3),('fig7-data1',3),('fig7-data3',3),('fig7-data5',2)]:
  d=cols(stem);groups=[]
  for col,cs in d.items():
   if col=='A':continue
   vals=[c for c in cs if isinstance(c['value'],(int,float)) and int(re.search(r'\d+',c['ref']).group())>=firstrow]
   if vals:groups.append({'column':col,'labels':[{'ref':c['ref'],'value':c['value']} for c in cs if isinstance(c['value'],str)],'descriptive':summary([c['value'] for c in vals]),'source_values':[{'ref':c['ref'],'value':c['value']} for c in vals],'biological_unit_id':None})
  behavior.append({'file':f'elife-85756-{stem}-v3.xlsx','groups':groups,'independence':'source row count; not unique fly count; no cross-group pairing inferred'})
 # Movie-level metadata actually available, but no tracked animal identity or raw XY streams.
 movies=[]
 for stem in ['fig2-figsupp1-data1','fig7-figsupp1-data1']:
  t=table(stem);rows=sorted({int(re.search(r'\d+',r).group()) for r in t if r.startswith('H') and re.fullmatch(r'\d{8}T\d{6}',str(t[r]))});records=[]
  for r in rows:records.append({'source_row':r,'data_type':t.get(f'A{r}'),'female_parent_label':t.get(f'B{r}'),'male_parent_label':t.get(f'C{r}'),'protocol':t.get(f'D{r}'),'movie_field':t.get(f'E{r}'),'arena':t.get(f'F{r}'),'camera':t.get(f'G{r}'),'timestamp_label':t.get(f'H{r}'),'n_source':t.get(f'I{r}'),'animal_id':None})
  keys={(r['arena'],r['camera'],r['timestamp_label']) for r in records}
  movies.append({'file':stem,'rows':len(records),'distinct_recording_locators':len(keys),'locator_is_not_animal_identity':True,'records':records})
 write('MEASUREMENT_AUDIT.json',{'conditioning':condition,'whole_cell':traces,'duplicate_audit':duplicates,'summary_only_grids':grids,'behavior_scalar_audit':behavior,'movie_metadata':movies,'fitting':False,'simulation':False})
 print(json.dumps({'conditioning':[{ 'paired':v['paired_odor'],'effects':v['post_minus_pre'],'max_mean_error':max(abs(g['mean_error']) for g in v['groups'].values())} for v in condition],'duplicate_arrays':duplicates,'movie_summary':[{k:v[k] for k in ['file','rows','distinct_recording_locators']} for v in movies]},indent=2))
if __name__=='__main__':main()
