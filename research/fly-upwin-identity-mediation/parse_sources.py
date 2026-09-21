from common import *
from html.parser import HTMLParser
class P(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.text=[];self.links=[]
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
  if t=='a':
   d=dict(a)
   if d.get('href'):self.links.append(d['href'])
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip-=1
 def handle_data(self,d):
  if not self.skip and d.strip():self.text.append(d.strip())
for f in (HERE/'sources').glob('*.html'):
 p=P();p.feed(f.read_text(errors='replace'));(HERE/'sources'/f'{f.stem}.txt').write_text('\n'.join(p.text));write(f'sources/{f.stem}-links.json',sorted(set(p.links)))
