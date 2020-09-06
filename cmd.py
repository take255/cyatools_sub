import bpy
import imp

from mathutils import ( Matrix)

from . import utils
imp.reload(utils)




#---------------------------------------------------------------------------------------
#Invert selected object using last selection.
#---------------------------------------------------------------------------------------
def invert_last_selection():    
    amt = utils.getActiveObj()
    selected = utils.selected()
    matrix = Matrix(amt.matrix_world)
    matrix.invert()

    utils.deselectAll()

    for ob in selected:
        if ob != amt:
            m = ob.matrix_world
            ob.matrix_world = matrix @ m
            utils.act(ob)
            bpy.ops.object.transform_apply( location = True , rotation=True , scale=True )


#---------------------------------------------------------------------------------------
#選択オブジェクトのコレクションをハイド
#---------------------------------------------------------------------------------------
def collection_hide():
    selected = utils.selected()
    layer = bpy.context.window.view_layer.layer_collection

    for ob in selected:
        for col in ob.users_collection:
            show_collection_by_name(layer ,col.name , True)

#---------------------------------------------------------------------------------------
#ビューレイヤーを名前で表示状態切替
#---------------------------------------------------------------------------------------
def show_collection_by_name(layer ,name , state):
    props = bpy.context.scene.cyatools_oa
    children = layer.children

    if children != None:
        for ly in children:
            if name == ly.name:
                ly.hide_viewport = state                

            show_collection_by_name(ly , name , state)
