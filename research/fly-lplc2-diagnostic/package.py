"""Freeze/verify this diagnostic package without updating any dependency."""
import sys
from common import HERE, load, save, sha, digest

def files():
    return {str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*'))
            if p.is_file() and p.name!='PACKAGE_MANIFEST.json' and '__pycache__' not in p.parts and p.suffix!='.pyc'}

if __name__=='__main__':
    if '--freeze' in sys.argv:
        assert load('VALIDATION.json')['passed']
        assert all(load('REPRODUCTION.json')['comparisons'].values())
        assert load('PRESERVATION.json')['changed']==[]
        f=files();lock=load('DEPENDENCY_LOCK.json')
        save('PACKAGE_MANIFEST.json',{'study':'isolated LPLC2 visual computation diagnostic',
            'classification':'PARTIAL MECHANISTIC CONSTRAINT — MORE DATA REQUIRED',
            'brain_spec_registry_sha256':lock['brain_spec_sha256'],
            'stage4_content_sha256':lock['stage4_content_sha256'],
            'frozen_stage4':lock['stage4_classification'],'files':f,'content_sha256':digest(f),
            'new_neural_model':False,'stage4_reruns':0,'new_canonical_anatomy_ownership':False})
    m=load('PACKAGE_MANIFEST.json');f=files()
    assert f==m['files'],'Diagnostic package contents changed'
    assert digest(f)==m['content_sha256']
    print({'valid':True,'files':len(f),'content_sha256':m['content_sha256'],'classification':m['classification']})
