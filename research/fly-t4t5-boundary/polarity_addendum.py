from common import *
import numpy as np,collections
summary=[]
for typ in ['T4','T5']:
 d=json.loads((HERE/f'{typ}_POLARITY_MEASUREMENTS.json').read_text());rr=d['rows'];pairs=[]
 for width in [1,2,4]:
  for dur in [40,160]:
   by={v:{r['cell']:r for r in rr if r['width_pixels']==width and r['duration_ms']==dur and r['position_author_centered']==0 and r['contrast_value']==v} for v in [0,1]};cells=sorted(set(by[0])&set(by[1]))
   if cells:pairs.append({'width_pixels':width,'duration_ms':dur,'cells':cells,'n_pairs':len(cells),'median_dark_mean_mV':float(np.median([by[0][c]['mean_mV'] for c in cells])),'median_light_mean_mV':float(np.median([by[1][c]['mean_mV'] for c in cells])),'median_paired_light_minus_dark_mV':float(np.median([by[1][c]['mean_mV']-by[0][c]['mean_mV'] for c in cells]))})
 item={'type':typ,'traces':len(rr),'analyzed_cells':len(set(r['cell'] for r in rr)),'missing_repeat_counts':sum(r['num_repeats_source'] is None for r in rr),'paired_center_summaries':pairs};summary.append(item)
write('POLARITY_PAIRED.json',summary)
lines=['# Complete direct T4/T5 polarity extraction','', 'The 2021 archive is complete and matches its published MD5. T4/T5 member size/CRC and SHA-256 are recorded separately. The T5 recordings are reused original recordings, not independent replications of 2019. No conditional fit was altered after their recovery.','', '| Type | Analyzed recordings | Mean traces | Missing explicit repeat counts |','|---|---:|---:|---:|']
for x in summary:lines.append(f"| {x['type']} | {x['analyzed_cells']} | {x['traces']} | {x['missing_repeat_counts']} |")
lines+=['','T4 has an additional slot (ordinal 5), explicitly MATLAB-empty in the source, skipped by the authors’ plotting code. T5 ordinals 3 and 4 contain only contrast 0. Other condition-specific missing values are also preserved rather than filled. T5 `numReps` is absent from the inspected raw-condition group; this extractor leaves the repeat count null rather than inventing it or assuming equality to T4. Singleton MATLAB contrast dimensions are handled without creating missing contrasts.','', '## Matched author-center comparisons','', 'Mean voltage is computed over [0, flash duration + 75 ms). These are descriptive within-recording pairs, not independent-fly significance tests. Medians of differences need not equal differences of medians.','', '| Type | Width (pixels) | Duration (ms) | Matched recording pairs | Dark mean (median mV) | Light mean (median mV) | Paired light − dark (median mV) |','|---|---:|---:|---:|---:|---:|---:|']
for x in summary:
 for r in x['paired_center_summaries']:
  if r['width_pixels']==2:lines.append(f"| {x['type']} | 2 | {r['duration_ms']} | {r['n_pairs']} | {r['median_dark_mean_mV']:.3f} | {r['median_light_mean_mV']:.3f} | {r['median_paired_light_minus_dark_mV']:.3f} |")
lines+=['','No inference of spikes, calcium, transmitter sign, anatomical column occupancy, FlyWire identity or LPLC2 capability follows from these signed somatic voltages. The fits remain OFF-only conditional T5 models; this descriptive polarity extraction does not retroactively provide held-out polarity prediction. Raw mean traces and full condition metrics are saved in the type-specific NPZ/JSON artifacts.']
(HERE/'POLARITY_ADDENDUM.md').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines[-10:]))
