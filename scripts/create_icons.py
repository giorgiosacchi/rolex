#!/usr/bin/env python3
"""Genera icone PWA dalla fotografia originale del quadrante Rolex."""
from pathlib import Path
from PIL import Image, ImageOps

root=Path(__file__).resolve().parent.parent
image=Image.open(root/'assets'/'rolex.png').convert('RGB')
w,h=image.size
# Quadrante centrato circa in (48% della larghezza, 50% dell'altezza).
cx,cy=w*0.485,h*0.498
side=min(w*0.91,h*0.62)
square=image.crop((int(cx-side/2),int(cy-side/2),int(cx+side/2),int(cy+side/2)))
out=root/'icons';out.mkdir(exist_ok=True)

for size,name in [(192,'icon-192.png'),(512,'icon-512.png'),(180,'apple-touch-icon.png')]:
    square.resize((size,size),Image.Resampling.LANCZOS).save(out/name,optimize=True)
# Icona adattiva con area centrale sicura contro ritagli della maschera Android.
size=512
safe=round(size*0.76)
tile=square.resize((safe,safe),Image.Resampling.LANCZOS)
mask=Image.new('RGB',(size,size),(8,9,14))
mask.paste(tile,((size-safe)//2,(size-safe)//2))
mask.save(out/'icon-maskable-512.png',optimize=True)
print('Create quattro icone PNG:',', '.join(p.name for p in out.glob('*.png')))
