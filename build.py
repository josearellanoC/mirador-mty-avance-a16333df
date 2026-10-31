#!/usr/bin/env python3
"""Rebuild index.html + img/ from data.json. Photos: /workspace/nas_backup/src/<id> (original) or /workspace/inf5/h_<id>.jpg."""
import json,os,html
from PIL import Image,ImageOps
D=os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
d=json.load(open('data.json')); os.makedirs('img',exist_ok=True)
def src(i):
    for p in (f'/workspace/nas_backup/src/{i}',f'/workspace/inf5/h_{i}.jpg'):
        if os.path.exists(p): return p
    raise SystemExit('falta foto '+i)
def make(i):
    t,f=f'img/t_{i}.jpg',f'img/f_{i}.jpg'
    if os.path.exists(t) and os.path.exists(f): return
    im=ImageOps.exif_transpose(Image.open(src(i))).convert('RGB')
    a=im.copy(); a.thumbnail((1600,1600),Image.LANCZOS); a.save(f,quality=82,optimize=True,progressive=True)
    b=im.copy(); b.thumbnail((400,400),Image.LANCZOS); b.save(t,quality=78,optimize=True)
rows=[];allf=[]
for lote,fs in d['fotos'].items():
    for (i,a,dt) in fs: make(i); allf.append(dict(t=f'img/t_{i}.jpg',f=f'img/f_{i}.jpg',l=lote,a=a,d=dt))
e=html.escape
def color(v):
    v=max(0,min(100,v or 0))/100
    c0=(243,238,232);c1=(196,106,42)
    r,g,b=[round(c0[j]+(c1[j]-c0[j])*v) for j in range(3)]
    return f'rgb({r},{g},{b})'
hm='<tr><th></th>'+''.join(f'<th class="h"><span>{e(h)}</span></th>' for h in d['hitos'])+'</tr>'
notas=[]
for lote,av in d['avance'].items():
    if av is None: notas.append(f'{lote} aún sin reportes.'); av={}
    hm+=f'<tr><th class="l">{e(lote)}</th>'+''.join(f'<td style="background:{color(av.get(h,0))}" title="{e(h)}: {av.get(h,0)}%"></td>' for h in d['hitos'])+'</tr>'
gal='';k=0
for lote,fs in d['fotos'].items():
    gal+=f'<h3>{e(lote)} · {fs[0][2]}</h3><div class="g">'
    for (i,a,dt) in fs:
        gal+=f'<img loading="lazy" src="img/t_{i}.jpg" alt="{e(lote)}, {e(a)}" data-k="{k}">';k+=1
    gal+='</div>'
logo=[f for f in os.listdir('img') if f.startswith('logo')][0]
out=open('template.html').read().replace('%LOGO%','img/'+logo).replace('%DIR%',e(d['direccion'])).replace('%CORTE%',d['corte']).replace('%HM%',hm).replace('%NOTAS%',' '.join(notas)).replace('%GAL%',gal).replace('%FOTOS%',json.dumps(allf,ensure_ascii=False))
open('index.html','w').write(out); print('ok',len(allf),'fotos')
