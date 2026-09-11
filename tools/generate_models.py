"""Deterministic low-poly hat authoring. Blender coordinates: +Y front, +Z up.
Exports editable OBJ/MTL, runtime JSON meshes, palette textures and actual mesh renders.
Run with Python + numpy + Pillow. No image-generation or downloaded model assets.
"""
from pathlib import Path
import json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
P = ['#171821','#30313f','#494956','#d4a343','#ffe08a', '#23182f','#493064','#725095',
     '#dba632','#f2ca50','#ffe68b','#a57629', '#182b66','#3058b4','#507bdd',
     '#323c28','#718344','#b6cc60','#e0dd78', '#422921','#6e4430','#986642', '#c58a52']
COLORS = [tuple(bytes.fromhex(c[1:])) for c in P]

def unit(a):
    a = np.array(a, dtype=float)
    return a / max(np.linalg.norm(a), 1e-9)

class Model:
    def __init__(self, name, label):
        self.name, self.label, self.v, self.f, self.c = name, label, [], [], []
    def face(self, points, color):
        for k in range(1, len(points)-1):
            tri = np.array([points[0], points[k], points[k+1]])
            if np.linalg.norm(np.cross(tri[1]-tri[0], tri[2]-tri[0])) < 1e-8:
                continue
            start = len(self.v)
            self.v.extend(tri.tolist()); self.f.append([start,start+1,start+2]); self.c.append(color)
    def ellipsoid(self, center, size, color, rings=7, sides=16, max_phi=math.pi, rot=None):
        center, size = np.array(center), np.array(size)
        def p(phi, theta):
            v = np.array([math.sin(phi)*math.cos(theta), math.sin(phi)*math.sin(theta), math.cos(phi)])*size
            if rot is not None: v = rot@v
            return center+v
        for j in range(rings):
            a,b=max_phi*j/rings,max_phi*(j+1)/rings
            for i in range(sides):
                t,u=2*math.pi*i/sides,2*math.pi*(i+1)/sides
                self.face([p(a,t),p(b,t),p(b,u),p(a,u)], color)
    def scalp(self, color, radius=1.44):
        # Front hairline above eyes; back and sides follow the head lower down.
        sides,rings=24,7
        def p(i,j):
            t=2*math.pi*i/sides
            end=1.66-0.60*max(0,math.sin(t))
            phi=end*j/rings
            return np.array([radius*math.sin(phi)*math.cos(t),radius*math.sin(phi)*math.sin(t),radius*math.cos(phi)])
        for j in range(rings):
            for i in range(sides):self.face([p(i,j),p(i,j+1),p(i+1,j+1),p(i+1,j)],color)
    def cone(self, base, tip, radius, color, sides=5):
        b,t=np.array(base),np.array(tip)
        n=unit(t-b); u=unit(np.cross(n,[0,0,1] if abs(n[2])<.9 else [0,1,0])); v=np.cross(n,u)
        ring=[b+radius*(math.cos(2*math.pi*i/sides)*u+math.sin(2*math.pi*i/sides)*v) for i in range(sides)]
        for i in range(sides):self.face([ring[i],ring[(i+1)%sides],t],color)
        self.face(list(reversed(ring)),color)
    def torus(self, center, major, minor, color, normal=(0,1,0), n=12, m=5, scale=(1,1)):
        c=np.array(center); z=unit(normal); u=unit(np.cross([0,0,1] if abs(z[2])<.9 else [0,1,0],z)); v=np.cross(z,u)
        def p(i,j):
            a,b=2*math.pi*i/n,2*math.pi*j/m
            return c+(major+minor*math.cos(b))*(math.cos(a)*u*scale[0]+math.sin(a)*v*scale[1])+minor*math.sin(b)*z
        for i in range(n):
            for j in range(m):self.face([p(i,j),p(i+1,j),p(i+1,j+1),p(i,j+1)],color)
    def block(self, center, half, color):
        c=np.array(center); h=np.array(half)
        vs=[c+h*np.array(s) for s in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
        for f in [[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]:self.face([vs[i] for i in f],color)

def jotaro():
    m=Model('01_jotaro_cap','Jotaro Cap'); m.scalp(0)
    m.ellipsoid((0,-.16,1.34),(1.45,1.25,.65),0,rings=5,sides=16)
    m.ellipsoid((0,1.0,.87),(1.46,1.02,.12),0,rings=4,sides=16)
    m.ellipsoid((0,1.02,.90),(1.32,.78,.10),1,rings=3,sides=14)
    for x in [-1,-.6,0,.6,1]:
        m.cone((x,-.9,.7),(x*1.4,-1.8,.8+abs(x)*.35),.4,0)
    m.block((.38,1.02,1.50),(.23,.075,.27),3)
    m.block((.38,1.10,1.51),(.16,.025,.19),4)
    m.ellipsoid((-.30,1.17,1.49),(.17,.075,.17),3,4,10)
    for i in range(12):
        x=-1.14+i*.205; y=1.14+.19*(1-(x/1.3)**2)
        m.torus((x,y,1.07),.080,.029,3,normal=(0,1,.4*(i%2)),n=8,m=4,scale=(1.3,.72))
    for i in range(5):
        m.torus((1.36,0.67,.99-i*.18),.105,.036,3,normal=(1,.4*(i%2),0),n=8,m=4,scale=(.8,1.2))
    return m

def josuke():
    m=Model('02_josuke_pompadour','Josuke Pompadour'); m.scalp(5)
    # One compact rounded rectangular slab; no separate hat or rolled rear mass.
    sides=24
    levels=[(.95,.98,0.98),(1.08,1.10,1.11),(1.13,1.12,1.40),(1.04,1.04,1.62),(.83,.87,1.70)]
    def ring(level):
        sx,sy,z=level
        return [np.array([sx*math.copysign(abs(math.cos(t))**.55,math.cos(t)), .26+sy*math.copysign(abs(math.sin(t))**.55,math.sin(t)),z]) for t in np.linspace(0,2*math.pi,sides,endpoint=False)]
    rs=[ring(l) for l in levels]
    for j in range(len(rs)-1):
        for i in range(sides):m.face([rs[j][i],rs[j][(i+1)%sides],rs[j+1][(i+1)%sides],rs[j+1][i]],6 if j!=2 else 7)
    m.face(rs[-1],5); m.face(list(reversed(rs[0])),5)
    for row in range(6):
        for col in range(7):
            x=(col-3)*.23+(row%2)*.08; y=-.45+row*.26
            if abs(x)<.8:m.ellipsoid((x,y,1.71),(.11,.075,.035),6,2,4)
    return m

def spikes(m, palette, seed, swept=False):
    rng=np.random.default_rng(seed)
    m.scalp(palette[0])
    for row in range(3):
        phi=.43+row*.43
        for i in range(9):
            theta=2*math.pi*(i+.35*row)/9
            d=np.array([math.sin(phi)*math.cos(theta),math.sin(phi)*math.sin(theta),math.cos(phi)])
            if d[1]>.55 and row==2:continue
            base=d*1.22
            tip=d*(1.83+rng.uniform(0,.30))+np.array([.32 if swept else .10,-.25,.08])
            m.cone(base,tip,.38 if row<2 else .32,palette[i%len(palette)],5)
    for x in [-.86,-.38,.28,.77]:
        m.cone((x,.93,1.0),(x-.17,1.40,.26+abs(x)*.18),.30,palette[1],5)

def giorno():
    m=Model('03_giorno_rolls','Giorno Rolls'); spikes(m,[8,9,10],7)
    for x,z in [(-.72,1.12),(0,1.27),(.72,1.12)]:
        m.ellipsoid((x,1.15,z),(.35,.14,.35),11,5,12)
        m.torus((x,1.31,z),.265,.105,9,n=12,m=6)
        m.torus((x,1.39,z),.263,.035,10,n=12,m=4)
    return m

def jonathan():
    m=Model('04_jonathan_hair','Jonathan Hair'); spikes(m,[12,13,14],11,True);return m

def jolyne():
    m=Model('05_jolyne_buns','Jolyne Buns');m.scalp(16)
    for sign in [-1,1]:
        center=np.array([sign*1.03,-.16,1.30]);m.ellipsoid(center,(.53,.48,.53),16,6,12)
        for i in range(12):
            t=2*math.pi*i/12
            p=center+np.array([math.cos(t)*.39,.29,math.sin(t)*.39])
            m.ellipsoid(p,(.13,.16,.13),17 if i%2 else 16,3,6)
        m.ellipsoid(center+np.array([0,.37,0]),(.21,.12,.23),17,4,8)
    # Broad leaf-shaped bangs on the scalp surface, with thickness at the silhouette.
    for points in [
        [(-.55,.77,1.35),(.12,1.23,.96),(.76,1.32,.35)],
        [(-.35,.90,1.30),(-.83,1.19,.60),(-1.15,.98,-.32)],
        [(.61,.88,1.05),(.97,1.12,.51),(1.18,.81,-.20)]
    ]:
        rs=[]
        for p,w in zip(points,[.29,.25,.015]):
            x,y,z=p;rs.append([np.array([x-w,y,z]),np.array([x,y+.12,z]),np.array([x+w,y,z]),np.array([x,y-.09,z])])
        for a,b in zip(rs,rs[1:]):
            for i in range(4):m.face([a[i],b[i],b[(i+1)%4],a[(i+1)%4]],18 if i<2 else 17)
    return m

def joseph():
    m=Model('06_joseph_hair','Joseph Hair');spikes(m,[19,20,21],33)
    m.cone((.9,-.65,.8),(1.95,-.8,.68),.38,21)
    m.cone((-.9,-.7,.7),(-1.85,-1.1,.4),.36,20)
    return m

import sys
from models_v2 import build
MODELS=build(sys.modules[__name__])

def export(m):
    folder=OUT/m.name;folder.mkdir(exist_ok=True)
    # Flattened triangles preserve authored faceted normals. Unity conversion flips winding.
    data={'name':m.name,'label':m.label,'positions':[round(c,6) for v in m.v for c in (v[0],v[2],v[1])],
          'triangles':[i for f in m.f for i in (f[0],f[2],f[1])],
          'uv':[c for col in m.c for _ in range(3) for c in ((col+.5)/len(P),.5)]}
    (folder/'mesh.json').write_text(json.dumps(data,separators=(',',':')),encoding='utf8')
    lines=['# +Y front, +Z up; head radius 1.415; origin at head center','mtllib palette.mtl',f'o {m.name}']
    lines += ['v '+' '.join(f'{c:.6f}' for c in v) for v in m.v]
    last=-1
    for face,col in zip(m.f,m.c):
        if col!=last:lines.append(f'usemtl color_{col}');last=col
        lines.append('f '+' '.join(str(i+1) for i in face))
    (folder/(m.name+'.obj')).write_text('\n'.join(lines),encoding='utf8')
    (folder/'palette.mtl').write_text('\n'.join(f'newmtl color_{i}\nKd '+ ' '.join(str(x/255) for x in c)+'\n' for i,c in enumerate(COLORS)),encoding='utf8')
    assert all(math.isfinite(c) for v in m.v for c in v)
    assert len(m.f)<21000, (m.name,len(m.f))
    assert all(np.linalg.norm(np.cross(np.array(m.v[b])-m.v[a],np.array(m.v[c])-m.v[a]))>1e-8 for a,b,c in m.f)
    return {'id':m.name,'label':m.label,'triangles':len(m.f),'vertices':len(m.v),'boundsMin':np.min(m.v,axis=0).tolist(),'boundsMax':np.max(m.v,axis=0).tolist()}

def render(m,size=440,yaw=25,head=True,elevation=15,light_direction=None):
    # Orthographic z-buffer renderer of the exported mesh (not an illustration).
    verts=list(m.v);faces=list(m.f);colors=[COLORS[c] for c in m.c]
    smooth=getattr(m,'smooth_normals',None)
    smooth_count=len(m.f)
    if head:
        h=Model('head','head');h.ellipsoid((0,0,0),(1.415,1.415,1.415),0,12,24)
        n=len(verts);verts+=h.v;faces += [[i+n for i in f] for f in h.f];colors += [(186,197,197)]*len(h.f)
        for x in [-.42,.42]:
            e=Model('eye','eye');e.ellipsoid((x,1.355,.16),(.10,.07,.15),0,5,8)
            n=len(verts);verts+=e.v;faces += [[i+n for i in f] for f in e.f];colors += [(32,38,49)]*len(e.f)
    az=math.radians(yaw); elev=math.radians(elevation)
    view=unit([math.sin(az)*math.cos(elev),math.cos(az)*math.cos(elev),math.sin(elev)])
    right=unit(np.cross(view,[0,0,1]));up=np.cross(right,view)
    v=np.array(verts);screen=np.stack([v@right,-v@up,v@view],axis=1)
    screen[:,:2]*=size/6.20;screen[:,0]+=size*.5;screen[:,1]+=size*.55
    rgb=np.zeros((size,size,4),dtype=np.uint8);depth=np.full((size,size),-np.inf)
    light=unit([-3,5,8] if light_direction is None else light_direction)
    for fi,(f,col) in enumerate(zip(faces,colors)):
        a,b,c=screen[f];n=unit(np.cross(v[f[1]]-v[f[0]],v[f[2]]-v[f[0]]))
        if n@view<=0:continue
        xmin=max(0,int(min(a[0],b[0],c[0])));xmax=min(size-1,int(max(a[0],b[0],c[0]))+1)
        ymin=max(0,int(min(a[1],b[1],c[1])));ymax=min(size-1,int(max(a[1],b[1],c[1]))+1)
        if xmax<xmin or ymax<ymin:continue
        yy,xx=np.mgrid[ymin:ymax+1,xmin:xmax+1];xx=xx+.5;yy=yy+.5
        den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
        if abs(den)<1e-8:continue
        wa=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den
        wb=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den;wc=1-wa-wb
        z=wa*a[2]+wb*b[2]+wc*c[2];sl=np.s_[ymin:ymax+1,xmin:xmax+1]
        mask=(wa>=-1e-5)&(wb>=-1e-5)&(wc>=-1e-5)&(z>depth[sl])
        depth[sl][mask]=z[mask]
        if smooth is not None and fi<smooth_count:
            ns=wa[...,None]*smooth[f[0]]+wb[...,None]*smooth[f[1]]+wc[...,None]*smooth[f[2]]
            ns/=np.maximum(np.linalg.norm(ns,axis=2,keepdims=True),1e-9)
            shade=.55+.45*np.maximum(0,ns@light)
            rgba=np.zeros((*shade.shape,4),dtype=np.uint8)
            rgba[:,:,:3]=np.clip(shade[...,None]*np.array(col),0,255);rgba[:,:,3]=255
            rgb[sl][mask]=rgba[mask]
        else:
            shade=.55+.45*max(0,float(n@light));rgba=tuple(int(t*shade) for t in col)+(255,)
            rgb[sl][mask]=rgba
    return Image.fromarray(rgb)

def main():
    if (OUT/'05_jolyne_buns'/'albedo.png').exists():
        raise SystemExit('Refined Jolyne is installed. This legacy six-hat generator would overwrite it. Run tools/refine_jolyne.py for the refined sample.')
    atlas=Image.new('RGB',(len(P)*16,16))
    d=ImageDraw.Draw(atlas)
    for i,col in enumerate(COLORS):d.rectangle((i*16,0,(i+1)*16-1,15),fill=col)
    atlas.save(OUT/'palette.png')
    reports=[export(m) for m in MODELS]
    (OUT/'catalog.json').write_text(json.dumps({'hats':reports},indent=2),encoding='utf8')
    for m in MODELS:
        render(m,256,15,False).resize((128,128),Image.Resampling.LANCZOS).save(OUT/m.name/'icon.png')
    board=Image.new('RGB',(1500,1100),'#f3eddf');draw=ImageDraw.Draw(board)
    fontpath='C:/Windows/Fonts/arial.ttf'
    title=ImageFont.truetype(fontpath,36); label=ImageFont.truetype(fontpath,24);small=ImageFont.truetype(fontpath,16)
    draw.text((35,22),'PEAK x JOJO | PLAYABLE HAT MVP',fill='#252b42',font=title)
    draw.text((37,70),'Actual exported geometry  /  Six static head cosmetics  /  v0.2.0',fill='#596478',font=small)
    for idx,m in enumerate(MODELS):
        x=(idx%3)*500;y=110+(idx//3)*475
        image=render(m,365);board.paste(image,(x+65,y),image)
        side=render(m,135,100);board.paste(side,(x+355,y+210),side)
        draw.text((x+35,y+372),m.label,fill='#252b42',font=label)
        draw.text((x+35,y+407),f'{len(m.f):,} triangles | OBJ + runtime mesh',fill='#596478',font=small)
    (ROOT/'docs').mkdir(exist_ok=True);board.save(ROOT/'docs'/'mesh-preview.png')
    views=ROOT/'docs/model-v2';views.mkdir(exist_ok=True)
    for m in MODELS:
        sheet=Image.new('RGB',(1440,1050),'#f3eddf');sd=ImageDraw.Draw(sheet)
        sd.text((26,15),m.label+' | ACTUAL MESH v0.2.0',font=title,fill='#252b42')
        for i,(name,yaw,el) in enumerate([('FRONT',0,0),('LEFT',-90,0),('BACK',180,0),('RIGHT',90,0),('TOP',0,89.99),('THREE-QUARTER',35,20)]):
            x=i%3*480;y=65+i//3*485
            im=render(m,460,yaw,True,el);sheet.paste(im,(x+10,y),im)
            sd.text((x+25,y+445),name,font=label,fill='#252b42')
        sheet.save(views/(m.name+'-six-views.png'))
    icon=render(MODELS[0],256,20,False);bg=Image.new('RGBA',(256,256),'#666c8a');bg.alpha_composite(icon);bg.convert('RGB').save(ROOT/'icon.png')
    print(json.dumps(reports,indent=2))

if __name__=='__main__':main()
