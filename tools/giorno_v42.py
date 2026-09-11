"""Conservative Giorno polish: one scalp envelope and continuous spiral ridges.
All accepted locks, three roll bodies and braid positions remain unchanged.
"""
import math
import numpy as np


def build(h):
    Model,sweep,ribbon,hairpoint,plait = [h[k] for k in ('Model','sweep','ribbon','hairpoint','plait')]
    m=Model('03_giorno_rolls','Giorno Rolls')
    # Replace the two overlapping scalp shells with one continuous envelope.
    # Keep the accepted tall upper volume, then smoothly meet the lower hairline.
    m.part();around=64;rings=22
    def skin(a,t):
        end=58+(130-58)*((1-math.cos(math.radians(a)))/2)**1.35
        u=float(np.clip((t-.77)/.23,0,1));blend=u*u*(3-2*u)
        scale=np.array((1.47,1.47,1.63))*(1-blend)+np.array((1.46,1.46,1.49))*blend
        return hairpoint(a,end*t,scale)
    grid=[[skin(i*360/around,j/rings) for i in range(around)] for j in range(rings+1)]
    for j in range(rings):
        for i in range(around):
            k=(i+1)%around
            m.face([grid[j][i],grid[j][k],grid[j+1][k],grid[j+1][i]],9)
    scale=(1.47,1.47,1.63)
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
        pts=[]
        for a in np.linspace(0,math.pi*4.1,61):
            rad=r*.86*(1-.93*a/(math.pi*4.1))
            pts.append([x+rad*math.cos(a),1.32+.022*(1-rad/r),z+rad*math.sin(a)])
        # Same sampled centerline as v4, but one continuous tube per spiral:
        # no repeated caps or normal discontinuities at every three samples.
        centers=[h['bezier'](pts[j:j+4],k/3) for j in range(0,57,3) for k in range(3)]+[np.array(pts[57])]
        m.part();rr=[]
        for i,p in enumerate(centers):
            tangent=centers[min(i+1,len(centers)-1)]-centers[max(0,i-1)]
            tangent/=np.linalg.norm(tangent)
            normal=np.array((0.,1.,0.));normal-=tangent*np.dot(normal,tangent);normal/=np.linalg.norm(normal)
            across=np.cross(normal,tangent)
            rr.append([p+across*.035*math.cos(a)+normal*.028*math.sin(a) for a in np.linspace(0,math.tau,6,endpoint=False)])
        m.face(list(reversed(rr[0])),8)
        for a,b in zip(rr,rr[1:]):
            for k in range(6):m.face([a[k],a[(k+1)%6],b[(k+1)%6],b[k]],8)
        m.face(rr[-1],8)
    plait(m,[.05,-.35,-.72,-1.08,-1.40],-1.40,9,.28)
    m.torus((0,-1.40,-1.40),.105,.037,11,normal=(0,0,1),n=14,m=6)
    sweep(m,[(0,-1.40,-1.39),(-.09,-1.49,-1.62),(.18,-1.47,-1.76),(.10,-1.45,-1.91)], [.1,.20,.14,.008],[.07,.13,.10,.006],9,normal=(0,-1,0))
    return m
