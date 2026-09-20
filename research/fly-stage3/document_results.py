"""Render final quantitative report from sealed evidence; never fits or runs a model."""
import hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent

def table(h,rows):
    return '\n'.join(['| '+' | '.join(h)+' |','| '+' | '.join(['---']*len(h))+' |']+['| '+' | '.join(map(str,row))+' |' for row in rows])
def pct(x):return 'undefined' if x is None else f'{100*x:.9g}%'
def num(x):return 'undefined' if x is None else f'{x:.12g}'

def main():
    ep=next((HERE/'evidence').iterdir());ev=next((HERE/'evaluations').glob('*/evaluation.json'))
    d=json.loads((ep/'results.json').read_text());a=json.loads(ev.read_text())
    ap=next((HERE/'anatomy-audit').glob('*/anatomy.json'));an=json.loads(ap.read_text())
    lp=next((HERE/'learned-evidence').iterdir());lv=json.loads((lp/'results.json').read_text())
    for name,h in json.loads((lp/'file-manifest.json').read_text())['files'].items():assert hashlib.sha256((lp/name).read_bytes()).hexdigest()==h
    assert hashlib.sha256((lp/'results.json').read_bytes()).hexdigest()==lp.name
    primary=[x for x in a['paired_comparisons'] if x['condition'].startswith('primary')]
    by={r['run']:r for r in d['runs']}
    comparison=table(['Seed / cue','MBON11 low (late)','MBON11 high (late)','Low/high contrast','MBON11 experience (low)','LH experience (low)','LH low/high contrast'],
        [[str(x['seed'])+' / '+x['cue'],num(x['low_last']['MB11']),num(x['high_last']['MB11']),pct(x['state_contrast']['MB11']),
          pct(x['experience_low']['MB11']),pct(x['experience_low']['LH']),pct(x['state_contrast']['LH'])] for x in sorted(primary,key=lambda x:x['condition'])])
    baseline=table(['Seed / cue','MBON11 low first → last','MBON11 high first → last','MBON18 low first → last','LH low first → last'],
        [[str(x['seed'])+' / '+x['cue'],num(x['low_baseline']['MB11'])+' → '+num(x['low_last']['MB11']),
          num(x['high_baseline']['MB11'])+' → '+num(x['high_last']['MB11']),
          num(x['low_baseline']['MB18'])+' → '+num(x['low_last']['MB18']),
          num(x['low_baseline']['LH'])+' → '+num(x['low_last']['LH'])] for x in sorted(primary,key=lambda x:x['condition'])])
    boundary=table(['Population','Neurons','Retained input','Omitted input','Input %','Retained output','Omitted output','Output %'],
        [[g,an['counts']['roles'][g],r['retained_input'],r['omitted_input'],pct(r['input_retention']),r['retained_output'],r['omitted_output'],pct(r['output_retention'])] for g,r in an['roles'].items()])
    controls=table(['Condition','Resource contrast MBON11','Contrast reduction','LH resource contrast','Largest PN/KC lesion change'],
        [[x['condition'],pct(x['state_contrast']),pct(x['reduction']),pct(x['LH_resource_contrast']),pct(max(x['sensory_lesion_change'].values()))] for x in a['interventions']])
    acquisition=table(['Cue / resource','MBON11 suppression','MBON18 suppression','LH suppression','MBON11 suppression with OA silenced'],
        [[x['cue']+' / '+str(x['resource']),pct(x['suppression']['MB11']),pct(x['suppression']['MB18']),pct(x['suppression']['LH']),pct(x['OA_lesion_suppression']['MB11'])] for x in a['acquisition']])
    sensitivity=table(['Variant','MBON11 state contrast','MBON11 trial change low','LH trial change low','PN contrast','KC contrast'],
        [[x['condition'],pct(x['state_contrast']['MB11']),pct(x['experience_low']['MB11']),pct(x['experience_low']['LH']),pct(x['state_contrast']['PN']),pct(x['state_contrast']['KC'])]
         for x in a['paired_comparisons'] if x['condition'].startswith('sensitivity')])
    factrows=[];interactions=[]
    for q in ('A','B'):
        for cond in ('intact','silence_dan','silence_mb11','freeze_modulation'):
            xx={(r['resource'],r['learned']):r['responses'][q]['groups']['VALUE'] for r in lv['rows'] if r['paired']==q and r['intervention']==cond}
            lo=xx[.2,True]-xx[.2,False];hi=xx[.8,True]-xx[.8,False]
            mixed=lo-hi;normalized=mixed/abs(hi) if abs(hi)>1e-12 else None
            factrows.append([q+' / '+cond,num(xx[.2,False]),num(xx[.2,True]),num(xx[.8,False]),num(xx[.8,True]),num(mixed),pct(normalized)])
            interactions.append({'cue':q,'intervention':cond,'mixed_difference':mixed,'relative_to_learned_effect':normalized})
    factorial=table(['Paired cue / intervention','Low naive','Low trained','High naive','High trained','Mixed difference','Relative interaction'],factrows)
    results_table=table(['Prospective criterion','Result'],[[k,'met' if v else '**not met**'] for k,v in a['criteria'].items()])
    temporal=[]
    for x in sorted(primary,key=lambda x:x['condition']):
        r=by[x['condition']+'-0.2'];s=by[f"protocol-none-single-intact-{x['cue']}-0.2"] if x['seed']==3701 else None
        t=r['metrics']['trials']
        temporal.append([x['condition'],pct(t[9]['after_offset']['MB11']/max(t[9]['maintained']['MB11'],1e-12)),
                        pct(t[9]['after_offset']['LH']/max(t[9]['maintained']['LH'],1e-12)),
                        ' / '.join(num(r['metrics']['duration_sweep']['MB11'][str(f)]) for f in (.25,.5,.75)),
                        pct(t[9]['maintained']['MB11']/s['metrics']['trials'][9]['maintained']['MB11']-1) if s else 'seeds3702/3: not scheduled'])
    timing=table(['Primary low-resource condition','MBON11 post-offset/maintained','LH post-offset/maintained','Seconds above25/50/75% in final12s','Ten vs single final cue MBON11'],temporal)
    criteria_path=ev.relative_to(HERE)
    paths={key:v['contacts'] for key,v in an['pathways'].items()}
    p=a['performance'];rs=[r for r in d['runs'] if r['run'].startswith('primary')]
    maxreset=max(r['reset_max_rate_delta'] for r in rs)
    mincontrast=min(x['state_contrast']['MB11'] for x in primary);maxcontrast=max(x['state_contrast']['MB11'] for x in primary)
    primaryexperience=[-x['experience_low']['MB11'] for x in primary]
    lhchange=[x['experience_low']['LH'] for x in primary]
    persistence=[]
    for x in primary:
        q=x['cue'];r=by[x['condition']+'-0.2'];b=r['baseline'][q]['groups']['MB11'];post=r['fast_reset'][q]['groups']['MB11']
        persistence.append(1-post/b)
    report=f'''# Stage 3 — resource-state modulation and persistence

**Final classification: {a['classification']}. Stop for review.**

This preparation demonstrates a small, selective, anatomy-dependent resource effect
and a persistent local experience effect. It **does not establish persistence,
withdrawal or voluntary abstention**. All six primary cue/seed pairs miss the
prospective 10% MBON11 resource threshold and the joint 5% experience thresholds.
MBON11 low/high contrast is {pct(mincontrast)}–{pct(maxcontrast)}; low-resource
trial-dependent MBON11 decline is {pct(min(primaryexperience))}–{pct(max(primaryexperience))}.
LH experience change is only {pct(min(lhchange))}–{pct(max(lhchange))}.

The assumed inhibitory MBON11→MBON18 path also creates competing readout directions.
No sign-flipped, thresholded or fitted decision decoder was introduced to turn these
signals into “continue” or “give up.” The stronger learned-value × resource-state
claim is unsupported at the preregistered magnitude. No parameters, anatomical
selection, thresholds or neural equations were adjusted after the main battery began.

## Frozen prior work and scope

[FROZEN_BEFORE.json](FROZEN_BEFORE.json) records 1,025 files spanning both research
stages and Genesis core/data/runtime/server. [PRESERVATION.json](PRESERVATION.json)
records the final comparison. Stage-1 essential tests pass10/10; Stage-2 tests pass9/9;
both primary trained-state hashes reproduced exactly before Stage3 implementation.
Stage1 remains **PASS**, Stage2 remains **PARTIAL-INCONCLUSIVE**. Their models,
parameters, accepted results, reports, extractions and manifests were untouched.
The C. elegans adapter/connectome and the canonical organism/database remain
unchanged, with seven life cycles. No canonical cycle, migration or activation ran.

## BIOLOGICAL FACT

Experimental and crosswalk evidence is independently audited with authoritative
links in [LITERATURE.md](LITERATURE.md). It supports state-dependent MB computations
and identifies candidate PPL101/MBON11/MBON18/OA-VPM4 pathways, but not a universal
monotonic persistence readout. In particular, the original tracking experiments
explicitly leave MBON interaction and behavior relationships unresolved.
[Sayin et al., 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6839618/).

The peptide evidence supports a direction of motivational modulation, not a chemical
edge-count-derived receptor graph. Source neurons, peptide dose, receptor location,
co-transmission and compensatory physiology are not established by this extraction.
[Krashes et al., 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2780032/),
[Tsao et al., 2018](https://elifesciences.org/articles/35264),
[2024 compensatory reinforcement study](https://pubmed.ncbi.nlm.nih.gov/38795709/).

## Circuit and provenance

Adult female FAFB/FlyWire materialization783, annotationv3.1.0; source checksums and
licensing inherited from the audited original cache. Root IDs are strings, never
JavaScript numbers. The model is new and isolated. More KCs are needed here than
Stage2 because the target compartments involve γ and αβ populations. Neuron count
was not an objective and no post-result expansion occurred.

- **4,563 neurons; 304,192 directed pairs; 375,699 pair/neuropil rows;
  905,536 anatomical contacts.**
- 4,214 KCs,317 cholinergic ALPNs, two each MBON11/MBON18/PPL101/OA-VPM4/APL/LHCENT1,
  four each MBON07/MBON14,12 MBON18-connected PD2a1/b1 alias candidates.
- Experience plasticity: **4,203 KC→MBON11 pairs,5,278 efficacy variables,
  18,268 contacts**. Value context:3,619 KC→MBON07 pairs,9,407 efficacy variables,
  22,625 contacts. Value variables do not learn in Stage3.
- Of the value variables, exactly **4,622** receive copied historical efficacies in
  the transfer assay, with source/target/neuropil/contact count checked against the
  original Stage1 anatomy. No new synapse or teaching event is inserted.
- Overlap:1,041 Stage1 roots;268 Stage2 roots; **3,374 additional to their union**.
- Omitted: **597,746 incoming and1,012,673 outgoing proofread contacts**. Boundary
  artifacts contain every external root/contact row and per-class/type aggregates.

{boundary}

### Actual contacts on the proposed causal paths

{table(['Path','Contacts'],[[k,v] for k,v in paths.items()])}

OA→MBON11 is highly asymmetric:45 contacts from left-labelled OA to right-labelled
MBON11 and2 in the other direction; cell-side labels are not axonal territorial
boundaries. MBON11→MBON18 totals36 and MBON18→PD2 totals92: neither is a giant relay.
The PD2 alias population has only26.86% retained input, LHCENT1 only16.61%, and OA
only4.28%. This prevents a complete natural acquisition/pursuit claim. Direct OA
current bypasses those missing afferents; it must not be presented as their recovery.

All current CB cell types, hemibrain aliases, sides, known and predicted transmitters,
FBbt/VFB IDs and ambiguity notes are retained. PD2 alias membership is not exact
functional-driver membership; only12/16 annotated alias candidates have observed
MBON18 input and are selected. No NPF-named neuron was invented as a peptide source.
KCs use experimentally established cholinergic identity despite problematic automatic
transmitter predictions. LHCENT1 is modeled inhibitory, consistent with its GABA
annotation. Unresolved MBON07 glutamatergic outputs and non-MBON11 OA fast effects
are numerically zeroed, while their anatomical rows remain in the extraction.

Compartment localization remains coarse:16,494/18,268 experience-plastic contacts
carry MB_PED labels; remaining neuropil labels are fully enumerated in the anatomy
audit. Neither these region labels nor cell names prove molecular receptor placement.

## COMPUTATIONAL MODEL — what was assumed

[PLAN.md](PLAN.md) fixes parameters, thresholds and comparisons before simulations.
Float64 rate dynamics use dt10ms, fast tau50ms, KC threshold0.15, and eligibility
500ms. Weights are proportional to contacts, normalized by **all proofread input**
at each target. Omitted inputs are silent. Conductances, gains and time constants
are not measured for this specimen.

A body-boundary variable obeys `dr/dt=(resource_input-r)/60s`, initialized0.2/0.8.
Only PPL101 responsiveness receives `g(r)=0.2+0.8r`. Lower resource reduces this
pathway's responsiveness. This is a directional dNPF-related approximation, **not
biological starvation, molecular NPF release or a persistence input**. There is no
PPL101 tonic injection. Its activity depends on retained neuronal inputs.

On observed KC→MBON11 rows, acute transmission is divided by `1+D`, where D is
contact-weighted activity from real PPL101→MBON11 contacts. Efficacy follows
`dm/dt=−0.08×KC_eligibility×D×m`, bounded0.1–1. These transfer functions are hypotheses.
Resource state does not directly set output, activity thresholds or learning rate.
OA stimulation inhibits MBON11 only through real OA→MBON11 contacts. No other OA
sign, receptor distribution or unobserved route is invented.

Persistent state contains rates, eligibility, per-edge efficacy, body state, clock,
PRNG and fingerprints. It contains no cue count, reward score, task appraisal,
continue/give-up flag or prose memory. The input stream contains numeric sensory
currents/timing, a bounded resource input, and specified OA currents in surrogate
acquisition arms. There is no LLM, database or product dependency.

## Protocol, baseline and resource counterbalancing

Seeds3701/3702/3703; equal-cardinality disjoint A/B PN patterns (16 roots each), fixed
amplitude1. Both resource conditions have **identical hashed sensory schedules**.
Twelve primary conditions run independently in seeded randomized order. Baseline
probes use disposable snapshot copies to avoid contaminating actual acquisition.

Ten12s contact periods start0,24,…,216s, total240s. Early contacts yield no
acquisition; absence of reward is not converted to a failure current or stop rule.
Primary readouts are raw dimensionless population rates during2–10s after onset;
additional onset, tail, post-offset and single-neuron data are saved. These are not
spike frequencies, measured fly speed or motor decisions.

{baseline}

Relative resource contrast is `low/high−1`; experience is `trial10/trial1−1`.
Positive MBON11 resource contrast is the literature-direction test. Positive LH
experience change is an explicit candidate hypothesis, not an established universal
pursuit decoder.

{comparison}

The raw state effect is selective: PN/KC responses are nearly unchanged, not globally
amplified. But it is small and downstream state effects have the opposite sign.
Maintained responses remain throughout unrewarded cue periods; simply responding
to a maintained sensory current is not evidence of autonomous pursuit.

## Intervention battery

All conditions start with intact-normalization denominators; lesion weights are
zeroed afterwards, never renormalized. Percentage reduction is relative to intact
MBON11 resource contrast for the same cue. Undefined means the required baseline
is absent; it is not counted as selective learning success.

{controls}

PPL101 silencing, local dopamine-gate removal and frozen resource modulation test
the causal route. Frozen plasticity separately tests experience, and MBON11/18
lesions test candidate downstream transmission. The MBON14 matched lesion uses one
cell per hemisphere and is matched in count, not centrality. MBON14 is not claimed
biologically independent of hunger; it is outside the particular modeled direct gate.
PN→KC removal destroys sensory drive, so it cannot count as selective persistence
loss. PN strength shuffling changes weights only on existing anatomical rows and
never fabricates topology. A surviving shuffled effect shows dependence on a motif,
not unique necessity of the exact biological weight distribution.

The global-gain negative control deliberately applies the resource factor throughout
the network. Its sensory changes disqualify it; the evaluator does not call it
motivational selectivity. No tonic-current rescue or post-outcome weight scaling was
introduced. Boundary lesions silence/remove only observed pathways.

## Acquisition, interruption and abstention limits

Acquisition-surrogate arms apply OA current0.5 from224–228s while the PN cue continues.
This is experimental direct-neuron stimulation, not natural taste transduction.
Suppression below is `1−acquisition/control`; a negative value means activation.

{acquisition}

OA suppresses MBON11 by5.5–6.3%, but slightly increases MBON18/LH output. It therefore
fails the joint20% pursuit-candidate suppression criterion. OA silencing removes
its modeled MBON11 effect but does not resolve the contradictory downstream readout.
This does not establish disengagement. Physical cue interruption removes the sensory
input and consequently neural responses; it is not a threat mechanism or learned
withdrawal. Sham remains silent: absence of activity is not an autonomous abstention
decision. No threat, competing-action policy or motor circuit was added.

## Persistence vs decay, adaptation and imposed drive

{timing}

Measured post-offset activity is tiny compared with maintained-cue activity; there
is no demonstrated long autonomous after-discharge. The25/50/75% duration sweep
illustrates maintained cue following and cannot rescue failed raw experience metrics.
Single-last-contact controls match total elapsed time; the small ten-vs-single
change reflects efficacy history, not just more elapsed simulation time. Fast tau
half/double tests are reported below and do not turn slower decay into persistence.

No sensory-adaptation variable exists in this model. PN/KC preservation and plasticity
freeze distinguish the recorded effect from global sensory fatigue within this
implementation, not from every possible real-fly adaptation mechanism. Resource
input alone generates zero neural activity in sham and analytic body-state tests.
There is no externally imposed tonic neural drive in primary conditions.

## Snapshot, reset and replay

All original snapshots restore the saved baselines. All12 primary acquisitions
replay bit-identically, and36 clean-environment fresh-process recalls reproduce
trained/fast-reset/original readouts exactly. Fast reset retains body and plastic
state; largest primary recall difference is **{maxreset:.6g}**, below1e−10.
Cue-only recall after reset retains a MBON11 decrease of
{pct(min(persistence))}–{pct(max(persistence))} from baseline. Thus a genuine modeled
neural/plastic history effect exists even though persistence acceptance fails.

Body-swap probes separately retain the same efficacies while changing current body
state. They do not turn that resource value into an external decision. Body dynamics
are validated against the60s relaxation equation; primary high/low assays start at
steady resource levels and do not simulate metabolic starvation or energy spending.
No cross-platform bitwise guarantee is made;1e−10 is the compatible-environment
numerical tolerance, not a timestep-convergence assertion.

## Learned association × current state

{factorial}

The four VALUE neurons' mean response is shown; only the two original Stage1 output
roots have imported training. The assay preserves a large learned-response difference
in this new context. However, the normalized mixed difference is only approximately
1.74e−6% (cueA) /2.27e−6% (cueB), far below5%. It disappears under the PPL101/MBON11/
frozen-modulation controls but is near numerical-tolerance scale in absolute units.
The stronger claim is therefore **unsupported**, not evidence of useful value-state
multiplication. Resource effects largely add to, rather than modulate, the learned
response difference. No permanent preference field or new Stage1 learning was used.

This is a test of transferred efficacies in a **new network context**, not a change
to Stage1 or proof of physiological transfer between brains. The broader appetite
network and peptide/body inputs are incomplete. A lack of strong interaction here
does not show that biological reward memory is state-independent.

## Parameter and boundary sensitivity

{ sensitivity }

All variants were scheduled before the main outcomes. Retained-total and
retained-role normalizations are optimistic alternative assumptions, not replacements
for the all-input primary. No induced current compensates for omitted input.
OA-gain variants use the acquisition arm; other variants use the unrewarded arm.
Full threshold-free effects and sensitivity are reported even if their sign changes,
baselines vanish or large gains saturate activity. No variant can retroactively
replace the failed primary criteria.

## Prespecified acceptance audit

{results_table}

The classification reflects the joint criteria, not the fact that tests execute.
Selective pathway effects alone are insufficient to establish persistence or a
coherent disengagement readout.

## Performance, execution and genuine artifacts

The122-condition battery plus12 full primary replays used
**{p['wall_seconds']:.2f}s total elapsed wall time** including the checkpoint transition.
The first{p.get('preserved_serial_conditions',0)} complete serial conditions were preserved
byte-for-byte; the remaining{p.get('parallel_conditions',0)} ran with four local workers
in{p.get('parallel_phase_seconds',0):.2f}s. Only orchestration changed; the exact neural
model, protocols and parameters stayed fixed. Completed-run hashes are included.
Each acquisition advances240 simulated seconds, including quiet/contact intervals;
this is not a claim of continuous autonomous motor behavior.

Measured peak worker RSS: **{p.get('peak_worker_rss_bytes',0)/2**20:.2f}MiB**; coordinator peak:
{p.get('peak_coordinator_rss_bytes',0)/2**20:.2f}MiB. The conservative concurrent-process
upper bound is{p.get('concurrent_rss_upper_bound_bytes',0)/2**20:.2f}MiB, computed from per-process
peaks, **not a sampled combined peak**. Serial-worker peak was not captured before
checkpointing. The learned-state assay took{lv['performance']['wall_seconds']:.2f}s and
{lv['performance']['peak_rss_bytes']/2**20:.2f}MiB peak RSS. Hardware/environment metadata is
saved with evidence; these are local measurements, not cloud service guarantees.

- [Circuit manifest](artifacts/{a['circuit']}/manifest.json)
- [Anatomical audit]({ap.relative_to(HERE)})
- [All122 condition records](evidence/{ep.name}/results.json)
- [Acceptance evaluation]({criteria_path})
- [Learned-state evidence](learned-evidence/{lp.name}/results.json)
- [Comparison CSV](RESULTS.csv)
- [Reproduction instructions](README.md)

Actual group activity is sampled every100ms; two dense runs save individual neurons
and all efficacies every1s. Snapshots/integration use float64; dense traces use
float32. Per-neuron probe arrays and all initial/trained/reset states are saved.
There is no fabricated activity or visualization. Artifacts are content-addressed
and checked on load; hash immutability is not filesystem write-once protection.

Implementation checks pass11/11. Scientific acceptance is separately reported above.
Source licensing remains the inherited caveat: Zenodo metadata CC-BY4.0, FlyWire
site/VFB guidance CC-BY-NC4.0, annotation terms not independently resolved. This
work is isolated local research, not commercial data publication or deployment.

## Review decision and remaining uncertainty

This experiment has no validated mapping to continue pursuing, disengage or choose
inactivity. Missing LH/OA inputs, cross-specimen driver aliases, unknown receptor
transfer functions, omitted nitric oxide/peptide physiology, simple point-neuron
APL, fixed synthetic cues and absent descending/VNC/body control are substantive
limits. Cell-type-gated efficacy is not verified subcellular receptor anatomy.
The resource variable is a declared computational boundary, not biological hunger.

**GENESIS MAPPING: none. Stage1 remains PASS; Stage2 remains PARTIAL-INCONCLUSIVE.**
Stage3 ends here with **{a['classification']}**. No further circuit expansion,
threat/sleep/arousal experiment, BrainAdapter migration or Genesis integration is
performed. Further investigation requires a separate review of these results.
'''
    plastic_rows=[]
    for r in sorted(rs,key=lambda r:r['run']):
        q=r['cue'];initial=r['baseline'][q]['groups']['MB11'];reset=r['fast_reset'][q]['groups']['MB11']
        swapped=r['body_swap_same_weights'][q]['groups']['MB11']
        plastic_rows.append([r['run'],r['plastic_rows_changed'],num(r['max_plastic_change']),
                             pct(reset/initial-1),pct(swapped/reset-1)])
    plastic_table=table(['Condition','Changed efficacy rows (>1e-12)','Largest efficacy decrease',
                         'Reset recall / baseline − 1','Body swap / reset recall − 1'],plastic_rows)
    report=report.replace('## Learned association × current state',
        '### Plastic-state and body-swap measurements\n\n'+plastic_table+'\n\n'
        'Efficacy decrease is an absolute change from the initial multiplier of 1. '
        'The body-swap column holds the trained weights fixed and changes the current '
        'resource boundary to the opposite level. It measures the acute component; '
        'it does not recondition the model.\n\n## Learned association × current state')
    report=report.replace('## Prespecified acceptance audit',
        'For cue A, modest unrewarded variants retain the resource-effect direction, '
        'but span 0.0207–0.0946%, still below 10%. Retained-total normalization gives '
        '0.0970%; retained-role normalization nearly abolishes the effect '
        '(7.38e−7%). Thus direction alone does not establish robust magnitude. '
        'Removing APL increases the primary contrast by approximately 2.3–2.5% '
        'relative; removing LH feedback changes it negligibly. These controls '
        'cannot establish that unknown omitted inputs would be harmless.\n\n'
        '## Prespecified acceptance audit')
    report=report.replace('The classification reflects the joint criteria, not the fact that tests execute.',
        'The evaluator also reports stricter diagnostic checks: exact-zero sham '
        'instead of the prospectively allowed <1% response, and 80% downstream '
        'interaction reduction where the plan required a reduction without a numeric '
        'cutoff. Both stricter checks pass; neither changes the classification. '
        'The four failed magnitude criteria above are explicitly prospective.\n\n'
        'The classification reflects the joint criteria, not the fact that tests execute.')
    # Presentation-only spacing. Scientific names, identifiers, links and data stay intact.
    report=re.sub(r'\bStage([123])\b',r'Stage \1',report)
    report=re.sub(r'\b(pass|passes|before|after|below|above|only|and|all|All|by|from|in|first|remaining|every|took|is|The|the|joint|advances|totals|seeds|Seeds|at|initialized|bounded|tau|dt|current|amplitude|gain|input|periods|materialization|annotation)(?=\d)',r'\1 ',report)
    report=re.sub(r'(?<=\d)(MiB|ms|s)\b',r' \1',report)
    report=re.sub(r',(?!\d{3}(?:\D|$))(?=\d)',', ',report)
    report=report.replace('contrast is 0.', 'contrast is 0.').replace('context:3', 'context: 3').replace('Overlap:1', 'Overlap: 1')
    (HERE/'REPORT.md').write_text(report)
    (HERE/'LEARNED_INTERACTIONS.json').write_text(json.dumps(interactions,indent=2)+'\n')
    print('Rendered final report from verified evidence.')

if __name__=='__main__':main()
