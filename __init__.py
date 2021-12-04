# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
from bpy.types import(
    PropertyGroup,
    Operator,
    )
import imp

from bpy.props import(
    StringProperty,
    BoolProperty,
    PointerProperty
    )

from . import display
from . import utils
from . import cmd
from . import cc3pipeline



imp.reload(display)
imp.reload(utils)
imp.reload(cmd)
imp.reload(cc3pipeline)


bl_info = {
"name": "cyatools sub",
"author": "Takehito Tsuchiya",
"version": (0, 1.1),
"blender": (2, 93, 1),
#"location" : "CYA",
"location": "Shader Editor",
"warning": "",
"category": "Node",

"description": "cyatools sub",
#"category": "Object"
}


class CYATOOLSSUB_Props_OA(PropertyGroup):
    const_bool : BoolProperty(name="const" , update = display.tgl_constraint)
    showhide_bool : BoolProperty(name="child" , update = display.tgl_child)
    showhide_collection_bool : BoolProperty(name="" , update = display.tgl_collection)
    focus_bool : BoolProperty(name="focus" ,  default = False)


#---------------------------------------------------------------------------------------
#UI
#---------------------------------------------------------------------------------------
class CYATOOLSSUB_PT_toolPanel(utils.panel):
    bl_label ='SUB Tools'
    bl_category = "Node"
    bl_idname = "CYATOOLSSUB_PT_toolPanel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"

    def draw(self, context):
        props = bpy.context.scene.cyatoolssub_oa
        layout=self.layout

        box = layout.box()
        box.label( text = 'display toggle' )

        row1 = box.row()
        box2 = row1.box()

        row2 = box2.row()
        row2.prop(props, "const_bool" , icon='CONSTRAINT')#コンストレインのON、OFF
        row2.prop(props, "showhide_bool" , icon='EMPTY_DATA')#選択した子供のみ表示


        box2.prop(props, "focus_bool")


        box1 = row1.box()
        box1.label( text = 'collection' )

        row1 = box1.row()
        row1.prop(props, "showhide_collection_bool" , icon='GROUP')
        row1.operator( "cyatoolssub.preserve_collections" , icon = 'IMPORT')
        row1.operator( "cyatoolssub.collections_hide" )

        #CC3パイプラインツール
        box = layout.box()
        box.label( text = 'CC3 pipeline' )
        row1 = box.row()

        row1.operator( "cyatoolssub.collect_textures" )
        row1.operator( "cyatoolssub.save_textures" )
        row1.operator( "cyatoolssub.save_uv" )
        row1.operator( "cyatoolssub.load_uv" )



# class CYATOOLSSUB_OT_instance_invert_last_selection(Operator):
#     """Inverse selected objects using last selection."""
#     bl_idname = "cyatoolssub.instance_invert_last_selection"
#     bl_label = "invert using last selection"
#     def execute(self, context):
#         cmd.invert_last_selection()
#         return {'FINISHED'}

#選択したモデルの所属するコレクションをハイド
class CYATOOLSSUB_OT_collections_hide(Operator):
    """選択したオブジェクトが属するコレクションをハイド"""
    bl_idname = "cyatoolssub.collections_hide"
    bl_label = "hide"
    def execute(self, context):
        cmd.collection_hide()
        return {'FINISHED'}

# #現在のコレクション表示状態を保持する
class CYATOOLSSUB_OT_preserve_collections(Operator):
    """現在のコレクション表示状態を保持する"""
    bl_idname = "cyatoolssub.preserve_collections"
    bl_label = ""
    def execute(self, context):
        display.preserve_collections()
        return {'FINISHED'}


#---------------------------------------------------------------------------------------
#
#CC3パイプラインツール
#
#---------------------------------------------------------------------------------------

class CYATOOLSSUB_OT_save_textures(Operator):
    bl_idname = "cyatoolssub.save_textures"
    bl_label = "save textures"

    #filepath : bpy.props.StringProperty(subtype="FILE_PATH")
    #filename : StringProperty()
    directory : StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        cc3pipeline.save_textures(self.directory)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}



#テクスチャを１マテリアルに集める
class CYATOOLSSUB_OT_collect_textures(Operator):
    """新規マテリアルを生成してテクスチャを集める"""
    bl_idname = "cyatoolssub.collect_textures"
    bl_label = "collect textures"
    def execute(self, context):
        cc3pipeline.collect_textures()
        return {'FINISHED'}


#UVの保存
class CYATOOLSSUB_OT_save_uv(Operator):
    """新規マテリアルを生成してテクスチャを集める"""
    bl_idname = "cyatoolssub.save_uv"
    bl_label = "save uv"
    def execute(self, context):
        cc3pipeline.save_uv()
        return {'FINISHED'}

#UVの保存
class CYATOOLSSUB_OT_load_uv(Operator):
    """新規マテリアルを生成してテクスチャを集める"""
    bl_idname = "cyatoolssub.load_uv"
    bl_label = "load uv"
    def execute(self, context):
        cc3pipeline.load_uv()
        return {'FINISHED'}



classes = (
    CYATOOLSSUB_Props_OA,
    CYATOOLSSUB_PT_toolPanel,
    #CYATOOLSSUB_OT_instance_invert_last_selection,
    CYATOOLSSUB_OT_collections_hide,
    CYATOOLSSUB_OT_preserve_collections,

    CYATOOLSSUB_OT_collect_textures,
    CYATOOLSSUB_OT_save_textures,

    CYATOOLSSUB_OT_save_uv,
    CYATOOLSSUB_OT_load_uv,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cyatoolssub_oa = PointerProperty(type=CYATOOLSSUB_Props_OA)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.cyatoolssub_oa
