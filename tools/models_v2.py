"""Hand-authored curved hair locks matching docs/concepts-v2. +Y forward, +Z up."""
import math
import numpy as np

def build(g):
    M, unit = g.Model, g.unit
    # Additional matte navy, indigo, lime, teal and band colors.
    g.P += ['#23334f','#354b6d','#273465','#3c4a8b','#5361ac',
            '#89aa30','#bbd64a','#318875','#71306d','#dcb052']
    g.COLORS[:] = [tuple(bytes.fromhex(c[1:])) for c in g.P]

    def tube(m, points, widths, color, normal=(0,1,0), depth=.48, steps=10, sides=8):
        """Cubic Bezier sweep; broad lenticular cross sections, capped, outward winding."""
        ps=np.array(points,float); rings=[]
        for j in range(steps+1):
            t=j/steps;s=1-t
            c=s**3*ps[0]+3*s*s*t*ps[1]+3*s*t*t*ps[2]+t**3*ps[3]
            tangent=unit(3*s*s*(ps[1]-ps[0])+6*s*t*(ps[2]-ps[1])+3*t*t*(ps[3]-ps[2]))
            axis=np.array(normal,float)
            if abs(tangent@unit(axis))>.97:axis=np.array([1,0,0.])
            u=unit(np.cross(axis,tangent));v=np.cross(tangent,u)
            w=float(np.interp(t,np.linspace(0,1,len(widths)),widths))
            rings.append([c+w*(math.cos(a)*u+depth*math.sin(a)*v) for a in np.linspace(0,2*math.pi,sides,endpoint=False)])
        m.face(list(reversed(rings[0])),color)
        for a,b in zip(rings,rings[1:]):
            for i in range(sides):m.face([a[i],a[(i+1)%sides],b[(i+1)%sides],b[i]],color)
        m.face(rings[-1],color)

    def lock(m, points, width, color, normal=(0,1,0), depth=.5):
        tube(m,points,[width*.42,width,width*.75,.012],color,normal,depth)

    def rear(m,color,rows=4):
        m.ellipsoid((0,-.76,.05),(1.13,.72,.99),color,7,20)
        for row in range(rows):
            z=.92-row*.39
            for sign in [-1,1]:
                lock(m,[(sign*1.20,-.60,z+.23),(sign*1.10,-1.28,z+.16),
                        (sign*.42,-1.54,z-.25),(-sign*.10,-1.39,z-.47)],.35,color,(0,-1,0))

    def braid(m,color,z=.15,length=1.7):
        tube(m,[(0,-1.45,z+.12),(0,-1.46,z-length*.3),(0,-1.48,z-length*.7),(0,-1.48,z-length)],[.18,.21,.18,.10],color,(0,-1,0),.75)
        for k in range(4):
            a=z-k*length/4
            for s in [-1,1]:
                lock(m,[(s*.04,-1.34,a+.18),(s*.48,-1.56,a+.05),
                        (s*.25,-1.64,a-.22),(-s*.06,-1.52,a-.43)],.29,color+(k%2),(0,-1,0),.75)

    def jotaro():
        m=M('01_jotaro_cap','Jotaro Cap');m.scalp(0)
        rear(m,0,3)
        for s in [-1,1]:
            for j in range(3):
                lock(m,[(s*1.15,-.1,.68-j*.2),(s*1.60,-.3,.7-j*.2),
                        (s*1.62,-.65,.65-j*.2),(s*1.58,-.86,.8-j*.25)],.25,0,(s,0,0))
            lock(m,[(s*1.25,.55,.6),(s*1.44,.60,.25),(s*1.32,.83,-.03),(s*1.30,.83,-.34)],.17,0,(s,1,0))
        # Asymmetric flattened crown; rounded-square outline, not a sphere.
        rings=[]
        for sx,sy,z in [(1.28,1.15,.83),(1.43,1.23,1.27),(1.32,1.12,1.98),(1.12,.96,2.10)]:
            ring=[]
            for a in np.linspace(0,2*math.pi,24,endpoint=False):
                x=sx*math.copysign(abs(math.cos(a))**.78,math.cos(a))
                y=sy*math.copysign(abs(math.sin(a))**.78,math.sin(a))-.10
                ring.append(np.array([x,y,z-.16*x]))
            rings.append(ring)
        for a,b in zip(rings,rings[1:]):
            for i in range(24):m.face([a[i],a[(i+1)%24],b[(i+1)%24],b[i]],0)
        m.face(rings[-1],1)
        # Visor elliptical plate slants downward at the projecting front.
        rot=np.array([[1,0,0],[0,math.cos(-.16),-math.sin(-.16)],[0,math.sin(-.16),math.cos(-.16)]])
        m.ellipsoid((0,1.06,.79),(1.46,1.04,.085),0,4,24,rot=rot)
        tube(m,[(-1.35,.45,1.04),(-1.3,1.60,1.0),(1.3,1.60,1.0),(1.35,.45,1.04)],[.055]*4,3,(0,0,1),1,24,8)
        for s in [-1,1]:m.ellipsoid((s*1.36,.48,1.04),(.08,.11,.12),3,4,10)
        m.ellipsoid((-.35,1.17,1.48),(.23,.07,.24),3,5,16)
        m.block((.35,1.15,1.49),(.22,.055,.29),3)
        # Raised palm, four fingers and angled thumb on the rectangular badge.
        m.block((.35,1.22,1.44),(.105,.025,.115),4)
        for j in range(4):
            tube(m,[(.268+j*.055,1.23,1.48),(.268+j*.055,1.23,1.55),(.268+j*.055,1.23,1.63),(.268+j*.055,1.23,1.68-abs(j-1.5)*.025)],[.022]*4,4,steps=3,sides=6)
        tube(m,[(.26,1.24,1.37),(.20,1.24,1.40),(.19,1.24,1.49),(.22,1.24,1.51)],[.025]*4,4,steps=4,sides=6)
        return m

    def josuke():
        m=M('02_josuke_pompadour','Josuke Pompadour');m.scalp(25);rear(m,25,5)
        # Filled pompadour dome with rolled perimeter, not a hollow horseshoe.
        m.ellipsoid((0,.19,1.34),(1.31,1.37,.60),25,6,24)
        for a in np.linspace(-.7,math.pi+.7,19):
            x=1.07*math.cos(a);y=.22+1.22*math.sin(a)
            lock(m,[(x*.79,y*.79,1.75),(x*1.22,y*1.09,2.06),
                    (x*1.26,y*1.17,1.21),(x*.98,y*1.09,.91)],.28,25 if int(a*10)%3 else 26,(x,y,0),.82)
        for j in range(4):
            y=-.77+j*.42
            for s in [-1,1]:
                lock(m,[(s*.97,y-.11,1.65),(s*.83,y+.05,1.97),(s*.32,y+.32,2.01),(-s*.15,y+.4,1.86)],.30,26,(0,0,1))
        for s in [-1,1]:
            for j in range(3):
                lock(m,[(s*1.25,.45,1.10-j*.31),(s*1.53,.02,.90-j*.31),(s*1.5,-.51,.77-j*.31),(s*1.03,-1.02,.67-j*.31)],.22,25,(s,0,0))
        return m

    def giorno():
        m=M('03_giorno_rolls','Giorno Rolls');m.scalp(8);rear(m,9,4)
        m.ellipsoid((0,-.13,1.01),(1.35,1.28,.79),9,7,24)
        for s in [-1,1]:
            for j in range(4):
                z=.45+j*.32
                lock(m,[(s*.55,.83,z+.26),(s*1.42,.67,z+.58),(s*1.59,-.65,z+.1),(s*(1.40-j*.1),-1.48,z+.44)],.30,9,(s,0,.5))
        for x in [-.67,0,.67]:
            lock(m,[(x,.52,1.34),(x-.19,.12,2.01),(x+.24,-.74,1.88),(x+.13,-1.44,1.82)],.38,9,(0,0,1))
        for x,z,r in [(-.81,1.07,.40),(0,1.18,.48),(.81,1.07,.40)]:
            m.ellipsoid((x,1.23,z),(r,.20,r),8,6,18)
            # Solid center plus an actual continuous spiral ridge, not dark empty holes.
            pts=[]
            for a in np.linspace(0,math.pi*4.5,64):
                radius=r*.90*(1-a/(math.pi*4.8))
                pts.append(np.array([x+radius*math.cos(a),1.40+.002*a,z+radius*math.sin(a)]))
            for j in range(0,60,3):tube(m,pts[j:j+4],[.046]*4,9,(0,1,0),.85,3,6)
            m.ellipsoid((x,1.43,z),(.065,.035,.065),9,3,8)
        braid(m,8,.1,1.48)
        m.torus((0,-1.48,-1.45),.16,.045,11,normal=(0,0,1))
        lock(m,[(0,-1.48,-1.46),(-.16,-1.52,-1.72),(.17,-1.60,-1.90),(.18,-1.56,-2.03)],.23,9,(0,-1,0))
        return m

    def jonathan():
        m=M('04_jonathan_hair','Jonathan Hair');m.scalp(25)
        m.ellipsoid((0,-.28,.97),(1.39,1.28,1.18),25,7,24)
        for row in range(2):
            for i in range(7):
                x=(i-3)*.34
                lock(m,[(x*.65,.80-row*.75,1.01),(x*1.48+.14,.68-row*.95,1.94),
                        (x*1.35+.25,-.5-row*.6,2.12),(x*1.22+.23,-.86-row*.52,2.74-abs(x)*.42)],.36,26+(i%2),(0,1,.5))
        for s in [-1,1]:
            for j in range(4):
                lock(m,[(s*.96,.38,1.05-j*.33),(s*1.62,-.15,1.37-j*.44),
                        (s*1.61,-1.03,1.08-j*.47),(s*(1.7-j*.10),-1.21,1.29-j*.64)],.31,26,(s,0,0))
            lock(m,[(s*.06,.78,1.21),(s*.66,1.45,1.68),(s*.73,1.49,.78),(s*.24,1.43,.47)],.29,27,(0,1,0),.75)
        for x in [-.78,0,.78]:lock(m,[(x,-1.20,.65),(x*1.25,-1.67,.22),(x*1.2,-1.57,-.68),(x*1.12,-1.42,-1.03)],.36,25,(0,-1,0))
        return m

    def jolyne():
        m=M('05_jolyne_buns','Jolyne Buns');m.scalp(23);rear(m,24,4)
        for s in [-1,1]:
            c=np.array([s*1.02,-.17,1.40]);n=unit([s*.55,0,.83])
            u=unit(np.cross([0,1,0],n));v=np.cross(n,u)
            m.ellipsoid(c+n*.20,(.51,.48,.59),23,8,16)
            # Alternating green segments around base, separate from navy wrapped bun.
            for k in range(16):
                a=k*2*math.pi/16;p=c+.48*(u*math.cos(a)+v*math.sin(a))
                m.ellipsoid(p,(.15,.14,.135),28+k%2,4,8)
            for j in range(3):
                a0=-.65+j*.65
                pts=[c+n*(.18+.30*math.sin(t))+.49*(u*math.cos(t)+v*math.sin(t)) for t in np.linspace(a0,a0+2.65,4)]
                tube(m,pts,[.08]*4,24,n,.6,12,6)
            lock(m,[(s*.04,.80,1.13),(s*.53,1.36,1.65),(s*1.13,1.43,.66),(s*1.05,1.14,-.41)],.36,29,(0,1,0),.60)
            lock(m,[(s*.58,.95,1.21),(s*1.13,1.27,1.02),(s*1.51,.92,.30),(s*1.46,.75,-.13)],.20,28,(s,1,0))
        braid(m,28,.93,1.95)
        m.torus((0,-1.48,-1.08),.20,.085,30,normal=(0,0,1))
        lock(m,[(0,-1.48,-1.10),(-.42,-1.61,-1.75),(.48,-1.57,-1.78),(.61,-1.50,-1.35)],.32,29,(0,-1,0),.6)
        return m

    def joseph():
        m=M('06_joseph_hair','Joseph Hair');m.scalp(19);rear(m,20,4)
        m.ellipsoid((.1,-.14,1.03),(1.30,1.21,.91),20,7,24)
        # Curved narrow patterned headband, independent of hair locks.
        def p(a,z,rad=1.40):return np.array([rad*math.cos(a),rad*math.sin(a),z])
        for j in range(48):
            a=j*2*math.pi/48;b=(j+1)*2*math.pi/48
            m.face([p(a,.51),p(b,.51),p(b,.81),p(a,.81)],31)
        for j in range(16):
            a=j*2*math.pi/16
            m.face([p(a,.54,1.408),p(a+.31,.54,1.408),p(a+.155,.79,1.408)],32)
        for row in range(2):
            for j in range(5):
                z=1.15+j*.20; y=.57-row*.83-j*.10
                lock(m,[(-.69,y,1.08),(-.48,y+.10,z+.75),(1.12,y-.31,z-.12),(1.85-j*.14,y-.60,z+.17)],.40,20+(j%2),(0,1,.7),.82)
        for s in [-1,1]:
            for j in range(3):
                lock(m,[(s*.87,.20,1.02-j*.27),(s*1.53,-.24,1.36-j*.3),(s*1.67,-.77,.8-j*.31),(s*1.78,-.95,1.04-j*.46)],.30,20,(s,0,0))
        for x,z in [(-.79,.3),(-.22,.38),(.42,.30),(1.05,.04)]:
            lock(m,[(x-.17,.65,1.12),(x-.48,1.37,1.52),(x+.20,1.49,.84),(x+.13,1.24,z)],.28,20,(0,1,0),.72)
        return m

    return [jotaro(),josuke(),giorno(),jonathan(),jolyne(),joseph()]
