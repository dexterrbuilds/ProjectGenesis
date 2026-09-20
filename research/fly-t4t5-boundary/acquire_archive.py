"""Resumable public Figshare ranges. No data analysis; validate complete archive MD5."""
from pathlib import Path
import concurrent.futures as cf
import hashlib,json,subprocess,time,os

HERE=Path(__file__).resolve().parent
URL='https://ndownloader.figshare.com/files/30851668'
TOTAL=6320065220
MD5='cabf1b1c6d0ef4af200d41256e2835cf'
DEST=HERE/'data/Figure2.zip'
PARTS=HERE/'data/Figure2.parts'
PARTS.mkdir(exist_ok=True)
if DEST.exists() and DEST.stat().st_size==TOTAL:
    h=hashlib.md5()
    with DEST.open('rb') as f:
        while b:=f.read(1024*1024):h.update(b)
    assert h.hexdigest()==MD5
    print(json.dumps({'already_complete':True,'bytes':TOTAL,'md5':MD5}),flush=True)
    raise SystemExit(0)
INDEX=PARTS/'ranges.json'
if INDEX.exists():ranges=json.loads(INDEX.read_text())
else:
    start=DEST.stat().st_size if DEST.exists() else 0
    ranges=[(s,min(s+32*1024*1024,TOTAL)) for s in range(start,TOTAL,32*1024*1024)]
    INDEX.write_text(json.dumps(ranges))

def fetch(r):
    start,end=r;p=PARTS/f'{start}-{end}.part'
    for attempt in range(5):
        have=p.stat().st_size if p.exists() else 0
        if have==end-start:return p
        assert have<end-start
        tmp=p.with_suffix('.incoming');headers=p.with_suffix('.headers')
        cmd=['curl','-L','--fail','--silent','--show-error','--max-time','600','-r',f'{start+have}-{end-1}',
             '-D',str(headers),URL,'-o',str(tmp)]
        result=subprocess.run(cmd,capture_output=True,text=True)
        if tmp.exists() and tmp.stat().st_size:
            # Accept only the requested offset from an actual HTTP range response.
            h=headers.read_text().lower()
            assert f'content-range: bytes {start+have}-' in h,h
            assert tmp.stat().st_size<=end-start-have
            with p.open('ab') as dst,tmp.open('rb') as src:
                while b:=src.read(1024*1024):dst.write(b)
            tmp.unlink()
        if result.returncode:print(json.dumps({'range':r,'attempt':attempt,'error':result.stderr[-160:]}),flush=True)
    assert p.stat().st_size==end-start,(r,p.stat().st_size)
    return p

with cf.ThreadPoolExecutor(max_workers=8) as pool:
    for i,p in enumerate(pool.map(fetch,ranges)):
        print(json.dumps({'complete_ranges':i+1,'of':len(ranges)}),flush=True)

with DEST.open('ab') as dst:
    for start,end in ranges:
        pos=dst.tell()
        if pos>=end:continue
        assert pos==start
        with (PARTS/f'{start}-{end}.part').open('rb') as src:
            while b:=src.read(1024*1024):dst.write(b)
assert DEST.stat().st_size==TOTAL
h=hashlib.md5()
with DEST.open('rb') as f:
    while b:=f.read(1024*1024):h.update(b)
assert h.hexdigest()==MD5
print(json.dumps({'complete':True,'bytes':TOTAL,'md5':MD5}),flush=True)
