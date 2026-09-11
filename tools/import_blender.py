"""Run in Blender's Scripting workspace, or blender --background --python this_file.
Creates a native .blend scene from the exact meshes used by the plugin.
"""
import bpy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
collection = bpy.data.collections.new('JOJO Hats MVP')
bpy.context.scene.collection.children.link(collection)
for folder in sorted((ROOT/'assets').iterdir()):
    if not folder.is_dir(): continue
    data=json.loads((folder/'mesh.json').read_text())
    xyz=data['positions'];tri=data['triangles'];uv=data['uv']
    vertices=[(xyz[i],xyz[i+2],xyz[i+1]) for i in range(0,len(xyz),3)]
    faces=[(tri[i],tri[i+2],tri[i+1]) for i in range(0,len(tri),3)]
    mesh=bpy.data.meshes.new(data['name']);mesh.from_pydata(vertices,[],faces);mesh.update()
    obj=bpy.data.objects.new(data['name'],mesh);collection.objects.link(obj)
    layer=mesh.uv_layers.new(name='Palette')
    for poly in mesh.polygons:
        poly.use_smooth=bool(data.get('normals'))
        for loop in poly.loop_indices:
            i=mesh.loops[loop].vertex_index;layer.data[loop].uv=(uv[2*i],uv[2*i+1])
    mat=bpy.data.materials.new(data['name']+'_palette');mat.use_nodes=True
    if data.get('normals'):
        ns=data['normals'];mesh.normals_split_custom_set_from_vertices([(ns[i],ns[i+2],ns[i+1]) for i in range(0,len(ns),3)])
    image_path=folder/data['texture'] if data.get('texture') else ROOT/'assets'/'palette.png'
    tex=mat.node_tree.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(image_path),check_existing=True)
    tex.interpolation='Linear' if data.get('texture') else 'Closest';mat.node_tree.links.new(tex.outputs['Color'],mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
    mesh.materials.append(mat)
    obj.hide_set(True)
    obj['notes']='Enable one hat at a time; origin at head center. +Y forward, +Z up.'
bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=1.415)
guide=bpy.context.object;guide.name='HEAD_GUIDE_DO_NOT_EXPORT';guide.display_type='WIRE';guide.hide_render=True
collection.objects[0].hide_set(False)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'jojo-hats-mvp.blend'))
print('Saved native editable scene: '+str(ROOT/'jojo-hats-mvp.blend'))
