"""Recover a complete CRC-checked ZIP member from preserved public byte ranges."""
from common import *
import struct,zlib,bisect,time
ranges=json.loads((HERE/'data/Figure2.parts/ranges.json').read_text());prefix=HERE/'data/Figure2.zip';segments=[(0,prefix.stat().st_size,prefix)]
for a,b in ranges:
 p=HERE/f'data/Figure2.parts/{a}-{b}.part'
 if p.exists() and p.stat().st_size==b-a:segments.append((a,b,p))
starts=[x[0] for x in segments]
def chunks(a,b):
 while a<b:
  i=bisect.bisect_right(starts,a)-1;s,e,p=segments[i];assert s<=a<e,(a,s,e)
  with p.open('rb') as f:
   f.seek(a-s)
   while a<min(e,b):
    data=f.read(min(1024*1024,min(e,b)-a));assert data;a+=len(data);yield data
entry=next(x for x in json.loads((HERE/'metadata/figure2-directory.json').read_text()) if 'singleBarStT4' in x.get('name',''))
print(entry)
header=b''.join(chunks(entry['offset'],entry['offset']+30));fields=struct.unpack('<IHHHHHIIIHH',header);assert fields[0]==0x04034b50
begin=entry['offset']+30+fields[-2]+fields[-1];dest=HERE/'data/wholecell/singleBarStT4.mat';tmp=dest.with_suffix('.part');crc=0;h=hashlib.sha256();n=0;t=time.perf_counter();dec=zlib.decompressobj(-15)
with tmp.open('wb') as f:
 for b in chunks(begin,begin+entry['compressed']):
  out=dec.decompress(b);f.write(out);crc=zlib.crc32(out,crc);h.update(out);n+=len(out)
 out=dec.flush();f.write(out);crc=zlib.crc32(out,crc);h.update(out);n+=len(out)
assert dec.eof and n==entry['size'] and crc==entry['crc'],(n,crc)
tmp.rename(dest)
write('T4_MEMBER_PROVENANCE.json',{'source':'https://ndownloader.figshare.com/files/30851668','zip_member':entry,'sha256':h.hexdigest(),'member_size_and_crc_verified':True,'whole_archive_md5_verified':False,'uncompressed_bytes':n,'wall_seconds':time.perf_counter()-t})
print('T4 member CRC and size verified',n)
