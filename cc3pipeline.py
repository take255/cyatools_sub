import bpy
import bmesh

import imp
import os
from pathlib import Path
import pickle


#from mathutils import ( Matrix)

from . import utils
imp.reload(utils)


#新規マテリアルを作成して、そこにイメージを集める
#シェーダーノード一覧
#https://docs.blender.org/api/blender2.8/bpy.types.html
def collect_textures():

    for ob in utils.selected():

        image_array = []

        for mat in ob.data.materials:
            print('------------------------------------')
            print(mat.name)
            nodes = mat.node_tree.nodes
            for node in nodes:
                #Node = nodes.get("Image Texture")
                if node.type == 'TEX_IMAGE':
                    img = node.image


                    for d in dir(img):
                        print(d)

                    image_array.append(img)


        newmat = bpy.data.materials.new(name='ImageCollected' )


        newmat.use_nodes = True
        nodes = newmat.node_tree.nodes
        mat_links = newmat.node_tree.links
        # a new material node tree already has a diffuse and material output node
        # output = mat_nodes['Material Output']
        # diffuse = mat_nodes['Diffuse BSDF']

        #nodes = newmat.node_tree.nodes
        #nodes.new(type='ShaderNodeOutputMaterial')
        for i,img in enumerate(image_array):
            tex = nodes.new(type='ShaderNodeTexImage')
            tex.image = img
            img.colorspace_settings.name = 'sRGB' #カラースペースをsRGBに強制
            tex.location.x = 100*i
            tex.location.y = 800

        # newmat
        # nodes.new(type='ShaderNodeOutputMaterial')
            # Node = nodes.get("Principled BSDF")
            # color = Node.inputs["Base Color"].default_value[:]
            # print(color)



#選択したイメージテクスチャノードの画像を保存
def save_textures(exportdir):
    path = Path( exportdir )

    mat = bpy.context.active_object.active_material

    nodes = mat.node_tree.nodes
    for node in nodes:
        if node.select:
            nodes.active = node
            if node.type == 'TEX_IMAGE':

                img = node.image
                new_path = str( Path(path) / Path(img.name) )
                root, ext = os.path.splitext(new_path)

                if ext.lower() != '.png':
                    new_path += '.png'

                img.filepath_raw = new_path
                img.file_format = 'PNG'
                img.save()


#選択したイメージテクスチャノードの画像を保存
#要素ごとにフォルダ分けする
def save_textures_():

    subpathes = ( 'Diffuse','Normal' )
    rootpath = Path("e:/tmp/b")

    target_dir = {}
    for path in subpathes:

        dst_dir = rootpath / Path(path)
        target_dir[path] = dst_dir
        os.makedirs(str(dst_dir), exist_ok=True )

    mat = bpy.context.active_object.active_material

    nodes = mat.node_tree.nodes
    for node in nodes:
        if node.select:
            if node.type == 'TEX_IMAGE':

                img = node.image

                for path in subpathes:
                    if img.name.find(path) != -1:

                        new_path = str( target_dir[path] / Path(img.name) )
                        root, ext = os.path.splitext(new_path)

                        if ext.lower() != '.png':
                            new_path += '.png'

                        img.filepath_raw = new_path
                        img.file_format = 'PNG'
                        img.save()



def save_uv():
    #props = bpy.context.scene.cyaimportexport_props
    #meshArray = []

    for obj in utils.selected():

        msh = obj.data
        vertices = obj.data.vertices
        polygons = obj.data.polygons

        # bm = bmesh.new()
        # bm.from_mesh(msh)

        # #頂点の情報
        # vtxCount = str(len(vertices))#頂点数
        # vtxArray = []

        # if props.upvector == 'Maya':
        #     #vector = (v[0],v[2],v[1])
        #     for v in vertices:
        #         vtx = Vtx()
        #         vtxArray.append(vtx)
        #         vtx.co = Vector([ v.co[0] , v.co[2] , -v.co[1] ]) * props.scale

        # elif props.upvector == 'Blender':
        #     #vector = (v[0],v[1],v[2])
        #     for v in vertices:
        #         vtx = Vtx()
        #         vtxArray.append(vtx)
        #         vtx.co = v.co * props.scale


        # for v in vertices:
        #     vtx = Vtx()
        #     vtxArray.append(vtx)
        #     vtx.co = v.co * props.scale

        #ポリゴンの情報
        #polygonCount = str(len(polygons))#頂点数
        polygonArray = []
        UVarray = []
        for face in polygons:
            polygonArray.append(face.vertices)

            #UVの情報
            u_data = []
            v_data = []
            for loop_idx in face.loop_indices:
                uv_coords = obj.data.uv_layers.active.data[loop_idx].uv
                u_data.append(uv_coords.x)
                v_data.append(uv_coords.y)
            UVarray.append([u_data,v_data])


    filename = r'E:\tmp\b\uv.pkl'
    f = open( filename, 'wb' )
    pickle.dump( UVarray, f ,protocol=0)
    f.close()


def load_uv():
    filename = r'E:\tmp\b\uv.pkl'
    f = open(  filename  ,'rb')
    uvdata = pickle.load( f )
    f.close()

    obj = utils.getActiveObj()
    polygons = obj.data.polygons

    #UVの生成
    #uvtex = utils.UV_new(mesh_data)
    #uvtex.name = 'UVset'

    for i,face in enumerate(polygons):
        for loop_idx,uv in zip(face.loop_indices,uvdata[i]):
            uv_coords = obj.data.uv_layers.active.data[loop_idx].uv
            uv_coords.x = uv[0]
            uv_coords.y = uv[1]