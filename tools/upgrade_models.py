"""v0.4 geometry upgrade. Does not launch game or touch test profile. Original assets backed up separately."""
from pathlib import Path
import json,math,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import generate_models as g
import models_v4

ROOT=g.ROOT;OUT=g.OUT;DOC=ROOT/'docs/model-v4'

def export(m,version='0.4.0'):
    ns=models_v4.normals(m)
    # Indexed vertices, split only where a normal or palette UV actually differs.
    verts=[];normals=[];uv=[];faces=[];lookup={}
    for face,color in zip(m.f,m.c):
        f=[]
        for i in face:
            key=(*np.round(m.v[i],6),*np.round(ns[i],6),color)
            if key not in lookup:
                lookup[key]=len(verts);verts.append(key[:3]);normals.append(key[3:6]);uv.append(((color+.5)/len(g.P),.5))
            f.append(lookup[key])
        faces.append(f)
    m.v=verts;m.f=faces;m.smooth_normals=np.array(normals)
    folder=OUT/m.name;folder.mkdir(exist_ok=True)
    data={'name':m.name,'label':m.label,'version':version,'positions':[float(x) for v in verts for x in (v[0],v[2],v[1])],
          'triangles':[i for f in faces for i in (f[0],f[2],f[1])],
          'normals':[float(x) for n in normals for x in (n[0],n[2],n[1])],
          'uv':[float(x) for p in uv for x in p]}
    (folder/'mesh.json').write_text(json.dumps(data,separators=(',',':')),encoding='utf8')
    lines=['# JOJO v'+version+', +Y forward +Z up','mtllib palette.mtl','o '+m.name]
    lines+=['v '+' '.join(map(str,v)) for v in verts]
    lines+=['vn '+' '.join(map(str,n)) for n in normals]
    last=-1
    for f,c in zip(faces,m.c):
        if c!=last:lines.append('usemtl color_'+str(c));last=c
        lines.append('f '+' '.join(f'{i+1}//{i+1}' for i in f))
    (folder/(m.name+'.obj')).write_text('\n'.join(lines),encoding='utf8')
    (folder/'palette.mtl').write_text('\n'.join(f'newmtl color_{i}\nKd '+' '.join(str(x/255) for x in c)+'\n' for i,c in enumerate(g.COLORS)),encoding='utf8')
    assert len(verts)<65000
    return {'id':m.name,'label':m.label,'triangles':len(faces),'vertices':len(verts),
            'boundsMin':np.min(verts,axis=0).tolist(),'boundsMax':np.max(verts,axis=0).tolist()}

def main():
    if json.loads((OUT/'catalog.json').read_text()).get('version') in {'0.4.1','0.4.2'}:
        raise SystemExit('Use the current refine_models_v41/v42.py entry point; do not overwrite the targeted revisions.')
    DOC.mkdir(exist_ok=True)
    models=models_v4.build(g)
    atlas=Image.new('RGB',(len(g.P)*16,16));d=ImageDraw.Draw(atlas)
    for i,c in enumerate(g.COLORS):d.rectangle((i*16,0,i*16+15,15),fill=c)
    atlas.save(OUT/'palette.png')
    reports=[export(m) for m in models]
    (OUT/'catalog.json').write_text(json.dumps({'version':'0.4.0','hats':reports},indent=2),encoding='utf8')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',26);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
    board=Image.new('RGB',(1500,1090),'#f3eddf');bd=ImageDraw.Draw(board)
    turnboard=Image.new('RGB',(2160,1200),'#f3eddf');td=ImageDraw.Draw(turnboard)
    bd.text((25,20),'PEAK x JOJO | GEOMETRY UPGRADE v0.4.0',font=font,fill='#263348')
    bd.text((25,58),'Actual meshes + authored normals / shared palette / guide head, not game screenshot',font=small,fill='#566477')
    for k,m in enumerate(models):
        print(m.name,len(m.f),'triangles',len(m.v),'vertices',flush=True)
        im=g.render(m,256,20,False);im.resize((128,128),Image.Resampling.LANCZOS).save(OUT/m.name/'icon.png')
        sheet=Image.new('RGB',(1440,1050),'#f3eddf');sd=ImageDraw.Draw(sheet)
        sd.text((25,15),m.label+' | ACTUAL MESH v0.4.0',font=font,fill='#263348')
        for j,(name,yaw,el) in enumerate([('FRONT',0,0),('LEFT',-90,0),('BACK',180,0),('RIGHT',90,0),('TOP',0,89.99),('THREE-QUARTER',35,15)]):
            x=j%3*480;y=65+j//3*485
            im=g.render(m,460,yaw,True,el);sheet.paste(im,(x+10,y),im)
            sd.text((x+25,y+446),name,font=small,fill='#263348')
        sheet.save(DOC/(m.name+'-six-views.png'))
        x=k%3*500;y=105+k//3*480
        im=g.render(m,370,28);board.paste(im,(x+30,y),im)
        im=g.render(m,155,145);board.paste(im,(x+338,y+212),im)
        bd.text((x+25,y+375),m.label,font=font,fill='#263348')
        bd.text((x+25,y+412),f'{len(m.f):,} triangles / {len(m.v):,} vertices',font=small,fill='#566477')
        # Actual geometry turntable: intermediate angles, no AI-generated stand-ins.
        frames=[]
        for frame_index,yaw in enumerate(range(0,360,30)):
            im=g.render(m,280,yaw);bg=Image.new('RGB',(280,280),'#f3eddf');bg.paste(im,(0,0),im);frames.append(bg)
            turnboard.paste(bg.resize((180,180),Image.Resampling.LANCZOS),(frame_index*180,k*200))
        td.text((5,k*200+179),m.label+' / yaw 0..330 in 30 degree steps',font=small,fill='#263348')
        frames[0].save(DOC/(m.name+'-turntable.gif'),save_all=True,append_images=frames[1:],duration=140,loop=0)
    board.save(DOC/'overview.png');board.save(ROOT/'docs/mesh-preview.png')
    turnboard.save(DOC/'rotation-contact-sheet.png')
    im=g.render(models[0],256,25,False);bg=Image.new('RGB',(256,256),'#66718c');bg.paste(im,(0,0),im);bg.save(ROOT/'icon.png')

if __name__=='__main__':main()
