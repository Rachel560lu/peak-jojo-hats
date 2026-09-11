"""Other four hats: joined volumes, frozen Josuke/Jolyne, conservative Giorno."""
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import generate_models as g
import models_v4
from upgrade_models import export
from mesh_io import load

CHANGED={'01_jotaro_cap','03_giorno_rolls','04_jonathan_hair','06_joseph_hair'}
DOC=g.ROOT/'docs/model-v42'
BASELINE=g.ROOT/'backups/pre-refinement-v0.4.2/assets'


def build():
    from jotaro_v42 import build as jotaro
    from giorno_v42 import build as giorno
    from swept_hair_v42 import build_jonathan,build_joseph
    return models_v4.build(g,{'01_jotaro_cap':jotaro,'03_giorno_rolls':giorno,
                             '04_jonathan_hair':build_jonathan,'06_joseph_hair':build_joseph})


def locked_hashes():
    return {p.relative_to(g.OUT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in g.OUT.rglob('*') if p.is_file() and p.parts[-2] not in CHANGED and p.name!='catalog.json'}


def verify_giorno(old,new):
    # v4 consists of 2 scalp shells, unchanged hair/roll/braid bodies, and 57
    # short spiral tube sections. Only shells and the segmented spirals change.
    replace={1,2,*range(21,40),*range(41,60),*range(61,80)}
    def key(m,face,color):
        return (color,tuple(sorted(tuple(np.round(m.v[i],6)) for i in face)))
    required={key(old,f,c) for f,c,group in zip(old.f,old.c,old.groups) if group not in replace}
    present={key(new,f,c) for f,c in zip(new.f,new.c)}
    assert len(required)>7000 and required<=present,'Giorno accepted locks/roll bodies/braid changed'
    bounds_old=np.array([np.min(old.v,axis=0),np.max(old.v,axis=0)])
    bounds_new=np.array([np.min(new.v,axis=0),np.max(new.v,axis=0)])
    assert np.allclose(bounds_old,bounds_new,atol=.001),'Giorno outer bounds changed'
    return {'unchangedSignatureTriangles':len(required),'outerBoundsMaxDelta':float(np.max(abs(bounds_old-bounds_new)))}


def previews():
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
    views=[('FRONT',0,0),('LEFT',-90,0),('BACK',180,0),('RIGHT',90,0),('TOP',0,89.99),('3/4',35,20)]
    summary=Image.new('RGB',(1440,1440),'#f3eddf');sd=ImageDraw.Draw(summary)
    sd.text((20,8),'v0.4.2 | ACTUAL MESH REFINEMENT / guide heads, not game screenshots',font=font,fill='#263348')
    for row,name in enumerate(sorted(CHANGED)):
        m=load(g.OUT/name)
        old=load(BASELINE/name) if (BASELINE/name/'mesh.json').exists() else None
        sheet=Image.new('RGB',(1440,1050),'#f3eddf');d=ImageDraw.Draw(sheet)
        d.text((20,15),m.label+' | actual v0.4.2 mesh',font=font,fill='#263348')
        compare=Image.new('RGB',(1920,750),'#f3eddf');cd=ImageDraw.Draw(compare)
        cd.text((20,10),m.label+' | BEFORE (top) / AFTER (bottom)',font=font,fill='#263348')
        for j,(label,yaw,elev) in enumerate(views):
            x=j%3*480;y=55+j//3*490
            im=g.render(m,460,yaw,True,elev);sheet.paste(im,(x+10,y),im);d.text((x+20,y+447),label,font=font,fill='#263348')
            for state,model in enumerate([old,m]):
                if model is None:continue
                im=g.render(model,320,yaw,True,elev);compare.paste(im,(j*320,40+state*355),im)
                cd.text((j*320+10,353+state*355),label,font=font,fill='#263348')
        sheet.save(DOC/(name+'-six-views.png'))
        if old is not None:compare.save(DOC/(name+'-before-after.png'))
        # Diagnostic rear light reveals relief that black/navy materials hide
        # under the default front light. Explicitly not the game's shader.
        relief=Image.new('RGB',(1080,380),'#f3eddf');rd=ImageDraw.Draw(relief)
        palette=list(g.COLORS);g.COLORS[:]=[(126,133,142)]*len(palette)
        try:
            for j,yaw in enumerate([120,180,240]):
                im=g.render(m,360,yaw,True,10,light_direction=(2,-5,7));relief.paste(im,(j*360,0),im)
        finally:g.COLORS[:]=palette
        rd.text((10,351),m.label+' | diagnostic clay / rear light (not game material)',font=font,fill='#263348')
        relief.save(DOC/(name+'-rear-relief.png'))
        frames=[]
        for yaw in range(0,360,30):
            im=g.render(m,300,yaw);bg=Image.new('RGB',(300,300),'#f3eddf');bg.paste(im,(0,0),im);frames.append(bg)
        frames[0].save(DOC/(name+'-turntable.gif'),save_all=True,append_images=frames[1:],duration=160,loop=0)
        for j,(_,yaw,el) in enumerate([views[i] for i in [0,1,2,4]]):
            im=g.render(m,340,yaw,True,el);summary.paste(im,(j*360,30+row*350),im)
        sd.text((15,342+row*350),m.label+' / front, side, back, top',font=font,fill='#263348')
        print('Reviewed exported views:',name,flush=True)
    summary.save(DOC/'overview.png')


def main():
    DOC.mkdir(exist_ok=True)
    immutable=locked_hashes();lock=DOC/'frozen-assets-sha256.json'
    if lock.exists():assert {k.replace('\\','/'):v for k,v in json.loads(lock.read_text()).items()}==immutable,'Frozen v0.4.1 assets changed'
    else:lock.write_text(json.dumps(immutable,indent=2),encoding='utf8')
    models=build();old_models=models_v4.build(g)
    report=verify_giorno(old_models[2],models[2])
    (DOC/'giorno-preservation.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    def tri_key(m,f,c):return (c,tuple(sorted(tuple(np.round(m.v[i],6)) for i in f)))
    old=old_models[0];new=models[0]
    cap={tri_key(old,f,c) for f,c,gr in zip(old.f,old.c,old.groups) if gr>=16}
    assert len(cap)==2522 and cap<={tri_key(new,f,c) for f,c in zip(new.f,new.c)},'Jotaro cap/badge geometry changed'
    (DOC/'jotaro-preservation.json').write_text(json.dumps({'unchangedCapTriangles':len(cap)},indent=2),encoding='utf8')
    catalog=json.loads((g.OUT/'catalog.json').read_text())
    for m in models:
        if m.name not in CHANGED:continue
        result=export(m,'0.4.2')
        catalog['hats']=[result if h['id']==m.name else h for h in catalog['hats']]
        im=g.render(m,256,20,False);im.resize((128,128),Image.Resampling.LANCZOS).save(g.OUT/m.name/'icon.png')
        print(m.name,result['triangles'],'triangles',result['vertices'],'vertices',flush=True)
    catalog['version']='0.4.2';(g.OUT/'catalog.json').write_text(json.dumps(catalog,indent=2),encoding='utf8')
    assert immutable==locked_hashes(),'Josuke/Jolyne/palette regression'
    previews()
    print('PASS: two v0.4.1 hats frozen; Giorno signature geometry preserved',flush=True)


if __name__=='__main__':main()
