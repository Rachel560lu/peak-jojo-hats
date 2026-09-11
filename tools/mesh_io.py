"""Read shipped JSON geometry for actual-mesh previews."""
import json
import numpy as np
import generate_models as g


def load(folder):
    data=json.loads((folder/'mesh.json').read_text())
    m=g.Model(data['name'],data['label'])
    m.v=np.array(data['positions']).reshape(-1,3)[:,[0,2,1]].tolist()
    m.f=np.array(data['triangles']).reshape(-1,3)[:,[0,2,1]].tolist()
    uv=np.array(data['uv']).reshape(-1,2)
    m.c=[int(uv[f[0],0]*len(g.P)) for f in m.f]
    m.smooth_normals=np.array(data['normals']).reshape(-1,3)[:,[0,2,1]]
    return m
