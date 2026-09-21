"""FROZEN, UNEXECUTED Stage-5 mathematical analysis code.

No neural model, physical observation conversion, numerical transfer fitting,
random sweep or behavioral decoder. Do not import/call during protocol design.
Executing this module requires a separate reviewed authorization record.
"""
from pathlib import Path
from decimal import Decimal, getcontext
import json
import hashlib
import argparse

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        while block:=stream.read(4194304):h.update(block)
    return h.hexdigest()

def read(path,numeric=False):
    with Path(path).open() as stream:
        return json.load(stream,parse_float=Decimal if numeric else float)

def canonical(value):
    return (json.dumps(value,sort_keys=True,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()

def require_authorization(path):
    if path is None:raise ValueError('Separate execution authorization is required.')
    p=Path(path).resolve()
    if HERE in p.parents:raise ValueError('Authorization must be outside the sealed protocol.')
    release=read(HERE/'RELEASE.json')
    expected=hashlib.sha256(json.dumps(release['files'],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    if expected!=release['content_sha256']:raise ValueError('Release digest mismatch.')
    a=read(p)
    if a.get('decision')!='AUTHORIZE ARCHIVED STAGE5 MATHEMATICAL ANALYSIS':raise ValueError('Wrong authorization scope.')
    if a.get('reviewed_content_sha256')!=expected:raise ValueError('Authorization names another release.')
    if not isinstance(a.get('explicit_user_authorization_reference'),str) or not a['explicit_user_authorization_reference'].strip():raise ValueError('Missing explicit user authorization reference.')
    for rel,h in release['files'].items():
        if digest(HERE/rel)!=h:raise ValueError('Protocol changed: '+rel)
    return release

def source_signs(left,right,epsilon):
    # Stored equality, never a physiological equality claim.
    delta=left-right
    if delta==0:return {0},False
    if abs(delta)<=epsilon:return {-1,0,1},True
    return ({1} if delta>0 else {-1}),False

def conditional_signs(source,operator):
    if operator=='zero':return {0}
    if operator=='increasing':return set(source)
    if operator=='decreasing':return {-s for s in source}
    if operator=='weak_increasing':return set(source)|{0}
    if operator=='weak_decreasing':return {-s for s in source}|{0}
    if operator in ('heterogeneous','arbitrary'):
        return {0} if source=={0} else {-1,0,1}
    raise ValueError('Nonpreregistered transfer operator.')

def family_sets(source,families):
    result={}
    for f in families:
        if f['id']=='E' or f.get('nuisance')=='unrestricted':result[f['id']]=[-1,0,1]
        else:result[f['id']]=sorted(conditional_signs(source,f['operator']))
    return result

def labels(sets):
    full=sets['E'];out=[]
    if len(full)==1:out.append('ROBUST ACROSS DECLARED EVIDENCE-ADMISSIBLE FAMILY')
    elif any(len(v)==1 for k,v in sets.items() if k not in ('E','N')):out.append('ROBUST ONLY UNDER RESTRICTED CONDITIONAL FAMILY')
    if len(full)>1 or len({tuple(v) for v in sets.values()})>1:out.append('TRANSFER-SENSITIVE / NON-ROBUST')
    if 0 in full:out.append('NULL-COMPATIBLE')
    return out

def validate_summary(row,s,parameters):
    parts=row['run'].split('-');variant='-'.join(parts[3:])
    if s['target']!='app' or s['seed']!=int(parts[1]) or s['paired']!=parts[2]:raise ValueError('Source identity mismatch.')
    expected='intact' if variant=='unpaired' else variant
    if s['intervention']!=expected or s['unpaired_teaching']!=(variant=='unpaired'):raise ValueError('Control identity mismatch.')
    if s['parameters']!=parameters:raise ValueError('Source model parameters changed.')
    if s['restoration_exact'] is not True:raise ValueError('Original snapshot restoration not exact.')
    if variant=='intact' and parts[1]=='1701' and s['replay_exact'] is not True:raise ValueError('Required original neural replay evidence absent.')
    for state in row['state_fields']:
        for cue in row['cues']:
            for group in ('MBON_app','PN','KC'):
                value=s[state][cue][group]
                if isinstance(value,bool) or not isinstance(value,(int,Decimal)) or not Decimal(value).is_finite():raise ValueError('Missing/nonfinite source readout.')

def control_gate(inputs,summaries,index,epsilon,family):
    checks=[]
    for row in inputs:
        name=row['run'];s=summaries[name];paired=s['paired']
        if name.endswith('-intact'):
            for contrast in ('response_change','plastic_state_retention'):
                signs=index[(name,paired,contrast)]['families'][family]
                checks.append({'run':name,'check':contrast+'_excludes_zero','passed':0 not in signs})
            checks.append({'run':name,'check':'restoration_equal','passed':index[(name,paired,'restoration_check')]['families'][family]==[0]})
        if any(name.endswith('-'+x) for x in ('freeze','silence_dan','remove_da_contacts','unpaired')):
            checks.append({'run':name,'check':'mechanism_or_timing_control_zero','passed':index[(name,paired,'response_change')]['families'][family]==[0]})
        if name.endswith('-intact') or any(name.endswith('-'+x) for x in ('freeze','silence_dan','remove_da_contacts','unpaired')):
            for cue in ('A','B'):
                for group in ('PN','KC'):
                    equal=abs(Decimal(s['post'][cue][group])-Decimal(s['baseline'][cue][group]))<=epsilon
                    checks.append({'run':name,'cue':cue,'check':group+'_sensory_stability','passed':equal})
    return {'family':family,'checks':checks,'verdict':'SATISFIED UNDER DECLARED CONDITIONAL FAMILY' if all(c['passed'] for c in checks) else 'NOT SATISFIED',
            'scope':'Archived model-dependence gate only. No biological mediation or strict cue-exclusive downstream inference.'}

def execute_authorized(authorization,output):
    # Authorization and integrity gates precede all source-summary value reads.
    release=require_authorization(authorization)
    out=Path(output).resolve();allowed=ROOT/'research/fly-stage5-runs'
    if allowed not in out.parents or out.exists():raise ValueError('Use a new separate directory beneath research/fly-stage5-runs.')
    protected=read(HERE/'PRESERVATION_MANIFEST.json')['files']
    for rel,h in protected.items():
        if digest(ROOT/rel)!=h:raise ValueError('Protected artifact changed: '+rel)
    lock=read(HERE/'STAGE1_INPUT_LOCK.json',numeric=True)
    families=read(HERE/'TRANSFER_FAMILIES.json')['families']
    if {f['id'] for f in families}!={'E','Z','P','R','WP','WR','H','U','N'}:raise ValueError('Family coverage differs from preregistration.')
    spec=read(HERE/'ESTIMANDS.json');precision=read(HERE/'ROBUSTNESS_DEFINITIONS.json')['numerics']
    epsilon=Decimal(precision['epsilon']);getcontext().prec=50
    units=[];summaries={};source_diagnostics=[]
    for row in lock['inputs']:
        for a in row['artifacts'].values():
            if digest(ROOT/a['path'])!=a['sha256']:raise ValueError('Stage1 source artifact hash mismatch.')
        s=read(ROOT/row['artifacts']['summary.json']['path'],numeric=True)
        validate_summary(row,s,lock['frozen_parameters']);summaries[row['run']]=s
        for cue in row['cues']:
            for contrast in spec['contrasts']:
                left=Decimal(s[contrast['left']][cue]['MBON_app']);right=Decimal(s[contrast['right']][cue]['MBON_app'])
                source,ambiguous=source_signs(left,right,epsilon);sets=family_sets(source,families)
                units.append({'run':row['run'],'cue':cue,'paired_cue':s['paired'],'contrast':contrast['id'],
                              'source_left':str(left),'source_right':str(right),'source_units':'dimensionless frozen model readout',
                              'source_sign_set':sorted(source),'numerical_ambiguity':ambiguous,'families':sets,'labels':labels(sets),
                              'counterexamples':'COUNTEREXAMPLE_REGISTRY.json; report all entries with this result; no conditional singleton is biological evidence.'})
            source_diagnostics.append({'run':row['run'],'cue':cue,'sensory_readouts':{state:{g:str(s[state][cue][g]) for g in ('PN','KC')} for state in row['state_fields']},
                                       'original_replay_exact':s['replay_exact'],'original_restoration_exact':s['restoration_exact']})
    if len(units)!=224:raise ValueError('Incomplete prospective unit coverage.')
    index={(u['run'],u['cue'],u['contrast']):u for u in units}
    gates=[control_gate(lock['inputs'],summaries,index,epsilon,f) for f in ('P','R')]
    counts={label:sum(label in u['labels'] for u in units) for label in read(HERE/'RESULT_CLASSIFICATION.json')['labels']}
    payload={'protocol_content_sha256':release['content_sha256'],'units':units,'unit_count':len(units),'label_counts':counts,
             'control_gate':gates,'source_diagnostics':source_diagnostics,'interpretation':'Conditional mathematical analysis only; full evidence family and all restricted branches reported.',
             'counterexample_registry':read(HERE/'COUNTEREXAMPLE_REGISTRY.json'),'neural_runs':0,'new_physical_observations':0,'capability_admissions':[]}
    data=canonical(payload)
    # Only a separately authorized result directory receives outputs.
    out.mkdir(parents=True,exist_ok=False)
    (out/'RESULTS.json').write_bytes(data)
    (out/'RESULTS.sha256').write_text(hashlib.sha256(data).hexdigest()+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser(description='Requires separate execution authorization; never run during protocol design.')
    p.add_argument('--authorization',required=True);p.add_argument('--output',required=True)
    args=p.parse_args()
    try:execute_authorized(args.authorization,args.output)
    except (ValueError,KeyError,TypeError,OSError) as error:
        raise SystemExit('UNINTERPRETABLE / NOT EXECUTED: '+str(error))
