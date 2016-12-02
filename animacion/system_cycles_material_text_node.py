# cycles_material_text_node.py Copyright (C) 2012, Silvio Falcinelli
#
# Show Information About the Blend.
# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "Cycles Auto Material Texures Node Editor",
    "author": "Silvio Falcinelli",
    "version": (0,1),
    "blender": (2, 6, 2),
    "api": 44136,
    "location": "Properties > Material > Automatic Node Editor ",
    "description": "automatic cycles texture map",
    "warning": "beta",
    "wiki_url": 'http://www.rendering3d.net/' \
        'scripts/materialedior',
    "tracker_url": "https://projects.blender.org/tracker/index.php?" \
        "func=detail&aid=????",
    "category": "System"}


import bpy

def AutoNodeOff():
    mats = bpy.data.materials
    for cmat in mats:
        cmat.use_nodes=False

def AutoNode():
    mats = bpy.data.materials
    for cmat in mats:
        #print(cmat.name)
        cmat.use_nodes=True
        TreeNodes=cmat.node_tree
        links = TreeNodes.links
    
        shader=''
        for n in TreeNodes.nodes:
    
            if n.type == 'TEX_IMAGE' or n.type == 'RGBTOBW':
                TreeNodes.nodes.remove(n)

            if n.type == 'OUTPUT_MATERIAL':
                shout = n       
                        
            if n.type == 'BACKGROUND':
                shader=n              
            if n.type == 'BSDF_DIFFUSE':
                shader=n  
            if n.type == 'BSDF_GLOSSY':
                shader=n              
            if n.type == 'BSDF_GLASS':
                shader=n  
            if n.type == 'BSDF_TRANSLUCENT':
                shader=n     
            if n.type == 'BSDF_TRANSPARENT':
                shader=n   
            if n.type == 'BSDF_VELVET':
                shader=n     
            if n.type == 'EMISSION':
                shader=n 
            if n.type == 'HOLDOUT':
                shader=n   

        if cmat.raytrace_mirror.use and cmat.raytrace_mirror.reflect_factor>0.001:
            print("MIRROR")
            if shader:
                if not shader.type == 'BSDF_GLOSSY':
                    print("MAKE MIRROR SHADER NODE")
                    TreeNodes.nodes.remove(shader)
                    shader = TreeNodes.nodes.new('BSDF_GLOSSY')    # RGB node
                    shader.location = 0,450
                    #print(shader.glossy)
                    links.new(shader.outputs[0],shout.inputs[0]) 
                        
        if not shader:
            shader = TreeNodes.nodes.new('BSDF_DIFFUSE')    # RGB node
            shader.location = 0,450
             
            shout = TreeNodes.nodes.new('OUTPUT_MATERIAL')
            shout.location = 200,400          
            links.new(shader.outputs[0],shout.inputs[0])                
                   
                   
                   
        if shader:                         
            textures = cmat.texture_slots
            for tex in textures:
                                
                if tex:
                    if tex.texture.type=='IMAGE':
                         
                        img = tex.texture.image
                        #print(img.name)  
                        shtext = TreeNodes.nodes.new('TEX_IMAGE')
          
                        shtext.location = -200,400 
        
                        shtext.image=img
        
                        if tex.use_map_color_diffuse:
                            links.new(shtext.outputs[0],shader.inputs[0]) 
    
                        if tex.use_map_normal:
                            t = TreeNodes.nodes.new('RGBTOBW')
                            t.location = -0,300 
                            links.new(t.outputs[0],shout.inputs[2]) 
                            links.new(shtext.outputs[0],t.inputs[0]) 
 


class Refresh(bpy.types.Operator):
    bl_idname = "ml.refresh"
    bl_label = "Refresh"
    bl_description = "Refresh"
    bl_register = True
    bl_undo = True
    @classmethod
    def poll(cls, context):
        return True
    def execute(self, context):
        AutoNode()
        return {'FINISHED'}


class Refresh(bpy.types.Operator):
    bl_idname = "ml.restore"
    bl_label = "Restore"
    bl_description = "Restore"
    bl_register = True
    bl_undo = True
    @classmethod
    def poll(cls, context):
        return True
    def execute(self, context):
        AutoNodeOff()
        return {'FINISHED'}



class OBJECT_PT_scenemassive(bpy.types.Panel):
    bl_label = "Automatic Massive Material Nodes"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    

    def draw(self, context):
        sc = context.scene
        ob_cols = []
        db_cols = []
        layout = self.layout
        l_row = layout.row()
        ob_cols.append(l_row.column())
        layout.separator()
        row = ob_cols[0].row() 
        row.operator("ml.refresh", text='BLENDER > CYCLES', icon='FORCE_TEXTURE')
        layout.separator()
        row = ob_cols[0].row() 
        row.operator("ml.restore", text='BLENDER Mode  (Node Off)', icon='MATERIAL')        
        layout.separator()
        row = ob_cols[0].row() 
        layout.separator()
        row = ob_cols[0].row() 
        layout.separator()
        row = ob_cols[0].row() 
        row.label(text="Ver 0.1 beta  Silvio Falcinelli")
        layout.separator()
        row = ob_cols[0].row() 
        row.label(text="wwww.rendering3d.net")


 
def register():
    bpy.utils.register_module(__name__)
    pass

def unregister():
    bpy.utils.unregister_module(__name__)

    pass

if __name__ == "__main__":
    register()