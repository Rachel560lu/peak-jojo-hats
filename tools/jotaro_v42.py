"""Jotaro's cap-hair transition: one fitted mantle with sculpted flow relief.

Original cap, visor and badges are deliberately preserved.  Only the former
independent side/back hair ribbons are replaced; +Y is face, +Z is up.
"""
import math
import numpy as np


# Non-repeating pointed hem: broad nape tufts, shorter temple/ear tufts.
# The mantle is one surface, so these shape its actual edge, not attached tubes.
HEM = np.array([
    [48,82],[58,99],[69,88],[82,94],[95,88],[112,105],
    [126,104],[143,120],[157,113],[179,124],[196,113],
    [213,119],[228,104],[245,111],[258,96],[276,102],
    [289,89],[302,98],[312,82],
], dtype=float)


def mantle_point(a, t):
    """A scalp-hugging surface, from buried root to a thin irregular hairline."""
    i=min(len(HEM)-2,max(0,int(np.searchsorted(HEM[:,0],a))-1))
    u=(a-HEM[i,0])/(HEM[i+1,0]-HEM[i,0])
    # Rounded valley into a sharp tuft tip. This replaces the mechanical
    # straight zigzag outline without adding a second skirt of hair pieces.
    smooth=u*u*(3-2*u)
    end=HEM[i,1]*(1-smooth)+HEM[i+1,1]*smooth
    # Slight backward sweep in the central flow; zero drift at mantle borders.
    # This deforms both the relief and surface coordinates, not another layer.
    edge_fade = math.sin(math.pi*(a-48)/264)
    drift = (8*math.sin(math.pi*t)+7*t)*math.sin(math.radians(a))*edge_fade
    az = math.radians(a+drift)
    phi = math.radians(46+(end-46)*t)
    direction = np.array([math.sin(phi)*math.sin(az),
                          math.sin(phi)*math.cos(az),math.cos(phi)])
    # Clear the radius-1.415 guide in authoring units, with low broad relief.
    # At upper rings the cap covers the roots completely.
    scallop = (.5+.5*math.cos(math.radians(a*8.6)-1.8*t+.32*math.sin(math.radians(a*2))))**2
    ridge = .092*math.sin(math.pi*t)**.65*scallop
    radius = 1.472+ridge
    # Ends point slightly outward only at the very edge. No fat cross section.
    radius += .022*t**5
    # Short swept side tips belong to this same loft, not glued-on tubes.
    radius += .16*t**7*(math.exp(-((a-111)/10)**2)+.85*math.exp(-((a-245)/10)**2))
    return direction*radius


def build(h):
    Model, sweep = h['Model'], h['sweep']
    m = Model('01_jotaro_cap','Jotaro Cap')
    m.part()
    around, rings = 128, 30
    grid = [[mantle_point(48+264*i/around,j/rings)
             for i in range(around+1)] for j in range(rings+1)]
    for j in range(rings):
        for i in range(around):
            m.face([grid[j][i],grid[j][i+1],grid[j+1][i+1],grid[j+1][i]],0)
    # A narrow inward-folded hem gives the single layer a real thin edge.
    # Its underside remains outside the guide head, never a dark open slit.
    m.part()
    for i in range(around):
        a,b=grid[-1][i],grid[-1][i+1]
        m.face([a,b,b*.975,a*.975],0)
    for i in [0,around]:
        for j in range(rings):
            a,b=grid[j][i],grid[j+1][i]
            pts=[a,b,b*.975,a*.975]
            m.face(pts if i==0 else list(reversed(pts)),0)

    # A pair of compact backward flicks per side preserves the recognizable
    # cap-to-hair silhouette. Their thin roots and lower lens lie in the loft,
    # unlike the previous hanging oval locks. The nape stays a single mantle.
    ribbon=h['ribbon']
    for s in [-1,1]:
        for start,end,phi,w in [(78,115,70,.18),(96,133,84,.21)]:
            ribbon(m,[(s*start,59),(s*(start+12),phi-1),
                       (s*(end-10),phi+5),(s*end,phi)],
                   w,0,scale=(1.48,1.48,1.48),lift=.055,tip=.115,steps=14)

    # Original rounded, squashed asymmetric cap crown.
    m.part(); crown=[]
    for sx,sy,z in [(1.33,1.20,.73),(1.40,1.26,.97),(1.42,1.22,1.52),(1.25,1.10,1.98),(1.07,.95,2.03)]:
        ring=[]
        for a in np.linspace(0,math.tau,40,endpoint=False):
            x=sx*math.copysign(abs(math.cos(a))**.83,math.cos(a));y=sy*math.sin(a)-.09
            ring.append(np.array([x,y,z-.17*x+.035*math.cos(2*a)]))
        crown.append(ring)
    for a,b in zip(crown,crown[1:]):
        for k in range(40):m.face([a[k],a[(k+1)%40],b[(k+1)%40],b[k]],0)
    m.part();m.face(crown[-1],0)
    # Continuous black band conceals mantle roots all around the opening.
    m.part()
    for j in range(48):
        a,b=j*math.tau/48,(j+1)*math.tau/48
        def p(t,z):return [1.355*math.cos(t),1.23*math.sin(t)-.09,z-.035*math.cos(t)]
        m.face([p(a,.76),p(b,.76),p(b,.91),p(a,.91)],1)
    # Original convex, downturned visor with thickness.
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
