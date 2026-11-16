import re, json, sys, os, shutil
from bs4 import BeautifulSoup
from PIL import Image
D, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT+'/img', exist_ok=True)
h=open(D+'/s.html').read()
def txt(e): return re.sub(r'\s+',' ',e.get_text(' ')).strip()
used={}
def fix_imgs(soup):
    for im in soup.find_all('img'):
        src=im.get('src',''); base=os.path.basename(src); stem,ext=os.path.splitext(base)
        if ext.lower() in ('.emf','.wmf'):
            srcf=f'{D}/png/{stem}.png'; out=stem+'.png'
        else:
            srcf=f'{D}/media/{base}'; out=stem+('.jpg' if ext.lower() in ('.jpeg','.jpg') else '.png')
        if out not in used and os.path.exists(srcf):
            i=Image.open(srcf)
            if i.mode in ('P','RGBA','LA') and out.endswith('.jpg'): i=i.convert('RGB')
            if i.mode=='CMYK': i=i.convert('RGB')
            if i.width>900: i=i.resize((900,int(i.height*900/i.width)))
            if out.endswith('.jpg'): i.convert('RGB').save(OUT+'/img/'+out,quality=82,optimize=True)
            else: i.save(OUT+'/img/'+out,optimize=True)
            used[out]=1
        alt=im.get('alt','')
        if alt.startswith('Vaizdo rezultatas') or alt.startswith('http') or alt.startswith('Susijęs'): alt='Iliustracija'
        new=soup.new_tag('img', src='img/'+out, alt=alt or 'Iliustracija', loading='lazy')
        im.replace_with(new)
def clean(fragment):
    s=BeautifulSoup(fragment,'html.parser')
    fix_imgs(s)
    for t in s.find_all(True):
        for a in list(t.attrs):
            if a not in ('src','alt','loading','href','colspan','rowspan','start','type'): del t[a]
    for t in s.find_all(['h1','h2','h3']):
        if not txt(t) and not t.find('img'): t.decompose()
        else: t.name='p'
    for t in s.find_all(['colgroup']): t.decompose()
    for a in s.find_all('a'): a['target']='_blank'; a['rel']='noopener'
    # strip empty paragraphs
    for p in s.find_all('p'):
        if not txt(p) and not p.find('img'): p.decompose()
    return str(s).strip()
def strip_prefix(t): return re.sub(r'^\s*([A-F]|\d)[\.\)]\s+','',t).rstrip(';. ').strip()

# ---- pre test
a=h.find('PRADEDANT MOKYTIS'); b=h.find('Bendrosios veiklos',a)
s=BeautifulSoup(h[a:b],'html.parser'); pre=[]; cur=None
for ol in s.find_all('ol'):
    if ol.get('type')=='1':
        for li in ol.find_all('li',recursive=False): cur={'q':txt(li),'o':[]}; pre.append(cur)
    else:
        for li in ol.find_all('li',recursive=False): cur['o'].append(txt(li))
prekey={1:'A',4:'E',7:'A',10:'F',2:'B',5:'D',8:'A',11:'C',3:'B',6:'A',9:'E',12:'A,B,C'}
for i,q in enumerate(pre,1): q['a']=[ord(x.strip())-65 for x in prekey[i].split(',')]

# ---- final test
a=h.find('BAIGUS PROGRAM'); b=h.find('Atsakymai',a)
s=BeautifulSoup(h[a:b],'html.parser')
fin=[]
for tbl in s.find_all('table'):
    if tbl.find_parent('table'): continue
    body=tbl.find('tbody') or tbl
    for tr in body.find_all('tr',recursive=False):
        td=tr.find_all(['td','th'],recursive=False)
        if len(td)<3 or not txt(td[0]).isdigit(): continue
        c=td[2]
        lis=c.find_all('li')
        if lis: items=lis
        else: items=[p for p in c.find_all('p') if txt(p) or p.find('img')]
        has_img=bool(c.find('img'))
        opts=[]
        for it in items:
            if has_img: opts.append(clean(str(it)))
            else: opts.append(strip_prefix(txt(it)))
        qh=clean(td[1].decode_contents())
        fin.append({'n':int(txt(td[0])),'q':qh,'o':opts,'html':has_img})
a=h.find('BAIGUS PROGRAM',200000); b=h.find('</table>',a)
s=BeautifulSoup(h[a:b+8],'html.parser'); key={}
for tr in s.find_all('tr'):
    c=[txt(x) for x in tr.find_all(['td','th'])]
    for k in range(0,len(c)-1,2):
        if c[k].isdigit(): key[int(c[k])]=c[k+1]
fin=[q for q in fin if q['n'] not in (48,52)]  # figure lost in source
for q in fin: q['a']=[ord(x)-65 for x in re.findall(r'[A-F]',key[q['n']])]
print('pre',len(pre),'fin',len(fin),[q['n'] for q in fin][:3],file=sys.stderr)
for q in fin:
    if len(q['o'])<2 or max(q['a'])>=len(q['o']): print('ISSUE',q['n'],q['o'][:4],q['a'],file=sys.stderr)

# ---- tasks
def split_tasks(start,end):
    seg=h[start:end]
    marks=[]
    for m in re.finditer(r'Modulis\s+„([^“]+)“',seg): marks.append((m.start(),'M',re.sub(r'\s+',' ',m.group(1))))
    for m in re.finditer(r'(?:<em>)?(\d+)\s*užduotis\.?',seg): marks.append((m.start(),'T',int(m.group(1))))
    marks.sort()
    def tagstart(p):
        return max(seg.rfind('<p',0,p), seg.rfind('<h1',0,p))
    mods=[]; cur=None; tasks=[]
    tpos=[]
    for p,k,v in marks:
        if k=='M':
            mods.append({'name':v,'tasks':[]}); tpos.append((tagstart(p),None,None))
        else:
            if not mods: continue
            tpos.append((tagstart(p),len(mods)-1,v))
    # heat-pump module heading in answers may be fine now
    res={}
    for i,(p,mi,num) in enumerate(tpos):
        if mi is None: continue
        q=tpos[i+1][0] if i+1<len(tpos) else len(seg)
        frag=seg[p:q]
        res[(mods[mi]['name'],num)]=frag
    return [m['name'] for m in mods],res
ws=h.find('Bendrosios veiklos')-60; we=h.find('BAIGUS PROGRAM')-200
ans_s=h.find('PRADEDANT MOKYTIS ATSAKYMAI'); ans_e=h.find('BAIGUS PROGRAM',200000)-200
wmods,wt=split_tasks(ws,we)
amods,at=split_tasks(ans_s,ans_e)
print(wmods,amods,file=sys.stderr)
modules=[]
for mn in wmods:
    if 'darbo rinką' in mn: continue
    tasks=[]
    for (m,num),frag in wt.items():
        if m!=mn: continue
        fs=BeautifulSoup(frag,'html.parser')
        first=fs.find(['p','h1'])
        title=txt(first) if first else f'{num} užduotis'
        if first: first.decompose()
        title=re.sub(r'^\d+\s*užduotis\.?\s*','',title).strip(' .')
        qh=clean(str(fs))
        ah=None
        if (m,num) in at:
            af=BeautifulSoup(at[(m,num)],'html.parser'); f2=af.find(['p','h1'])
            if f2: f2.decompose()
            ah=clean(str(af))
        tasks.append({'n':num,'title':(title.capitalize() if title.isupper() else title).replace('Švok','ŠVOK'),'q':qh,'a':ah})
    tasks.sort(key=lambda t:t['n'])
    modules.append({'name':mn,'tasks':tasks})
    print(mn,len(tasks),sum(1 for t in tasks if t['a']),file=sys.stderr)
missing=[k for k in at if k not in wt]; print('ans w/o task',missing,file=sys.stderr)
data={'pre':pre,'fin':fin,'modules':modules}
open(OUT+'/data.js','w').write('window.SVOK='+json.dumps(data,ensure_ascii=False)+';\n')
print('imgs',len(used),file=sys.stderr)
