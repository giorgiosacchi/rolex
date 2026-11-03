#!/usr/bin/env python3
"""Aggiorna SOLO il tessuto del cinturino JB, dal riferimento fotografico Goldfinger."""
from pathlib import Path
from io import BytesIO
from subprocess import check_output
from PIL import Image
from scipy.ndimage import gaussian_filter
import numpy as np

ROOT=Path(__file__).resolve().parent.parent
# Recupera sempre la fotografia JB originale per non accumulare rielaborazioni.
original=check_output(["git","show","af07880f55f19b84d5cd8254d1fb0c71391f1a64:assets/jb.webp"],cwd=ROOT)
A=np.asarray(Image.open(BytesIO(original)).convert("RGB"),dtype=np.float32)
h,w=A.shape[:2]
assert (w,h)==(1024,1536), "Dimensioni immagine diverse dall'atteso"
y,x=np.ogrid[:h,:w]
ring=((x-502)/405.0)**2+((y-703)/395.0)**2
zone=(((y<348)|(y>=1072))&(x>=275)&(x<=729)&(ring>1.005))
r,g,b=A[:,:,0],A[:,:,1],A[:,:,2]
olive=(g>r*.88)&(r>g*.75)&(b<g*.95)&(g<160)&(r<170)
red=(r>g*1.32)&(r>b*1.12)&(g<100)&(b<110)
navy=(b>r*1.04)&(b>g*1.03)&(r<110)&(g<120)
cloth=zone&(olive|red|navy)&(np.maximum.reduce([r,g,b])<165)
left_olive=(x>=369)&(x<=420)
right_olive=(x>=590)&(x<=642)
left_border=((x>=362)&(x<=368))|((x>=421)&(x<=427))
right_border=((x>=583)&(x<=589))|((x>=643)&(x<=649))
green=(left_olive|right_olive)&cloth
burgundy=(left_border|right_border)&cloth
black=cloth&~green&~burgundy
amp=np.clip(.299*r+.587*g+.114*b,5,130)
B=A.copy()
base=np.clip(4+amp*.38,5,52)
for i,offset in enumerate((0,0,2)):
    B[:,:,i][black]=np.clip(base[black]+offset,0,255)
ol=np.clip(8+amp*.37,11,62)
for i,fac in enumerate((.87,1.02,.80)):
    B[:,:,i][green]=np.clip(ol[green]*fac,0,255)
rd=np.clip(9+amp*.35,11,61)
for i,fac in enumerate((1,.42,.48)):
    B[:,:,i][burgundy]=np.clip(rd[burgundy]*fac,0,255)
mask=np.clip(gaussian_filter(cloth.astype(np.float32),sigma=.58),0,1)[...,None]
out=np.clip(A*(1-mask)+B*mask,0,255).astype("uint8")
Image.fromarray(out,"RGB").save(ROOT/"assets"/"jb.webp","WEBP",quality=94,method=6)
print(f"Aggiornati {cloth.sum():,} pixel del cinturino; cassa e quadrante preservati")

sw=ROOT/"sw.js"
content=sw.read_text()
if "rolex-live-dual-jb-v4" not in content:
    raise RuntimeError("Versione inattesa della cache PWA: interrompo per sicurezza")
sw.write_text(content.replace("rolex-live-dual-jb-v4","rolex-live-dual-jb-v5"))
print("Aggiornata cache PWA a v5")
