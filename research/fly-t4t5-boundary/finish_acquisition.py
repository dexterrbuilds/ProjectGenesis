from common import *
import zipfile,shutil,time
p=HERE/'data/Figure2.zip';h=hashlib.md5();t=time.perf_counter()
with p.open('rb') as f:
 while b:=f.read(4*1024*1024):h.update(b)
assert p.stat().st_size==6320065220 and h.hexdigest()=='cabf1b1c6d0ef4af200d41256e2835cf'
# Remove only redundant task-created transport chunks after byte-for-byte validation against the full archive.
released=0
with p.open('rb') as f:
 for a,b in json.loads((HERE/'data/Figure2.parts/ranges.json').read_text()):
  part=HERE/f'data/Figure2.parts/{a}-{b}.part'
  if not part.exists():continue
  f.seek(a);expected=hashlib.sha256(f.read(b-a)).hexdigest();assert sha(part)==expected
  released+=part.stat().st_size;part.unlink()
member='Figure2/singleBarStT5.mat';dest=HERE/'data/wholecell/singleBarStT5.mat'
with zipfile.ZipFile(p) as z:
 info=z.getinfo(member)
 if not dest.exists():
  tmp=dest.with_suffix('.part')
  with z.open(member) as src,tmp.open('wb') as out:shutil.copyfileobj(src,out,1024*1024)
  assert tmp.stat().st_size==info.file_size;tmp.rename(dest)
 write('T5_MEMBER_PROVENANCE.json',{'source':'https://ndownloader.figshare.com/files/30851668','member':member,'sha256':sha(dest),'size':info.file_size,'crc32':info.CRC,'member_size_and_crc_verified':True,'whole_archive_md5_verified':True})
write('ACQUISITION_COMPLETE.json',{'archive':str(p.relative_to(HERE)),'bytes':p.stat().st_size,'published_md5':h.hexdigest(),'sha256':sha(p),'whole_archive_verified':True,'redundant_transport_bytes_removed_after_validation':released,'original_T5_2019_archive_partial_not_used':True,'wall_seconds':time.perf_counter()-t})
print('Archive and T5 member verified; duplicate transport chunks released',released)
