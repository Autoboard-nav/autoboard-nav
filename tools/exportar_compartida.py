#!/usr/bin/env python3
"""Genera la versión COMPARTIDA: copia index.html (la app única) y autopista.html (redirección) (y los recursos) a una carpeta de destino
dejando vacías las claves de fábrica (__CLAVES_DEF). Uso: python3 tools/exportar_compartida.py DESTINO"""
import re, shutil, sys, os
if len(sys.argv)<2: sys.exit(__doc__)
dst=sys.argv[1]; src=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VACIO="const __CLAVES_DEF={maptiler:'',tomtom:'',ocm:'',ocm2:''};"
os.makedirs(dst,exist_ok=True)
for f in ('index.html','autopista.html'):   # index.html = la app (3D autopista); autopista.html = solo redirige a ./
    h=open(os.path.join(src,f),encoding='utf-8').read()
    if f=='index.html':
        h,n=re.subn(r"const __CLAVES_DEF=\{[^}]*\};",VACIO,h); assert n==1,f
    open(os.path.join(dst,f),'w',encoding='utf-8').write(h)
for f in ('manifest.webmanifest','sw.js','icon-192.png','icon-512.png','icon-512-maskable.png','apple-touch-icon.png','car.glb','cybertruck.glb','modelo3.glb'):
    if os.path.exists(os.path.join(src,f)): shutil.copy2(os.path.join(src,f),os.path.join(dst,f))
for d in ('assets','autopistas','carriles','modelos'):
    if os.path.isdir(os.path.join(src,d)): shutil.copytree(os.path.join(src,d),os.path.join(dst,d),dirs_exist_ok=True)
print('Exportado a',dst)
