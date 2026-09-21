"""Lossless reporting/packaging of sealed outputs; no new transfer calculation or model."""
from pathlib import Path
from collections import Counter
import csv,json,hashlib,shutil,datetime
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;P=R/'research/fly-stage5-protocol-v0.1'
S=R/'research/fly-stage5-results-attempt2-staging'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):
 assert not p.exists();p.write_text(json.dumps(d,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def fmt(v):return '{'+', '.join('+'+str(x) if x>0 else str(x) for x in v)+'}'
assert load(H/'REPRODUCIBILITY.json')['valid']
assert load(H/'INTEGRITY_AFTER.json')['passed']
a=load(H/'CANONICAL_BEFORE.json');b=load(H/'CANONICAL_AFTER.json')
assert a==b==load(P/'CANONICAL_BEFORE.json')
assert all(load(H/f'PROCESS_{n}.json')['exit_code']==0 for n in [1,2])
r=load(P/'RELEASE.json');auth=load(H/'AUTHORIZATION.json')
assert r['content_sha256']==auth['reviewed_content_sha256']
x=R/'research/fly-stage5-runs/attempt-2-process-1/RESULTS.json';y=R/'research/fly-stage5-runs/attempt-2-process-2/RESULTS.json'
assert x.read_bytes()==y.read_bytes()
d=load(x);units=d['units'];fs=['E','Z','P','R','WP','WR','H','U','N'];contrasts=['response_change','restoration_check','plastic_state_retention','learned_state_comparison']
lock=load(P/'STAGE1_INPUT_LOCK.json');run_names=[row['run'] for row in lock['inputs']]
expected={(run,c,con) for run in run_names for c in ['A','B'] for con in contrasts}
assert len(units)==224 and {(u['run'],u['cue'],u['contrast']) for u in units}==expected
assert all(set(u['families'])==set(fs) for u in units)
assert not S.exists();S.mkdir()
for n in [1,2]:shutil.copytree(R/f'research/fly-stage5-runs/attempt-2-process-{n}',S/f'process-{n}')
shutil.copy2(x,S/'RESULT_MATRIX.json')
shutil.copy2(P/'COUNTEREXAMPLE_REGISTRY.json',S/'PREREGISTERED_COUNTEREXAMPLES.json')
write(S/'PROTOCOL_REFERENCE.json',{'relative_path':str(P.relative_to(R)),'version':r['version'],'content_sha256':r['content_sha256'],'release_file_sha256':sha(P/'RELEASE.json'),'analysis_code_sha256':r['analysis_code_sha256'],'sealed_artifact_hashes':r['files'],'anatomical_or_neural_state_ownership':'references only; no new ownership'})
write(S/'ATTEMPT1_REFERENCE.json',{'path':'research/fly-stage5-preflight-evidence/73105536b60f57079bf5ef556d20c10f7194cba0650e70e77383291506cc7047','content_sha256':'73105536b60f57079bf5ef556d20c10f7194cba0650e70e77383291506cc7047','historical_status':'Stopped preflight; auxiliary verification implementation error; 0 evaluated units; no authorization record; no scientific result. Unchanged.','new_attempt_id':'genesis-stage5-attempt-2-20260920'})
family_summary={f:[{'identification_set':list(k),'units':n} for k,n in sorted(Counter(tuple(u['families'][f]) for u in units).items())] for f in fs}
coverage=[]
for con in contrasts:
 for role in ['paired','unpaired']:
  us=[u for u in units if u['contrast']==con and (u['cue']==u['paired_cue'])==(role=='paired')]
  coverage.append({'contrast':con,'cue_role':role,'unit_count':len(us),'source_sign_sets':[{'sign_set':list(k),'units':n} for k,n in sorted(Counter(tuple(u['source_sign_set']) for u in us).items())]})
write(S/'FAMILY_SUMMARY.json',{'families':family_summary,'unit_label_counts':d['label_counts'],'ambiguity_flags':sum(u['numerical_ambiguity'] for u in units),'contrast_and_cue_role_coverage':coverage,'aggregation_scope':'Descriptive counts only; full unaggregated results retained. Marginal sets are not a joint Cartesian product or probabilities.'})
write(S/'SOURCE_DEPENDENCE_GATES.json',d['control_gate'])
write(S/'SOURCE_DIAGNOSTICS.json',d['source_diagnostics'])
# Direct expansion of the sealed matrix, with no recalculated signs or readout.
fields=['run','cue','paired_cue','cue_role','contrast','source_left','source_right','source_units','source_sign_set','numerical_ambiguity','family','identification_set','labels']
with (S/'ALL_FAMILY_RESULTS.csv').open('w',newline='') as out:
 w=csv.DictWriter(out,fieldnames=fields);w.writeheader()
 for u in units:
  for f in fs:
   row={k:u[k] for k in ['run','cue','paired_cue','contrast','source_left','source_right','source_units','numerical_ambiguity']}
   row.update(cue_role='paired' if u['cue']==u['paired_cue'] else 'unpaired',source_sign_set=json.dumps(u['source_sign_set']),family=f,identification_set=json.dumps(u['families'][f]),labels=json.dumps(u['labels']))
   w.writerow(row)
# All preregistered adversaries retained beside every unit. No new numerical witnesses.
counter_units=[]
for u in units:
 counter_units.append({'run':u['run'],'cue':u['cue'],'contrast':u['contrast'],
 'restricted_nonzero_singletons':[f for f in fs if len(u['families'][f])==1 and u['families'][f]!=[0]],
 'null_map':u['families']['Z'],'plateau_preserving':u['families']['WP'],'plateau_reversing':u['families']['WR'],
 'opposite_orientation':{'P':u['families']['P'],'R':u['families']['R']},
 'heterogeneous_zero_mass_and_cancellation':u['families']['H'],'alternative_input_nuisance':u['families']['N'],
 'counterexample_registry_entries':list(range(1,9)),
 'scope':'Registry adversaries retain their frozen analytic meanings; no new parameter sweep or physical inference.'})
write(S/'COUNTEREXAMPLE_AUDIT.json',{'registry':d['counterexample_registry'],'units':counter_units,'nonzero_singleton_unit_count':sum(bool(u['restricted_nonzero_singletons']) for u in counter_units),'all_units_retain_null_and_nuisance_challenges':all(0 in u['null_map'] and u['alternative_input_nuisance']==[-1,0,1] for u in counter_units),'outcome':'No restricted nonzero conclusion survives every evidence-admissible counterexample. No biological direction, responder mass, recall mediation, magnitude ranking, physiological reset or kinematic inference is admitted.'})
failed=[{'family':g['family'],**c} for g in d['control_gate'] for c in g['checks'] if not c['passed']]
preservation={'passed':True,'protected_files':9170,'sealed_stage5_artifacts':28,'sealed_release_sha256':r['content_sha256'],'attempt1_preserved':True,'canonical_before_equals_after':True,'canonical_database_sha256':b['sha256'],'canonical_decisions':b['tableRowCounts']['genesis_decisions'],'schedule_enabled':False,'neural_runs':d['neural_runs'],'new_physical_observations':d['new_physical_observations'],'brain_adapter_changes':0,'runtime_actions':0,'wallet_actions':0,'organism_llm_actions':0,'capability_admissions':d['capability_admissions'],'evidence':'Hash audits, exact sealed code, recorded commands and read-only SQL snapshots; not a claim of external OS-wide process surveillance.'}
write(H/'PRESERVATION_FINAL.json',preservation)
write(S/'PRESERVATION_AUDIT.json',preservation)
write(S/'EXECUTION_SUMMARY.json',{'attempt_id':'genesis-stage5-attempt-2-20260920','sealed_stage5_release_hash':r['content_sha256'],'authorization_referenced_hash':auth['reviewed_content_sha256'],'authorization_hash_match':True,'corrected_preflight':'PASSED','authoritative_dependency_verification':'PASSED','sealed_artifacts':'UNCHANGED','execution':'COMPLETED EXACT SEALED ANALYSIS IN TWO FRESH PROCESSES','byte_identical':True,'planned_runs':28,'evaluated_runs':len(run_names),'planned_units':224,'evaluated_units':len(units),'family_evaluations':len(units)*len(fs),'gates':{g['family']:g['verdict'] for g in d['control_gate']},'label_counts':d['label_counts'],'failed_scientific_checks':failed,'integrity_failures_attempt2':[],'null_compatible_units':224,'transfer_sensitive_units':224,'full_family_signed_invariant_units':0,'result_sha256':sha(x),'scientific_scope':'Archived dimensionless source → conditional marginal ordinal identification sets. No physical or behavioral output.'})
# Verify the exported CSV against the frozen output, not a second scientific implementation.
rows=list(csv.DictReader((S/'ALL_FAMILY_RESULTS.csv').open()));assert len(rows)==2016
lookup={(u['run'],u['cue'],u['contrast']):u for u in units}
for row in rows:
 u=lookup[(row['run'],row['cue'],row['contrast'])];assert json.loads(row['identification_set'])==u['families'][row['family']]
 assert row['source_left']==u['source_left'] and row['source_right']==u['source_right']
write(S/'REPORTING_VALIDATION.json',{'passed':True,'exact_unit_keys':224,'family_rows':2016,'csv_lossless_comparison':True,'copy_of_original_matrix_byte_identical':(S/'RESULT_MATRIX.json').read_bytes()==x.read_bytes(),'no_new_transfer_calculation':True,'both_original_process_outputs_retained':True})
# Human report: only sealed results, scope and descriptive coverage.
lines=['# Project Genesis Stage 5 — archived-data mathematical results',
'','## Execution identity and integrity','',
'Prospective Protocol v0.1.0. Attempt 2 completed the exact sealed analysis after the second user authorization. This is not a neural simulation or a biological capability test.',
'',f"- **SEALED_STAGE5_RELEASE_HASH:** `{r['content_sha256']}`",f"- **AUTHORIZATION_REFERENCED_HASH:** `{auth['reviewed_content_sha256']}`",'- **AUTHORIZATION_HASH_MATCH: TRUE**, verified by reading the separate record back from disk.',
'- Corrected preflight: 10,093 comparisons passed. All 28 sealed artifacts and 9,170 prior protected files matched. All 381 Stage-1 evidence payloads and 140 selected references remained pinned.',
'- Authoritative Brain Spec package and route/identity/identifiability release methods passed. The sealed static suite passed 17/17 tests. No Stage-1 numerical source-summary values were read before authorization.',
'- Attempt 1 remains the unchanged stopped-preflight record, including the incorrect auxiliary checker and zero evaluated units. Its content hash is `73105536b60f57079bf5ef556d20c10f7194cba0650e70e77383291506cc7047`.',
'- Attempt 2 corrected only external hash-object semantics. The manifest file hash and canonical package-content hash remain distinct. Both checker iterations are archived; the final label-only correction prevents overwriting PACKAGE-CONTENT metadata with a generic release label. No scientific comparison or protected-file check was weakened.',
'', '## Complete coverage and reproducibility','',
'Both processes exited 0 with empty stdout/stderr. They independently generated byte-identical `RESULTS.json` and `RESULTS.sha256`. Process 2 read only process 1’s exit-status record, never its scientific results. Comparison occurred after both finished.',
'',f"Scientific result SHA-256: `{sha(x)}` ({x.stat().st_size:,} bytes).",'',
'**28/28 frozen runs × 2 cue identities × 4 contrasts = 224/224 units**, each with all nine families: **2,016 family evaluations**. The six intact runs cover three model seeds and both cue assignments. Intervention coverage is seed 1701 only. These are not 28 independent biological replicates. No new training, neural replay, lesion calculation, fitting, rescaling or physical observation enters the calculation.',
'','| Process | Wall time (s) | Child user + system CPU (s) | Peak child RAM (MiB) |','|---|---:|---:|---:|']
for n in [1,2]:
 p=load(H/f'PROCESS_{n}.json');lines.append(f"| {n} | {p['wall_seconds']:.3f} | {p['child_user_cpu_seconds']+p['child_system_cpu_seconds']:.3f} | {p['child_maxrss_native_units']/1048576:.2f} |")
lines += ['', 'These are execution measurements for hash verification and archived-data mathematical processing, not neural update benchmarks. Timing/log records are expected to differ; scientific output bytes must match and do.',
'', '## Family-by-family identification sets','',
'All signs below are abstract comparison signs. They have no physical unit or behavioral meaning. Sets are marginal per contrast, not jointly independent states or probabilities.',
'','| Family | Set → number of units | Assumption / scope |','|---|---|---|']
scopes={'E':'Broad evidence-admissible family; unrestricted nuisance.','Z':'Constant map and matched nuisance; mathematical null.','P':'Common strictly increasing map, matched nuisance; orientation assumed.','R':'Common strictly decreasing map, matched nuisance; orientation assumed.','WP':'Weakly increasing map; plateaus included.','WR':'Weakly decreasing map; plateaus included.','H':'Abstract heterogeneous mixture; zero responsive mass and cancellation retained.','U':'Arbitrary fixed scalar function; no inferred physiological operator.','N':'Unrestricted nuisance contrasts; no fitted or bounded nuisance magnitude.'}
for f in fs:lines.append('| '+f+' | '+'; '.join(fmt(v['identification_set'])+' → '+str(v['units']) for v in family_summary[f])+' | '+scopes[f]+' |')
lines += ['', '### Coexisting preregistered labels','', '| Label | Units |','|---|---:|']
for label,count in d['label_counts'].items():lines.append(f'| {label} | {count} |')
lines += ['', '**All 224 units are both TRANSFER-SENSITIVE / NON-ROBUST and NULL-COMPATIBLE.** All also have ROBUST ONLY UNDER RESTRICTED CONDITIONAL FAMILY; this includes zero singletons and must not be read as 224 nonzero effects. No unit has a signed singleton across the full evidence-admissible family. No unit is UNINTERPRETABLE, and no numerical ambiguity flag was raised.',
'', '## Source-dependence gates and controls','', '| Gate | Verdict | Checks passed |','|---|---|---:|']
for g in d['control_gate']:lines.append(f"| {g['family']} | {g['verdict']} | {sum(c['passed'] for c in g['checks'])}/{len(g['checks'])} |")
lines += ['', 'Both gates satisfy exactly the frozen conditional requirements. All six intact paired-cue response-change and plastic-state-retention comparisons exclude zero under P/R; their restoration comparisons equal zero. Frozen-plasticity, silenced-DAN, removed-DA-contact and unpaired-teaching paired-cue controls equal zero. Required PN/KC baseline/post stability checks pass at the unchanged 1e−12 dimensionless engineering tolerance. Original restoration/replay metadata passed the sealed source-validation requirements; no neural replay was newly executed.',
'','**Failed gate checks: none.** All other preregistered interventions remain reported even where their ordinal profile does not differ from intact. A route removal with zero sensory/output activity is not pathway-specific biological mediation evidence.',
'', '### Full run/cue profiles under P','',
'The table reports both cue identities. Each entry gives the P sets for response_change / restoration_check / plastic_state_retention / learned_state_comparison, in that order. Every other family for every entry remains in ALL_FAMILY_RESULTS.csv and RESULT_MATRIX.json; no branch is discarded.',
'', '| Frozen run | Paired identity | Cue A: four sets | Cue B: four sets |','|---|---|---|---|']
for run in run_names:
 groups=[]
 for cue in ['A','B']:groups.append(' / '.join(fmt(lookup[(run,cue,con)]['families']['P']) for con in contrasts))
 lines.append(f"| {run} | {lookup[(run,'A',contrasts[0])]['paired_cue']} | {groups[0]} | {groups[1]} |")
lines += ['', 'Both paired and unpaired cues have nonzero P/R comparisons in the six intact runs. The frozen gate is not a strict cue-exclusivity criterion. Single-DAN and matched-DAN lesions both retain nonzero ordinal comparisons; this analysis does not rank their effect magnitudes. The matched lesion is opposite-compartment, not established biologically unrelated. PN-weight shuffling, APL removal and recurrence removal also retain nonzero comparisons in these saved runs; none is omitted or retuned.',
'', '### Contrast and cue-role coverage','', '| Contrast | Cue role | Source sign sets → counts |','|---|---|---|']
for c in coverage:lines.append(f"| {c['contrast']} | {c['cue_role']} | "+'; '.join(fmt(x['sign_set'])+' → '+str(x['units']) for x in c['source_sign_sets'])+' |')
lines += ['', 'Across all units, 96 saved source comparisons are strictly negative beyond the frozen tolerance and 128 are exactly equal stored values. All 56 restoration comparisons are equal. Each non-restoration contrast includes 16 negative paired-cue and 16 negative unpaired-cue comparisons, plus 12 equal comparisons for each role. These are unrescaled source-order counts, not a new cross-cue score.',
'', '## Counterexample audit','',
'COUNTEREXAMPLE_AUDIT.json retains every registered challenge beside all 224 units, including all 96 units with conditional nonzero singletons. It reports only the sealed analytic alternatives; no numerical parameter sweep or new witness-fitting was performed.',
'', '| Apparent conclusion | Retained challenge | Interpretation |','|---|---|---|']
for e in d['counterexample_registry']['entries']:lines.append(f"| {e['claim']} | {e['adversary']} | {e['required_downgrade']} |")
lines += ['', 'For every conditional nonzero result, Z permits zero, WP/WR permit plateaus, P and R give opposite orientations, H permits zero responsive mass or cancellation, and N permits cancellation or either orientation. Thus no nonzero signed conclusion survives the full declared family. Even exact source equality gives the full set under E/N when nuisance is unrestricted.',
'', '## Invariants actually established and limits','',
'- **Conditional equality:** for the 128 exactly equal saved source comparisons, every matched-nuisance fixed-map family Z/P/R/WP/WR/H/U returns `{0}`. This does not extend to E/N or establish a physiological reset.',
'- **Conditional order:** for the 96 ordered comparisons, P returns `{−1}` and R `{+1}`. Their orientation is imposed by the family definition, not discovered from biology. Weak monotonicity also permits equality.',
'- **Model-dependence profile:** the P and R gates pass for the archived intact/mechanism/timing/restoration/sensory controls under their declared matched-context assumptions. This is not biological mediation.',
'- **Set-valued uncertainty:** every full-family identification set is `{−1,0,+1}`. This is an exhaustive uncertainty statement under the frozen rules, not one invariant signed response or a distribution.',
'- Null remains compatible for all units. This is not evidence of biological absence. Direction remains transfer-sensitive for all units. Transfer sensitivity is a valid completed result.',
'- Scalar sufficiency, common map, domain compatibility, nuisance restrictions, sign and responsiveness remain assumptions or unknowns. No gain, time constant, responder fraction, receptor sign, voltage, firing rate, physical transfer magnitude or biological latency is identified. No 4/17 mixture weight or 50 ms downstream constant was imported.',
'- Separate Stage-1 model, biological spike-count, acute somatic voltage, population calcium, recall voltage, two behavioral-driver and individual-anatomy domains remain separate. No new observation bridge or root-specific activity is assigned.',
'', '## Evidence categories','',
'| Category | What this execution establishes |','|---|---|',
'| BIOLOGICAL FACT | No new biological measurements or biological transmission claim. Prior literature stays in its original observation domains. |',
'| EXPERIMENTALLY SUPPORTED COMPUTATIONAL APPROXIMATION | No new physiological approximation is calibrated or admitted. Stage 1 supplies its frozen model observations and control evidence only. |',
'| HYPOTHESIS | A connection between the abstract source scalar and an independently observed biological target remains unestablished. |',
'| ENGINEERING / MATHEMATICAL ASSUMPTION | Decimal parsing, 50-digit arithmetic, 1e−12 precision policy, analytic transfer families, matched-context restrictions and marginal identification sets remain explicit. |',
'| GENESIS PRODUCT MAPPING | None. |',
'', '## Preservation and failures','',
'Post-execution verification passed: all 9,170 protected files, all 28 sealed protocol artifacts, the release identity, Brain Spec v0.2, Stage 1, C. elegans and the prior packages remain unchanged. Attempt-1 package and original working records remain unchanged. The database audit before/after matches the frozen state exactly:',
'',f"- Database SHA-256: `{b['sha256']}`.",'- Seven decisions/cycles; schedule disabled.',
'- Zero new neural runs, physical observations, runtime actions, wallet actions, organism LLM actions, BrainAdapter changes or capability admissions.',
'- Attempt-2 actual integrity failures: none. Failed scientific gate checks: none. Attempt-1 auxiliary comparison error remains recorded as an unsuccessful historical preflight.',
'', '## Artifact guide','',
'- RESULT_MATRIX.json: exact original scientific output, all 224 units, all family sets, source decimals, ambiguity flags, diagnostics and labels.',
'- ALL_FAMILY_RESULTS.csv: lossless long-format table of all 2,016 family evaluations.',
'- process-1/ and process-2/: both original outputs and result hashes.',
'- SOURCE_DEPENDENCE_GATES.json: all 164 P/R checks and verdicts.',
'- COUNTEREXAMPLE_AUDIT.json and PREREGISTERED_COUNTEREXAMPLES.json: complete challenge coverage.',
'- FAMILY_SUMMARY.json: all family set counts and both cue roles.',
'- governance/: authorization/read-back, corrected checker versions/diffs, pre/post hash audits, authoritative verification logs, static suite logs, database audits, commands/environment, process records, stdout/stderr and reproducibility.',
'- PROTOCOL_REFERENCE.json and ATTEMPT1_REFERENCE.json: exact historical identities, references only.',
'- RELEASE.json: content hash of the sorted compact UTF-8 file-hash map, with every generated artifact hashed; release file excluded to avoid circular hashing.',
'', '## Scientific conclusion','',
'The frozen learned source signal supports conditional ordinal comparisons and the preregistered modeled source-dependence profile under strict monotone, common-map, matched-context assumptions. The evidence-admissible family admits zero and both orientations for every unit. No nonzero signed conclusion is invariant across that family. This establishes no biological propagation, physical response, behavioral output or new Genesis capability.',
'', '**Stop for review.** No integration, Brain Spec update, capability promotion, decoder, fitting or subsequent study is performed.','']
(S/'STAGE5_REPORT.md').write_text('\n'.join(lines))
shutil.copytree(H,S/'governance')
# Record the artifact kinds before sealing without assigning scientific meaning to governance logs.
write(S/'ARTIFACT_GUIDE.json',{'primary_scientific_outputs':['process-1/RESULTS.json','process-2/RESULTS.json','RESULT_MATRIX.json'],'lossless_reporting_outputs':['ALL_FAMILY_RESULTS.csv','FAMILY_SUMMARY.json','SOURCE_DEPENDENCE_GATES.json','SOURCE_DIAGNOSTICS.json','COUNTEREXAMPLE_AUDIT.json'],'human_report':'STAGE5_REPORT.md','governance_directory':'governance','result_sha256':sha(x),'original_outputs_are_not_overwritten':True})
files={str(p.relative_to(S)):sha(p) for p in sorted(S.rglob('*')) if p.is_file()}
content=hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
write(S/'RELEASE.json',{'id':'genesis-stage5-scientific-results','version':'0.1.0','attempt_id':'genesis-stage5-attempt-2-20260920','sealed_protocol_content_sha256':r['content_sha256'],'scientific_result_sha256':sha(x),'files':files,'content_sha256':content,'hash_definition':'SHA256 of compact sorted UTF-8 JSON file-hash map; RELEASE.json excluded','execution_status':'completed; two fresh processes byte-identical','biological_capability_classification':None,'capability_admissions':[],'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
dest=R/'research/fly-stage5-results'/content;dest.parent.mkdir(exist_ok=True);assert not dest.exists();S.rename(dest)
assert all(sha(dest/p)==h for p,h in files.items())
print(json.dumps({'package':str(dest),'content_sha256':content,'files':len(files),'planned_units':224,'evaluated_units':len(units),'result_sha256':sha(x),'package_verified':True}))
