"""Read-only biological workbook analysis; no Stage-4 imports or response data."""
import sys
from pathlib import Path
import numpy as np
from common import HERE, load, save, sha
sys.path.insert(0,str(HERE/'vendor'))
import xlrd

def analyze():
    src=HERE/'data/contrast-source.xls'
    reg=load('SOURCE_DATA_REGISTRATION.json')
    assert sha(src)==reg['source_sha256']
    assert sha(HERE/'SOURCE_DATA_ADDENDUM.md')==reg['addendum_sha256']
    book=xlrd.open_workbook(src)
    s=book.sheet_by_name('Fig7g')
    headers=s.row_values(0)
    assert headers[2]=='Tm9_Control_ON_Fullfield_Mean_Amplitude_dF_F0'
    assert headers[4]=='Tm9_Control_Fly_Index'
    rows=[]
    for r in range(1,s.nrows):
        cells=[s.cell(r,c) for c in (0,2,4)]
        if all(c.ctype==xlrd.XL_CELL_EMPTY for c in cells):continue
        assert all(c.ctype==xlrd.XL_CELL_NUMBER and np.isfinite(c.value) for c in cells)
        off,on,fly=[c.value for c in cells]
        assert fly==int(fly)
        rows.append({'row':r+1,'fly':int(fly),'off':off,'on':on})
    flies=[]
    for f in sorted({r['fly'] for r in rows}):
        rs=[r for r in rows if r['fly']==f]
        flies.append({'fly':f,'rois':len(rs),'on':float(np.mean([r['on'] for r in rs])),
                      'off':float(np.mean([r['off'] for r in rs]))})
    y=np.array([f['on'] for f in flies]);pred=(y.sum()-y)/(len(y)-1)
    for f,p in zip(flies,pred):
        f.update(zero_prediction=0.,signed_prediction=float(p),
                 zero_squared_error=f['on']**2,signed_squared_error=(f['on']-p)**2)
    widths=[]
    def describe(name,values,reference):
        a=np.array(values,float)
        if not len(a):return dict(name=name,n=0,range=reference,reason='No numeric measurements supplied')
        assert np.isfinite(a).all()
        return dict(name=name,n=len(a),mean=float(a.mean()),median=float(np.median(a)),
                    minimum=float(a.min()),maximum=float(a.max()),unit='degree',range=reference,
                    independent_fly_count='unknown; ROI-level summary only')
    s=book.sheet_by_name('Fig4j-m')
    for r in range(s.nrows):
        if s.cell_type(r,0)!=xlrd.XL_CELL_TEXT:continue
        vals=[s.cell_value(r,c) for c in range(1,s.ncols) if s.cell_type(r,c)==xlrd.XL_CELL_NUMBER]
        widths.append(describe(s.cell_value(r,0),vals,f"Fig4j-m!B{r+1}:{xlrd.formula.colname(s.ncols-1)}{r+1}"))
    s=book.sheet_by_name('Fig6f')
    for c in range(s.ncols):
        vals=[s.cell_value(r,c) for r in range(1,s.nrows) if s.cell_type(r,c)==xlrd.XL_CELL_NUMBER]
        widths.append(describe(s.cell_value(0,c),vals,f"Fig6f!{xlrd.formula.colname(c)}2:{xlrd.formula.colname(c)}{s.nrows}"))
    return {'source':{'doi':'10.1038/s41467-021-24986-w','sha256':sha(src),
            'sheet':'Fig7g','ranges':['A2:A71','C2:C71','E2:E71'],
            'unit':'dF/F0','response':'authors mean during full-field stimulus; no new time-window selection',
            'species':'Drosophila melanogaster','sex':'female','age_days':'1–7',
            'preparation':'in vivo right optic-lobe two-photon GCaMP6f; no CDM for analysis',
            'stimulus':'2 s ON/OFF full-field flashes; 4 s intermediate background',
            'root_crosswalk':'class Tm9 only; recorded ROIs not individually matched to FAFB'},
            'selection':'all 70 supplied control ROIs; no response exclusion; equal weight per fly',
            'roi_rows':rows,'flies':flies,'n_flies':len(flies),'n_rois':len(rows),
            'mean_on_fly_weighted':float(y.mean()),'mean_off_fly_weighted':float(np.mean([f['off'] for f in flies])),
            'zero_model_parameters':0,'signed_model_parameters':1,
            'zero_lofo_mse':float(np.mean(y*y)),'signed_lofo_mse':float(np.mean((y-pred)**2)),
            'signed_improves_folds':int(np.sum((y-pred)**2<y*y)),
            'validation':'leave one biological fly out; seven folds; not an independent laboratory replication',
            'inference_limit':'Observation-level restriction only. No parameter transfers, neural kernel or Stage-4 predictions.',
            'widths':widths}

if __name__=='__main__':
    out=analyze();save('INDEPENDENT_RESULTS.json',out)
    print({k:out[k] for k in ('n_flies','n_rois','mean_on_fly_weighted','mean_off_fly_weighted','zero_lofo_mse','signed_lofo_mse','signed_improves_folds')})
