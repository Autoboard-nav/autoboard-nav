#!/usr/bin/env python3
"""Añade a assets/radares.json los radares NUEVOS del feed de Radares Anunciados (https://github.com/GeiserX/radares-anunciados-ha, datos ODbL 1.0).
Uso: python3 tools/importar_radares.py ruta/al/feed.geojson
- Solo puntos activos de fuentes oficiales/abiertas estables (DGT, SCT, Euskadi, Navarra, Donostia, Madrid, Salamanca, OpenStreetMap).
- Sin límite de velocidad conocido => se descarta (el aviso inventaría 50 km/h).
- No se tocan los puntos que ya existen (a <100 m) ni su orden: las ediciones locales (por coordenadas) siguen valiendo.
- Se descartan: radares móviles anunciados por día (caducan), multas agrupadas, notas de OSM sin confirmar y tramos (líneas)."""
import json, math, sys, collections, os
ruta=sys.argv[1]; base=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'assets')
FUENTES={'dgt','sct','euskadi','navarra','donostia','madrid','salamanca','osm','sct_remolc'}
TIPO={'fixed':'fijo','section':'tramo','trailer':'movil'}
old=json.load(open(os.path.join(base,'radares.json')))
feed=json.load(open(ruta))['features']
def d(a,b,c,e):
    p=math.pi/180; return 6371000*math.hypot((e-b)*p*math.cos((a+c)/2*p),(c-a)*p)
G=collections.defaultdict(list)
def put(lat,lon): G[(round(lat,2),round(lon,2))].append((lat,lon))
def cerca(lat,lon,r):
    for i in (-.01,0,.01):
        for j in (-.01,0,.01):
            for (a,b) in G.get((round(lat+i,2),round(lon+j,2)),()):
                if d(lat,lon,a,b)<r: return True
    return False
for o in old: put(o['lat'],o['lon'])
nuevos=[]; cont=collections.Counter()
for f in feed:
    p=f['properties']
    if f['geometry']['type']!='Point' or not p.get('active') or p['source'] not in FUENTES or p['kind'] not in TIPO: continue
    mx=p.get('maxspeed')
    if not mx: cont['sin límite']+=1; continue
    lon,lat=f['geometry']['coordinates']
    if cerca(lat,lon,100): cont['ya existía']+=1; continue
    put(lat,lon)
    nuevos.append({'lat':round(lat,5),'lon':round(lon,5),'max':int(mx),'t':TIPO[p['kind']],'s':p['source']}); cont['nuevo '+p['source']]+=1
json.dump(old+nuevos,open(os.path.join(base,'radares.json'),'w'),separators=(',',':'),ensure_ascii=False)
print(len(old),'+',len(nuevos),'=',len(old)+len(nuevos)); print(dict(cont))
