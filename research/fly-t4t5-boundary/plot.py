from pathlib import Path
import os,json,sys
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P/'vendor'))
os.environ['MPLCONFIGDIR']=str(P/'.mpl-cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
r=json.loads((P/'RESULTS.json').read_text())['aggregate'];families=['flash','apparent_motion','moving_bar','static_grating','drifting_grating']
fig,ax=plt.subplots(1,3,figsize=(16,4.4),layout='constrained')
for i,(kind,label,col) in enumerate([('Z','Zero reference','#aaaaaa'),('SELECTED','Flash-selected model','#286e80')]):
 vals=[next(x['median_rmse_mV'] for x in r if x['candidate']==kind and x['family']==f) for f in families]
 ax[0].bar(np.arange(5)+(.19 if i else -.19),vals,.36,label=label,color=col)
ax[0].set_xticks(range(5),['Other flash\nwidths','Apparent\nmotion','Moving\nbar','Static\ngrating','Drifting\ngrating']);ax[0].set_ylabel('Median per-recording RMSE (mV)');ax[0].legend(fontsize=8);ax[0].set_title('Held-out stimulus families')
with np.load(P/'processed/cell_01_test.npz') as z,np.load(P/'PREDICTIONS.npz') as pred:
 m=json.loads(str(z['metadata']));i=next(i for i,x in enumerate(m) if x['family']=='moving_bar');a,b=z['starts'][i],z['ends'][i]
 ax[1].plot(z['t_ms'][a:b],z['voltage_mV'][a:b],label='Measured voltage',color='#222222');ax[1].plot(z['t_ms'][a:b],pred['cell1_SELECTED'][a:b],label='Frozen prediction',color='#286e80')
ax[1].set_title('T5 recording 1: first moving-bar trace');ax[1].set_xlabel('Time from stimulus onset (ms)');ax[1].set_ylabel('Baseline-subtracted voltage (mV)');ax[1].legend(fontsize=8)
meta=json.loads((P/'T4_POLARITY_MEASUREMENTS.json').read_text())['rows']
with np.load(P/'T4_POLARITY_TRACES.npz') as z:
 for v,color,label in [(0,'#734aa0','Dark flash'),(1,'#db9620','Light flash')]:
  rr=next(x for x in meta if x['cell']==1 and x['width_pixels']==2 and x['duration_ms']==160 and x['position_author_centered']==0 and x['contrast_value']==v)
  ax[2].plot(z['time_ms'],z[rr['key']],color=color,label=label)
ax[2].axvspan(0,160,color='#eeeeee',zorder=-1);ax[2].set_title('T4 recording 1: center polarity responses');ax[2].set_xlabel('Time from stimulus onset (ms)');ax[2].set_ylabel('Measured voltage (mV)');ax[2].legend(fontsize=8)
for a in ax:a.spines[['top','right']].set_visible(False)
fig.suptitle('T4/T5 boundary study — conditional assays, not a validated general boundary',fontsize=13)
fig.savefig(P/'RESULTS_FIGURE.png',dpi=180);fig.savefig(P/'RESULTS_FIGURE.svg')
