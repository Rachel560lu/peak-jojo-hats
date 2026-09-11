"""Independent checks of the shipped JSON/OBJ/texture set and model silhouette constraints."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image

root=Path(__file__).resolve().parents[1]
catalog=json.loads((root/'assets/catalog.json').read_text())['hats']
assert len(catalog)==6 and len({h['id'] for h in catalog})==6
total=0
for h in catalog:
    d=root/'assets'/h['id'];m=json.loads((d/'mesh.json').read_text())
    v=np.array(m['positions']).reshape(-1,3);f=np.array(m['triangles']).reshape(-1,3);uv=np.array(m['uv']).reshape(-1,2)
    assert np.isfinite(v).all() and np.isfinite(uv).all()
    expected='0.4.1' if h['id'] in {'02_josuke_pompadour','05_jolyne_buns'} else '0.4.2'
    assert m.get('version')==expected and not m.get('texture'), 'Unexpected geometry revision or texture override'
    normals=np.array(m['normals']).reshape(-1,3)
    assert normals.shape==v.shape and np.isfinite(normals).all()
    assert np.allclose(np.linalg.norm(normals,axis=1),1,atol=1e-5)
    assert len(uv)==len(v) and f.min()>=0 and f.max()<len(v)
    assert (uv>=0).all() and (uv<=1).all()
    assert len(f)==h['triangles'] and len(v)==h['vertices']
    area=np.linalg.norm(np.cross(v[f[:,1]]-v[f[:,0]],v[f[:,2]]-v[f[:,0]]),axis=1)
    assert area.min()>1e-8
    # Scalp primitives never extend below the jaw and the top stays reasonable.
    assert v[:,1].min()>-2.4 and v[:,1].max()<3.0
    assert len(v)<65000 and len(f)<21000
    obj=(d/(h['id']+'.obj')).read_text().splitlines()
    ov=np.array([[float(x) for x in line.split()[1:]] for line in obj if line.startswith('v ')])
    assert np.allclose(v,ov[:,[0,2,1]],atol=1e-6)
    assert Image.open(d/'icon.png').size==(128,128)
    assert Image.open(d/'icon.png').getchannel('A').getbbox() is not None
    total+=len(f)
    print(h['id']+': geometry, OBJ parity, texture coordinates, icon PASS')
assert total<90000
josuke=json.loads((root/'assets/02_josuke_pompadour/mesh.json').read_text())
assert np.array(josuke['positions']).reshape(-1,3)[:,1].max()<2.3
v=np.array(josuke['positions']).reshape(-1,3)
assert np.linalg.norm(v,axis=1).min()>1.45, 'Josuke surface crosses guide head'
# A single shared crown/scalp component, with only the intended hairline opening.
f=np.array(josuke['triangles']).reshape(-1,3)
edges={}
adj=[set() for _ in v]
for face in f:
    for a,b in zip(face,np.roll(face,-1)):
        key=tuple(sorted((int(a),int(b))));edges[key]=edges.get(key,0)+1
        adj[a].add(int(b));adj[b].add(int(a))
seen={0};todo=[0]
while todo:
    for i in adj[todo.pop()]-seen:seen.add(i);todo.append(i)
assert len(seen)==len(v), 'Detached Josuke pieces'
assert all(n in (1,2) for n in edges.values()) and sum(n==1 for n in edges.values())==144
locked=json.loads((root/'docs/model-v42/frozen-assets-sha256.json').read_text())
for name,digest in locked.items():
    assert hashlib.sha256((root/'assets'/name.replace('\\','/')).read_bytes()).hexdigest()==digest, 'Frozen asset changed: '+name
giorno=json.loads((root/'docs/model-v42/giorno-preservation.json').read_text())
assert giorno['unchangedSignatureTriangles']>=7384 and giorno['outerBoundsMaxDelta']<.001
jotaro=json.loads((root/'docs/model-v42/jotaro-preservation.json').read_text())
assert jotaro['unchangedCapTriangles']==2522
print('PASS: Josuke/Jolyne and palette frozen; Giorno signature geometry preserved; continuous head-clearing Josuke surface.')
print(f'PASS: 6 hats, {total} total triangles; compact Josuke height confirmed.')
