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

# from . import modifierlist
# from . import rigtools
# from . import importexport
# from . import objectlist
# from . import idmaptools
# from . import ue4tools

imp.reload(display)
imp.reload(utils)
imp.reload(cmd)
# imp.reload(modifierlist)
# imp.reload(rigtools)
# imp.reload(importexport)
# imp.reload(objectlist)
# imp.reload(idmaptools)
# imp.reload(ue4tools)

bl_info = {
"name": "cyatools sub",
"author": "Takehito Tsuchiya",
"version": (0, 1),
"blender": (2, 80, 3),
"description": "cyatools sub",
"category": "Object"}


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


        #self.layout.operator("cyatools.apply", icon='BLENDER')
        # self.layout.operator("cyatools.modelingtools", icon='BLENDER')
        # self.layout.operator("cyatools.cya_helper_tools", icon='BLENDER')
        # self.layout.operator("cyatools.curvetools", icon='BLENDER')
        # self.layout.operator("cyatools.rename", icon='BLENDER')
        # self.layout.operator("cyatools.skinningtools", icon='BLENDER')
        # self.layout.operator("cyatools.etc", icon='BLENDER')


# #メッセージダイアログ
# #スペース区切りで改行する
# class CYATOOLS_MT_messagebox(bpy.types.Operator):
#     bl_idname = "cyatools.messagebox"
#     bl_label = ""
 
#     message : bpy.props.StringProperty(
#         name = "message",
#         description = "message",
#         default = ''
#     )
 
#     def execute(self, context):
#         self.report({'INFO'}, self.message)
#         print(self.message)
#         return {'FINISHED'}
 
#     def invoke(self, context, event):
#         return context.window_manager.invoke_props_dialog(self, width = 400)
 
#     def draw(self, context):
#         buf = self.message.split(' ')
#         for s in buf:
#             self.layout.label(text = s)
#         #self.layout.label("")



class CYATOOLSSUB_OT_instance_invert_last_selection(Operator):
    """Inverse selected objects using last selection."""
    bl_idname = "cyatools.instance_invert_last_selection"
    bl_label = "invert using last selection"
    def execute(self, context):
        cmd.invert_last_selection()
        return {'FINISHED'}

#選択したモデルの所属するコレクションをハイド
class CYATOOLS_OT_collections_hide(Operator):
    """選択したオブジェクトが属するコレクションをハイド"""
    bl_idname = "cyatoolssub.collections_hide"
    bl_label = "hide"
    def execute(self, context):
        cmd.collection_hide()
        return {'FINISHED'}

# #現在のコレクション表示状態を保持する
class CYATOOLS_OT_preserve_collections(Operator):
    """現在のコレクション表示状態を保持する"""
    bl_idname = "cyatoolssub.preserve_collections"
    bl_label = ""
    def execute(self, context):
        display.preserve_collections()
        return {'FINISHED'}




classes = (
    CYATOOLSSUB_Props_OA,
    CYATOOLSSUB_PT_toolPanel,
    CYATOOLSSUB_OT_instance_invert_last_selection,
    CYATOOLS_OT_collections_hide,
    CYATOOLS_OT_preserve_collections,    
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.cyatoolssub_oa = PointerProperty(type=CYATOOLSSUB_Props_OA)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.cyatoolssub_oa
    