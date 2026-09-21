from common import *
import numpy as np
p=HERE/'processed/Figure_3-figure-supplement2D_Source_data.json'
t={c['ref']:c['value'] for c in load(p)[0]['cells']};groups=[]
for paired,n,cs in [('OCT',6,['B','C','D','E']),('MCH',5,['G','H','I','J'])]:
 row=[]
 for col in cs:
  v=[t[f'{col}{i}'] for i in range(5,5+n)];row.append({'column':col,'n_source_rows':n,'values':v,'mean':float(np.mean(v)),'source_mean':t[f'{col}3'],'mean_error':float(np.mean(v)-t[f'{col}3']),'sem_error':float(np.std(v,ddof=1)/np.sqrt(n)-t[f'{col}4'])})
 groups.append({'paired_odor':paired,'groups':row,'external_fly_ids':None})
write('ALPHA1_CONDITIONING_AUDIT.json',{'source':'https://elifesciences.org/articles/79042/figures#fig3s2','archive':'sources/elife-79042-fig3-figsupp2-data1-v2.zip','source_workbook_sha256':sha(HERE/'sources/79042-alpha1/Figure_3-figure-supplement2D_Source_data.xlsx'),'groups':groups,'quantity':'odor-evoked spike count as labeled in figure caption, not UpWiN mV','response_window':'0–1.2 s per article electrophysiology method; counts/rates must not be interchanged','preparation':'in-vivo MBON-alpha1; MB319C; PAM-alpha1 MB043-split-LexA; 1 min paired odor + 120 1 ms 2 Hz pulses','relation_to_85756':'Comparable olfactory timing but different target neurons and DAN driver; not same-animal measurements or a numerical transfer function','genesis_rate_conversion':None,'cross_paper_identity_join':None})
print(groups)
