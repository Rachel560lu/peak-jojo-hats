"""Continuous scalp-to-lock volumes for Jonathan and Joseph, v0.4.2.

The main hair mass is a single indexed-at-export surface, with combed relief
sculpted into its radius. Hero tips remain distinct but start inside that mass.
No repeated oval side/rear plates, new materials, or changes to other hats.
Coordinates: +Y face, +Z up.
"""
import math
import numpy as np


def _smooth(t):
    t = min(1.0, max(0.0, t))
    return t*t*(3-2*t)


def _wrapped(a):
    return (a + math.pi) % math.tau - math.pi


def _flow_shell(m, color, scale, front, back, flow, profile, rings=36):
    """One continuous envelope, with broad irregular low-relief flow ridges.

    `flow` stores (angular Bezier path, width, relief) for sparse individually
    laid-out strands. Relief vanishes along each path's ends, so neither
    roots nor tips acquire separate component outlines or floating end caps.
    """
    m.part()
    around = 112
    centers=[]
    samples=np.linspace(0,1,81)
    for path,width,height in flow:
        points=np.array(path,float)
        angles=np.array([(1-t)**3*points[0]+3*(1-t)**2*t*points[1]+
                         3*(1-t)*t*t*points[2]+t**3*points[3] for t in samples])
        az=np.radians(angles[:,0]);phi=np.radians(angles[:,1])
        coords=np.stack([np.sin(phi)*np.sin(az),np.sin(phi)*np.cos(az),np.cos(phi)],axis=1)
        # Low roots, a broad continuous middle, then narrowing organic ends.
        ws=width*np.interp(samples,[0,.16,.60,.85,1],[.30,.90,1,.67,.10])
        hs=height*np.array([_smooth(t/.18)*_smooth((1-t)/.24) for t in samples])
        centers.append((coords,ws,hs))
    def point(a, t):
        rear = ((1-math.cos(a))*.5)**1.35
        end = front+(back-front)*rear
        # Short connected irregular ends, not an exposed even helmet rim.
        if profile == 'jonathan':
            end += rear * (4.9*math.sin(a*5+.9)+2.0*math.sin(a*9-.3))
        else:
            end += rear * (3.4*math.sin(a*6+.45)+1.5*math.cos(a*9))
        p = math.radians(end)*t
        x,y,z = np.array([math.sin(p)*math.sin(a),math.sin(p)*math.cos(a),math.cos(p)])*scale
        if z < 0:
            z *= min(1,1.48/scale[2])
        surface = np.array([x,y,z])
        normal = surface/np.array(scale)**2
        normal /= max(np.linalg.norm(normal),1e-9)
        # Flow is angularly warped around the dome rather than laid in rows.
        lift = 0.0
        phi = math.degrees(p)
        q=np.array([math.sin(p)*math.sin(a),math.sin(p)*math.cos(a),math.cos(p)])
        for coords,ws,hs in centers:
            distance=np.linalg.norm(coords-q,axis=1)*1.5
            # Max-of-lenses is a union with the scalp, never an overlapping
            # detached shell. Smooth cubic shoulder removes a hard oval edge.
            u=np.maximum(0,1-(distance/ws)**2)
            raised=hs*u*u
            lift=max(lift,float(np.max(raised)))
        # Root/hem clearance matters at grazing angles: no raised open edge.
        surface += normal*lift*_smooth((1-t)/.10)
        # A broad, low crown bulge supports the buried hero roots.
        if profile == 'jonathan':
            surface[2] += .055*math.exp(-((phi-32)/30)**2)
        else:
            surface[0] += .09*math.exp(-(phi/50)**2)
            surface[2] += .035*math.exp(-((phi-25)/28)**2)
        return surface
    grid = [[point(i*math.tau/around,j/rings) for i in range(around)] for j in range(rings+1)]
    for j in range(rings):
        for i in range(around):
            k=(i+1)%around
            m.face([grid[j][i],grid[j][k],grid[j+1][k],grid[j+1][i]],color)
    # A small continuous underfold buries the lower rim in the guide scalp.
    # It prevents a grazing-angle thin open-sheet outline beside the temples.
    outer=grid[-1]
    inner=[p*.925 for p in outer]
    for i in range(around):
        k=(i+1)%around
        m.face([outer[i],outer[k],inner[k],inner[i]],color)
    return point


def build_jonathan(h):
    m = h['Model']('04_jonathan_hair','Jonathan Hair')
    sweep = h['sweep']
    flow=[]
    for s in [-1,1]:
        flow += [([(s*52,44),(s*82,36),(s*119,59),(s*144,77)],.34,.21),
                 ([(s*71,56),(s*96,62),(s*118,78),(s*137,96)],.32,.20),
                 ([(s*84,75),(s*111,77),(s*137,96),(s*151,114)],.29,.18),
                 ([(s*102,91),(s*128,99),(s*144,115),(s*156,132)],.25,.14)]
    flow += [([(126,43),(144,58),(163,77),(166,109)],.34,.19),
             ([(176,32),(164,67),(180,93),(180,134)],.35,.20),
             ([(228,51),(220,76),(201,103),(207,129)],.30,.18)]
    _flow_shell(m,26,(1.49,1.48,1.79),58,132,flow,'jonathan',rings=34)
    # The rise and backward sweep are still Jonathan's signature. Roots are
    # deeper/wider and blend into the same filled crown, then individual tips
    # taper without a second detached fan of thin upper surface ribbons.
    fan = [(-1.06,-.42,2.15,.32),(-.74,-.65,2.51,.35),
           (-.34,-.33,2.73,.38),(.06,-.55,2.84,.39),
           (.48,-.30,2.67,.37),(.85,-.66,2.40,.34),(1.12,-.42,2.12,.30)]
    for x,ty,tz,w in fan:
        sweep(m,[(x*.63,.49-abs(x)*.15,1.38),
                 (x*.83,.43,1.94),(x+.20,ty+.24,tz-.29),(x+.10,ty,tz)],
              [.20,w,w*.77,.007],[.145,.25,.17,.005],26,
              normal=(0,1,.25),steps=15,sides=10)
    # Two large S-locks define the forehead; both root inside the crown.
    for s in [-1,1]:
        sweep(m,[(s*.065,.66,1.59),(s*.70,1.37,1.64),
                 (s*.62,1.54,.90),(s*.24,1.43,.61)],
              [.16,.26,.19,.008],[.10,.16,.11,.006],27,steps=16,sides=10)
    return m


def build_joseph(h):
    m = h['Model']('06_joseph_hair','Joseph Hair')
    sweep = h['sweep']; hairpoint=h['hairpoint']
    flow=[([(-26,26),(-3,8),(52,25),(91,61)],.36,.21),
          ([(-42,35),(-5,18),(63,39),(110,78)],.33,.19),
          ([(-19,17),(55,12),(122,41),(155,65)],.34,.18),
          ([(8,15),(92,23),(157,51),(183,86)],.30,.18),
          ([(-57,33),(-86,43),(-106,60),(-119,88)],.28,.18),
          ([(-66,59),(-86,70),(-114,83),(-129,106)],.27,.18),
          ([(76,63),(100,76),(129,90),(139,111)],.27,.19),
          ([(121,75),(143,86),(162,106),(170,126)],.26,.18),
          ([(162,68),(184,91),(194,114),(202,133)],.27,.19),
          ([(-154,72),(-163,93),(-176,108),(-170,124)],.28,.19),
          ([(-126,81),(-132,98),(-147,116),(-142,128)],.25,.17)]
    _flow_shell(m,20,(1.48,1.47,1.77),62,131,flow,'joseph',rings=32)
    # Offset crown retains Joseph's strong side sweep. Broad root cross-
    # sections now sit within the continuous shell instead of hovering on it.
    crown = [([(-.36,.37,1.47),(-.33,.49,2.00),(1.09,.23,1.91),(1.58,-.12,1.98)],.39),
             ([(-.17,.11,1.55),(.09,-.29,2.10),(1.26,-.53,1.97),(1.72,-.72,1.78)],.40),
             ([(-.32,-.32,1.49),(-.30,-.62,1.97),(.48,-1.05,1.91),(.91,-1.27,1.59)],.35),
             ([(-.64,.31,1.22),(-1.05,.30,1.58),(-1.25,-.19,1.53),(-1.51,-.41,1.57)],.27)]
    for ps,w in crown:
        sweep(m,ps,[.20,w,w*.74,.007],[.145,.255,.175,.005],20,
              normal=(0,1,.5),steps=16,sides=10)
    # Two concise temple flicks preserve the short, messy silhouette. Their
    # roots are sunk below the shell rather than pasted along the side.
    for s in [-1,1]:
        sweep(m,[(s*1.03,.30,.91),(s*1.39,.03,.74),
                 (s*1.56,-.24,.58),(s*1.55,-.48,.64)],
              [.115,.23,.15,.006],[.07,.12,.075,.004],20,
              normal=(s,0,.2),steps=12,sides=8)
    # Headband: preserve all original colors, placement and motifs.
    m.part()
    def bp(a,phi):return hairpoint(a,phi,(1.49,1.49,1.49))
    for j in range(64):
        a,b=j*360/64,(j+1)*360/64
        m.face([bp(a,60),bp(b,60),bp(b,71),bp(a,71)],31)
    m.part()
    for j in range(18):
        a=j*20
        pts=[bp(a+2,69),bp(a+17,69),bp(a+10,61)]
        m.face([p*1.003 for p in reversed(pts)],32)
    for ps,w in [([(-.48,.67,1.36),(-.87,1.21,1.37),(-1.02,1.12,.65),(-.88,.99,.30)],.23),
                 ([(-.21,.70,1.37),(-.51,1.36,1.42),(-.22,1.51,.87),(-.13,1.37,.49)],.22),
                 ([(.08,.69,1.40),(.53,1.29,1.38),(.83,1.24,.79),(.91,.99,.34)],.26)]:
        sweep(m,ps,[.11,w,w*.65,.008],[.055,.13,.09,.006],20,steps=14,sides=10)
    return m


def _preview():
    """Read-only to shipped assets: real geometry QA for these two builders."""
    from pathlib import Path
    from PIL import Image, ImageDraw, ImageFont
    import generate_models as g
    import models_v4
    out = g.ROOT/'docs/model-v42-agent-swept'
    out.mkdir(exist_ok=True)
    models = models_v4.build(g,{'04_jonathan_hair':build_jonathan,'06_joseph_hair':build_joseph})
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
    views=[('FRONT',0,0),('LEFT',-90,0),('BACK',180,0),('RIGHT',90,0),('TOP',0,89.99),('3/4',35,15)]
    for m in [models[3],models[5]]:
        m.smooth_normals=models_v4.normals(m)
        board=Image.new('RGB',(1260,960),'#f3eddf');d=ImageDraw.Draw(board)
        d.text((20,12),m.label+' / v0.4.2 continuous mass',font=font,fill='#263348')
        for i,(label,yaw,elev) in enumerate(views):
            x=i%3*420;y=i//3*450+50
            im=g.render(m,400,yaw,True,elev);board.paste(im,(x+10,y),im)
            d.text((x+20,y+395),label,font=font,fill='#263348')
        board.save(out/(m.name+'-six-views.png'))
        v=np.array(m.v)
        print(m.name,'triangles=',len(m.f),'unique positions=',len(np.unique(np.round(v,6),axis=0)),
              'bounds=',v.min(axis=0).tolist(),v.max(axis=0).tolist(),flush=True)
        assert len(m.f)<12500
        assert np.max(v[:,2])<3.0


if __name__=='__main__':
    _preview()
