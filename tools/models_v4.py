"""Six separately authored hairstyles. Surface-following locks, not stacked rear templates.
Coordinates are +Y face, +Z up. All geometry is original and uses the shared palette.
"""
import math
import numpy as np

def build(g,replacements=None):
    unit=g.unit
    class Model(g.Model):
        def __init__(self,name,label):
            super().__init__(name,label);self.groups=[];self.group=0
        def face(self,points,color):
            before=len(self.f);super().face(points,color)
            self.groups.extend([self.group]*(len(self.f)-before))
        def part(self):self.group+=1
        def ellipsoid(self,*a,**kw):self.part();super().ellipsoid(*a,**kw)
        def torus(self,*a,**kw):self.part();super().torus(*a,**kw)
        def block(self,*a,**kw):self.part();super().block(*a,**kw)

    def bezier(ps,t):
        p=np.array(ps,float);s=1-t
        return s**3*p[0]+3*s*s*t*p[1]+3*s*t*t*p[2]+t**3*p[3]

    def sweep(m,ps,width,thickness,color,normal=(0,1,0),steps=14,sides=10):
        """Independent width/depth; parallel transported frame avoids sudden twist."""
        m.part();rings=[];prior=None
        centers=[bezier(ps,t) for t in np.linspace(0,1,steps+1)]
        for j,c in enumerate(centers):
            t=j/steps; tangent=unit(centers[min(j+1,steps)]-centers[max(j-1,0)])
            ref=np.array(normal,float) if prior is None else prior
            v=ref-tangent*np.dot(ref,tangent)
            if np.linalg.norm(v)<1e-5:v=np.cross(tangent,[1,0,0] if abs(tangent[0])<.9 else [0,1,0])
            v=unit(v);u=unit(np.cross(v,tangent));v=np.cross(tangent,u);prior=v
            w=np.interp(t,np.linspace(0,1,len(width)),width)
            h=np.interp(t,np.linspace(0,1,len(thickness)),thickness)
            rings.append([c+u*w*math.cos(a)+v*h*math.sin(a) for a in np.linspace(0,math.tau,sides,endpoint=False)])
        m.face(list(reversed(rings[0])),color)
        for a,b in zip(rings,rings[1:]):
            for k in range(sides):m.face([a[k],a[(k+1)%sides],b[(k+1)%sides],b[k]],color)
        m.face(rings[-1],color)

    def hairpoint(az,phi,scale,r=1):
        a,p=math.radians(az),math.radians(phi)
        out=np.array([math.sin(p)*math.sin(a),math.sin(p)*math.cos(a),math.cos(p)])*np.array(scale)*r
        if out[2]<0:out[2]*=min(1,1.48/scale[2])
        return out

    def shell(m,color,scale=(1.46,1.46,1.49),front=57,back=132):
        """Hairline clears face; sides taper toward temples rather than a helmet edge."""
        m.part();n=48;rings=14
        def p(i,j):
            a=360*i/n;co=math.cos(math.radians(a))
            end=front+(back-front)*((1-co)/2)**1.35
            return hairpoint(a,end*j/rings,scale)
        for j in range(rings):
            for i in range(n):m.face([p(i,j),p(i+1,j),p(i+1,j+1),p(i,j+1)],color)
        # hairpoint azimuth is clockwise looking from above; reverse winding.
        # Face order above is outward for this parameterization.

    def ribbon(m,path,width,color,scale=(1.46,1.46,1.49),lift=.13,tip=.10,steps=16):
        """A tapered raised lock following a continuous head envelope.
        Its underside and root remain embedded in the hair shell; thickness is not width.
        path contains four (azimuth, polar angle) Bezier controls in degrees.
        """
        m.part();rings=[];count=8
        for j in range(steps+1):
            t=j/steps;ang=bezier(path,t)
            local_width=width*np.interp(t,[0,.22,.65,.9,1],[.44,1,.87,.43,.025])
            h=lift*np.interp(t,[0,.15,.65,1],[0,1,.85,0])
            radius=1+tip*t**4
            p=hairpoint(*ang,scale,radius)
            eps=.002
            tangent=unit(hairpoint(*bezier(path,min(1,t+eps)),scale,1+tip*min(1,t+eps)**4)-hairpoint(*bezier(path,max(0,t-eps)),scale,1+tip*max(0,t-eps)**4))
            radial=unit(p/np.array(scale)**2);across=unit(np.cross(radial,tangent));normal=unit(np.cross(tangent,across))
            ring=[]
            for k in range(count):
                a=k*math.tau/count
                # Thin closed lens. Surface lower half is slightly buried.
                height=(h+.055)*math.sin(a)-.035
                ring.append(p+across*local_width*math.cos(a)+normal*height)
            rings.append(ring)
        m.face(list(reversed(rings[0])),color)
        for a,b in zip(rings,rings[1:]):
            for k in range(count):m.face([a[k],a[(k+1)%count],b[(k+1)%count],b[k]],color)
        m.face(rings[-1],color)

    def plait(m,zs,y,color,width=.30):
        """Overlapping interlaced strands with shrinking cross section, not separate beads."""
        for i in range(len(zs)-1):
            za,zb=zs[i:i+2];w=width*(1-.13*i)
            for s in [-1,1]:
                sweep(m,[(s*w*.68,y,za), (s*w*1.1,y-.10,za-.12),
                         (-s*w*.35,y-.16,zb+.15),(-s*w*.60,y,zb)],
                      [w*.63,w*.78,w*.63,w*.48],[w*.45,w*.56,w*.46,w*.32],color,normal=(0,-1,0),steps=10,sides=8)

    def jotaro():
        m=Model('01_jotaro_cap','Jotaro Cap')
        shell(m,0,front=63,back=124)
        # Separate, irregular short locks rooted beneath the cap opening.
        for a,finish,w in [(-76,97,.18),(-104,110,.24),(-136,122,.27),(-169,129,.29),(164,122,.30),(132,117,.24),(101,104,.23),(72,97,.16)]:
            ribbon(m,[(a,58),(a+7,74),(a-5,finish-12),(a+9,finish)],w,0,lift=.12,tip=.045)
        for s in [-1,1]:
            ribbon(m,[(s*71,59),(s*75,73),(s*66,86),(s*62,100)],.14,0,lift=.09,tip=.035)
            for a,ph in [(85,76),(104,86)]:
                ribbon(m,[(s*a,61),(s*(a+5),72),(s*(a+18),ph+2),(s*(a+27),ph-2)],.18,0,lift=.10,tip=.10)
        # Rounded squashed asymmetric crown. Lower edge follows hair envelope.
        m.part();rings=[]
        for sx,sy,z in [(1.33,1.20,.73),(1.40,1.26,.97),(1.42,1.22,1.52),(1.25,1.10,1.98),(1.07,.95,2.03)]:
            ring=[]
            for a in np.linspace(0,math.tau,40,endpoint=False):
                x=sx*math.copysign(abs(math.cos(a))**.83,math.cos(a));y=sy*math.sin(a)-.09
                ring.append(np.array([x,y,z-.17*x+.035*math.cos(2*a)]))
            rings.append(ring)
        for a,b in zip(rings,rings[1:]):
            for k in range(40):m.face([a[k],a[(k+1)%40],b[(k+1)%40],b[k]],0)
        m.part();m.face(rings[-1],0)
        # Continuous black band hides roots under cap, wrapping all the way around.
        m.part()
        for j in range(48):
            a,b=j*math.tau/48,(j+1)*math.tau/48
            def p(t,z):return [1.355*math.cos(t),1.23*math.sin(t)-.09,z-.035*math.cos(t)]
            m.face([p(a,.76),p(b,.76),p(b,.91),p(a,.91)],1)
        # Convex downturned visor, real thickness and curved silhouette.
        m.part();top=[];bottom=[]
        for j in range(9):
            t=j/8;rr=[];bb=[]
            for k in range(25):
                a=-math.pi/2+k*math.pi/24
                x=1.37*math.sin(a);y=.50+(1.69*t+.37)*math.cos(a)
                z=.82-.24*t+.10*math.cos(a)-.035*x
                rr.append(np.array([x,y,z]));bb.append(np.array([x,y,z-.07]))
            top.append(rr);bottom.append(bb)
        for j in range(8):
            for k in range(24):
                m.face([top[j][k],top[j][k+1],top[j+1][k+1],top[j+1][k]],0)
                m.face([bottom[j][k],bottom[j+1][k],bottom[j+1][k+1],bottom[j][k+1]],0)
        for k in range(24):m.face([top[-1][k],bottom[-1][k],bottom[-1][k+1],top[-1][k+1]],1)
        sweep(m,[(-1.33,.37,.91),(-1.24,1.65,.96),(1.24,1.65,.90),(1.33,.37,.86)],[.052]*4,[.052]*4,3,steps=28,sides=8)
        for s in [-1,1]:m.ellipsoid((s*1.33,.38,.90),(.09,.09,.12),3,6,12)
        m.ellipsoid((-.35,1.175,1.37),(.23,.065,.25),3,7,16)
        m.block((.34,1.18,1.36),(.22,.055,.28),3)
        m.block((.34,1.245,1.31),(.105,.015,.105),4)
        for j in range(4):
            x=.255+j*.057;m.ellipsoid((x,1.255,1.46),(.022,.025,.105-abs(j-1.5)*.017),4,5,8)
        sweep(m,[(.25,1.25,1.25),(.19,1.25,1.28),(.18,1.25,1.38),(.22,1.25,1.4)],[.027]*4,[.025]*4,4,steps=6,sides=6)
        return m

    def josuke():
        from josuke_v41 import build as build_josuke
        return build_josuke(Model('02_josuke_pompadour','Josuke Pompadour'))

    def giorno():
        m=Model('03_giorno_rolls','Giorno Rolls');shell(m,9,front=58,back=130)
        scale=(1.47,1.47,1.63)
        shell(m,9,scale,front=56,back=123)
        for a,p,w in [(-24,20,.33),(15,18,.35),(-53,37,.29),(54,35,.33),(-79,54,.25),(82,52,.26),(-105,73,.23),(110,72,.26)]:
            s=-1 if a<0 else 1
            ribbon(m,[(a,p),(a+s*20,p+8),(s*146,p+21),(s*169,p+37)],w,9,scale,lift=.13,tip=.10 if p<60 else .04)
        sweep(m,[(-.10,.82,1.30),(-.40,.32,2.06),(.29,-.52,1.99),(.19,-1.30,1.47)],
              [.13,.35,.28,.008],[.07,.19,.16,.006],9,normal=(0,0,1))
        for s in [-1,1]:
            ribbon(m,[(s*62,72),(s*82,76),(s*107,82),(s*126,84)],.23,9,scale,lift=.12,tip=.08)
        for s in [-1,1]:
            for j in range(3):
                ribbon(m,[(s*116,77+j*13),(s*145,90+j*8),(s*177,109+j*5),(s*180,122+j*3)],.22,9,lift=.08,tip=.025)
        for x,z,r in [(-.78,1.08,.37),(0,1.18,.44),(.78,1.08,.37)]:
            m.ellipsoid((x,1.12,z),(r,.23,r),9,9,20)
            # Ridge lies against solid curved roll face; no floating front disk.
            pts=[]
            for a in np.linspace(0,math.pi*4.1,61):
                rad=r*.86*(1-.93*a/(math.pi*4.1))
                pts.append([x+rad*math.cos(a),1.32+.022*(1-rad/r),z+rad*math.sin(a)])
            for j in range(0,57,3):sweep(m,pts[j:j+4],[.035]*4,[.028]*4,8,steps=3,sides=6)
        plait(m,[.05,-.35,-.72,-1.08,-1.40],-1.40,9,.28)
        m.torus((0,-1.40,-1.40),.105,.037,11,normal=(0,0,1),n=14,m=6)
        sweep(m,[(0,-1.40,-1.39),(-.09,-1.49,-1.62),(.18,-1.47,-1.76),(.10,-1.45,-1.91)], [.1,.20,.14,.008],[.07,.13,.10,.006],9,normal=(0,-1,0))
        return m

    def jonathan():
        m=Model('04_jonathan_hair','Jonathan Hair')
        scale=(1.49,1.48,1.79);shell(m,26,scale,front=58,back=132)
        # Hero locks vary in depth as well as direction; no planar two-row fan.
        for x,ty,tz,w in [(-1.12,-.39,2.17,.29),(-.78,-.61,2.52,.32),(-.38,-.31,2.73,.35),(.05,-.54,2.84,.36),(.48,-.30,2.66,.34),(.87,-.69,2.39,.30),(1.16,-.41,2.11,.27)]:
            sweep(m,[(x*.55,.68-abs(x)*.19,1.37),(x*.84,.49,2.03),
                     (x+.22,ty+.24,tz-.30),(x+.12,ty,tz)], [.12,w,w*.72,.006],[.07,.23,.16,.004],26,normal=(0,1,.3),steps=16)
        # Fan rises above forehead then curves back. Distributed over entire crown.
        for a,p,q,w in [(-48,39,41,.36),(-23,43,30,.36),(4,44,23,.38),(29,43,29,.35),(55,43,43,.32),(-83,54,67,.30),(84,54,63,.32)]:
            s=-1 if a<0 else 1
            ribbon(m,[(a,p),(a+s*24,12),(s*120,q-12),(s*154,q)],w,26,scale,lift=.18,tip=.20)
        for s in [-1,1]:
            for j in range(4):
                ribbon(m,[(s*(76+j*13),63+j*9),(s*(99+j*12),66+j*12),(s*(127+j*9),83+j*12),(s*(133+j*10),98+j*11)],.29-j*.02,26,scale,lift=.12,tip=.10)
        for a,q in [(151,134),(175,141),(200,130)]:
            ribbon(m,[(a,82),(a-12,104),(a+4,122),(a+7,q)],.28,26,scale,lift=.10,tip=.055)
        for a,ph in [(119,73),(143,55),(175,42),(211,57),(239,72)]:
            ribbon(m,[(a-12,ph),(a+8,ph+13),(a-6,ph+33),(a+7,ph+49)],.30,26,scale,lift=.13,tip=.08)
        for a,ph,finish in [(129,83,118),(156,66,114),(181,58,108),(205,72,123),(229,86,121)]:
            ribbon(m,[(a-9,ph),(a+11,ph+10),(a+3,finish-8),(a+14,finish)],.235,26,scale,lift=.16,tip=.07)
        for s in [-1,1]:
            sweep(m,[(s*.07,.67,1.63),(s*.71,1.38,1.67),(s*.63,1.54,.90),(s*.24,1.43,.61)], [.16,.26,.19,.008],[.10,.16,.11,.006],27)
        return m

    def jolyne():
        m=Model('05_jolyne_buns','Jolyne Buns');shell(m,23,front=57,back=127)
        # Shallow hair pulled into the two buns, followed by a separate center braid.
        for s in [-1,1]:
            for j in range(5):
                ribbon(m,[(s*(58+j*20),74+j*9),(s*(71+j*16),59+j*7),(s*91,48),(s*94,39)],.16,23,lift=.045,tip=0)
            for j in range(4):
                ribbon(m,[(s*178,52+j*18),(s*151,55+j*14),(s*117,52+j*7),(s*99,42+j*2)],.21,23,lift=.055,tip=0)
            c=np.array([s*1.02,-.04,1.28]);n=unit([s*.61,-.05,.79]);u=unit(np.cross([0,1,0],n));v=np.cross(n,u)
            center=c+n*.19
            m.ellipsoid(center,(.48,.47,.53),23,10,20)
            # Wrapped navy arcs follow the bun volume, not isolated hoop bands.
            for off in [-.20,.03,.24]:
                rad=math.sqrt(max(.01,.48**2-off**2))
                pts=[center+n*off+rad*(u*math.cos(a)+v*math.sin(a)) for a in np.linspace(0,math.tau,49)]
                for j in range(0,45,3):sweep(m,pts[j:j+4],[.045]*4,[.025]*4,24,normal=n,steps=3,sides=6)
            # Two interweaving strands around the base, continuous rather than beads.
            for phase in [0,math.pi]:
                pts=[]
                for a in np.linspace(0,math.tau,97):
                    rad=.47+.025*math.sin(a*10+phase)
                    pts.append(c+rad*(u*math.cos(a)+v*math.sin(a))+n*.045*math.cos(a*10+phase))
                for j in range(0,93,3):sweep(m,pts[j:j+4],[.045]*4,[.035]*4,29 if phase==0 else 28,normal=n,steps=3,sides=6)
            # Root hugs forehead; broad middle then thin curved tip framing the face.
            sweep(m,[(s*.035,.72,1.31),(s*.59,1.24,1.48),(s*1.02,1.25,.38),(s*1.10,.84,-.32)], [.10,.35,.26,.008],[.055,.12,.09,.006],29)
            sweep(m,[(s*.48,.69,1.29),(s*1.11,.79,1.13),(s*1.33,.73,.44),(s*1.38,.54,.04)], [.10,.21,.12,.008],[.05,.095,.065,.006],28,normal=(s,1,0))
        from jolyne_v41 import add_braid
        add_braid(m,sweep,ribbon,hairpoint)
        return m

    def joseph():
        m=Model('06_joseph_hair','Joseph Hair');scale=(1.48,1.47,1.77)
        shell(m,20,scale,front=62,back=131)
        # Crown emerges from an offset whorl, then spreads around the dome.
        paths=[([(-26,26),(-3,8),(52,25),(91,61)],.37,.15),
               ([(-42,35),(-5,18),(63,39),(110,78)],.35,.15),
               ([(-19,17),(55,12),(122,41),(155,65)],.36,.14),
               ([(8,15),(92,23),(157,51),(183,86)],.31,.12),
               ([(-57,33),(-86,43),(-106,60),(-119,88)],.28,.10),
               ([(-66,59),(-86,70),(-114,83),(-129,106)],.25,.07),
               ([(76,63),(100,76),(129,90),(139,111)],.27,.065),
               ([(121,75),(143,86),(162,106),(170,126)],.25,.04),
               ([(162,68),(184,91),(194,114),(202,133)],.26,.045),
               ([(-154,72),(-163,93),(-176,108),(-170,124)],.28,.05),
               ([(-126,81),(-132,98),(-147,116),(-142,128)],.23,.055)]
        for ps,w,tip in paths:ribbon(m,ps,w,20,scale,lift=.14,tip=tip)
        for ps,w in [([(-.36,.38,1.50),(-.34,.50,2.08),(1.08,.23,1.93),(1.58,-.12,1.98)],.37),
                     ([(-.17,.14,1.67),(.09,-.30,2.18),(1.26,-.53,1.97),(1.72,-.72,1.78)],.38),
                     ([(-.34,-.33,1.56),(-.32,-.61,2.02),(.48,-1.05,1.91),(.91,-1.27,1.59)],.33),
                     ([(-.69,.35,1.28),(-1.05,.30,1.65),(-1.25,-.19,1.53),(-1.51,-.41,1.57)],.24)]:
            sweep(m,ps,[.14,w,w*.70,.006],[.10,.27,.19,.004],20,normal=(0,1,.5),steps=16)
        for a,ph,finish in [(118,82,110),(144,78,122),(173,81,128),(200,92,131),(225,83,117),(246,72,105)]:
            ribbon(m,[(a-15,ph),(a+7,ph+9),(a+5,finish-9),(a+18,finish)],.22,20,scale,lift=.11,tip=.04)
        for s in [-1,1]:
            for ph,a in [(76,92),(92,112)]:
                ribbon(m,[(s*a,ph-13),(s*(a+7),ph),(s*(a+17),ph+5),(s*(a+26),ph+3)],.20,20,scale,lift=.1,tip=.10)
        # Band conforms to a sphere, avoiding a floating constant-radius cylinder.
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
        for ps,w in [([(-.48,.67,1.38),(-.87,1.21,1.37),(-1.02,1.12,.65),(-.88,.99,.30)],.23),
                     ([(-.21,.70,1.39),(-.51,1.36,1.42),(-.22,1.51,.87),(-.13,1.37,.49)],.22),
                     ([(.08,.69,1.42),(.53,1.29,1.38),(.83,1.24,.79),(.91,.99,.34)],.26)]:
            sweep(m,ps,[.11,w,w*.65,.008],[.055,.13,.09,.006],20)
        return m

    helpers={'Model':Model,'sweep':sweep,'ribbon':ribbon,'hairpoint':hairpoint,'shell':shell,'bezier':bezier,'plait':plait}
    layouts=[('01_jotaro_cap',jotaro),('02_josuke_pompadour',josuke),('03_giorno_rolls',giorno),
             ('04_jonathan_hair',jonathan),('05_jolyne_buns',jolyne),('06_joseph_hair',joseph)]
    replacements=replacements or {}
    return [replacements[name](helpers) if name in replacements else fn() for name,fn in layouts]

def normals(m):
    """Average within authored pieces only; do not smooth across overlapping locks."""
    accum={};v=np.array(m.v)
    for f,group in zip(m.f,m.groups):
        a,b,c=v[f];n=np.cross(b-a,c-a)
        for i in f:
            key=(group,*np.round(v[i],6));accum[key]=accum.get(key,np.zeros(3))+n
    out=np.zeros_like(v)
    for f,group in zip(m.f,m.groups):
        for i in f:
            n=accum[(group,*np.round(v[i],6))];out[i]=n/max(np.linalg.norm(n),1e-12)
    return out
