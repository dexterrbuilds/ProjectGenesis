from common import *
import numpy as np
stats=read('VALIDATION_RESULTS.json')['strata'];env=read('UNCERTAINTY.json')['envelopes']
summary=[]
for s in stats:
 ee=[e for e in env if e['stratum']==s['stratum']];finite=[e for e in ee if e['half_width_mV'] is not None]
 if s['meets_registered_criteria']:
  summary.append({'stratum':s['stratum'],'recordings':s['recordings'],'conditions':s['conditions'],'median_RMSE_mV':s['median_recording_RMSE_mV'],'reference_RMSE_mV':s['median_reference_RMSE_mV'],'MSE_difference_CI95':s['paired_difference_ci95_mV2'],'zero_difference_CI95':s['difference_from_zero_ci95_mV2'],'finite_envelope_recordings':len(finite),'unknown_envelope_recordings':len(ee)-len(finite),'median_envelope_half_width_mV':float(np.median([e['half_width_mV'] for e in finite])) if finite else None,'empirical_envelope_coverage':sum(e['simultaneous_condition_waveform_coverage'] for e in finite)/len(finite) if finite else None})
write('RESULT_SUMMARY.json',{'classification':'LIMITED EMPIRICAL INTERFACE SUPPORTED','passing_comparisons':summary,'total_strata':len(stats),'passing_strata':len(summary),'prediction_count':len(read('PREDICTION_METRICS.json')),'recordings_are_not_flies':True,'cross_family_prediction_supported':False})
def f(x):return '—' if x is None else f'{x:.3f}'
def interval(x):return '—' if x is None else '['+', '.join(f(v) for v in x)+']'
lines=['# Complete empirical validation table','','RMSE is the median of per-recording waveform RMSE, in mV. Intervals are for the equal-recording-weight mean paired MSE difference, mV²; they are not intervals on the median RMSE. No fly-independent inference. E1 reference is nearest-condition E0; E2 reference is the recording-balanced family mean.','','| Stratum | Conditions | Recordings | RMSE | Reference RMSE | MSE difference CI95 | Versus zero CI95 | Comparative support |','|---|---:|---:|---:|---:|---|---|---|']
for s in stats:lines.append('| '+s['stratum'].replace('|',' / ')+f" | {s['conditions']} | {s['recordings']} | {f(s['median_recording_RMSE_mV'])} | {f(s['median_reference_RMSE_mV'])} | {interval(s['paired_difference_ci95_mV2'])} | {interval(s['difference_from_zero_ci95_mV2'])} | "+('yes' if s['meets_registered_criteria'] else 'no / untested')+' |')
lines+=['','## Residual envelopes for supported comparisons','','These are maxima across each recording’s held-out conditions and all 501 time samples. The cross-recording rank envelope is descriptive, not a guaranteed population interval. Unknown is unbounded, not zero. Class-template export does not claim this individual residual envelope is an uncertainty interval on the template mean.','','| Stratum | Finite / unknown recording envelopes | Median half-width mV | Held-out coverage |','|---|---:|---:|---:|']
for s in summary:lines.append('| '+s['stratum'].replace('|',' / ')+f" | {s['finite_envelope_recordings']} / {s['unknown_envelope_recordings']} | {f(s['median_envelope_half_width_mV'])} | {f(s['empirical_envelope_coverage'])} |")
(HERE/'VALIDATION_TABLES.md').write_text('\n'.join(lines)+'\n')
