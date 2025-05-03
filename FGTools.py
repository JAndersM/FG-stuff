bl_info = {
    "name": "FG Tools",
    "author": "jam007",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D",
    "description": "Tools for Flightgear development",
    "warning": "",
    "doc_url": "",
    "category": "Tools",
}

import os
import math
import bpy
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector


class FGA_add_Axis(bpy.types.Operator, AddObjectHelper):
    """Create a new Axis Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Axis Object"
    bl_options = {'REGISTER', 'UNDO'}

    scale: bpy.props.FloatVectorProperty(
        name="scale",
        default=(1.0, 1.0, 1.0),
        subtype='TRANSLATION',
        description="scaling",
    )

    def execute(self, context):
        self.add_object(self, context)
        return {'FINISHED'}
    
    def add_axis(self, context):
        scale_z = self.scale.z

        verts = [
            Vector((0, 0, -0.5*scale_z)),
            Vector((0, 0, 0.5*scale_z)),
        ]

        edges = [[0,1]]
        faces = []

        mesh = bpy.data.meshes.new(name="Axis")
        mesh.from_pydata(verts, edges, faces)
        object_data_add(context, mesh, operator=self)            

class FG_PT_Tools_Panel(bpy.types.Panel):
    bl_label = "FG Tools"
    bl_idname = "FGTools_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "FG Tools"

    def draw(self, context):
        layout = self.layout
        myprops = context.scene.myprops
        rw=layout.row()
        rw.prop(myprops, "file")
        
         
class FG_PT_Animation_Panel(bpy.types.Panel):
    bl_label = "Make Animation"
    bl_idname = "FGAnimation_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "FG Tools"
    bl_options = {'DEFAULT_CLOSED'}
    
    knob=False

    def draw(self, context):
        layout = self.layout
        myprops = context.scene.myprops
        layout.prop(myprops, "object")
        layout.prop(myprops, "animname")
        layout.prop(myprops, "type_enum")
        layout.prop(myprops, "prop")
        layout.prop(myprops, "axis_enum")
        layout.prop(myprops, "factor")
        brow=layout.column()
        brow.prop(myprops, "bind_enum")
        brow.prop(myprops, "biprop")
        brow.enabled=self.knob
        row = layout.row()
        row.operator("fga.exportanim")
        
class FG_OT_Animation_Operator(bpy.types.Operator):
    bl_label = "Export Animation"
    bl_idname = "fga.exportanim"
    
    def execute(self, context):
        myprops = context.scene.myprops
        selection = bpy.context.selected_objects
        active = bpy.context.active_object
        if len(active.data.vertices) ==2 :
            axobj=True
        else:
            axobj=False 
        text="<animation>\n"
        if myprops.animname != "":
            text=text+"    <name>"+myprops.animname+"</name>\n"
        for obj in selection:
            if obj != active or axobj==False:
                text=text+"    <object-name>"+obj.name+"</object-name>\n"
        match myprops.type_enum:
            case "R":
                at="rotate"
            case "S":
                at="spin"
            case "T":
                at="translate"
            case "K":
                at="knob"
            case _:
                at="***"
        text=text+"    <type>"+at+"</type>\n" \
        +"    <property>"+myprops.prop+"</property>\n" \
        +"    <factor>"+str(myprops.factor)+"</factor>\n    <center>\n" \
        +"        <x-m>"+str(active.location[0])+"</x-m>\n" \
        +"        <y-m>"+str(active.location[1])+"</y-m>\n" \
        +"        <z-m>"+str(active.location[2])+"</z-m>\n    </center>\n"
        if axobj :
            if myprops.object :
                text=text+"    <axis>\n        <object-name>"+active.name+"<object-name>\n    </axis>\n"
            else :
                v0=active.matrix_world @ active.data.vertices[0].co
                v1=active.matrix_world @ active.data.vertices[1].co
                text=text+"    <axis>\n        <x1-m>"+str(v0.x)+"</x1-m>\n" \
                +"        <y1-m>"+str(v0.y)+"</y1-m>\n" \
                +"        <z1-m>"+str(v0.z)+"</z1-m>\n" \
                +"        <x2-m>"+str(v1.x)+"</x2-m>\n" \
                +"        <y2-m>"+str(v1.y)+"</y2-m>\n" \
                +"        <z2-m>"+str(v0.z)+"</z2-m>\n    </axis>\n"
        else :
            text=text+"    <axis>\n"
            match myprops.axis_enum:
                case "Xp" :
                     text=text+"        <x>1</x>\n        <y>0</y>\n        <z>0</z>\n"
                case "Xn" :
                     text=text+"        <x>-1</x>\n        <y>0</y>\n        <z>0</z>\n"
                case "Yp" :
                     text=text+"        <x>0</x>\n        <y>1</y>\n         <z>0</z>\n"
                case "Yn" :
                     text=text+"        <x>0</x>\n        <y>-1</y>\n        <z>0</z>\n"
                case "Zp" :
                     text=text+"        <x>0</x>\n        <y>0</y>\n        <z>1</z>\n"
                case "Zn" :
                     text=text+"        <x>0</x>\n        <y>0</y>\n        <z>-1</z>\n"
                case _ :
                    text=text+"****\n"
            text=text+"    </axis>\n"
        if myprops.bind_enum !="None" :
            text=text+"    <action>\n        <binding>\n"
            match myprops.bind_enum:
                case "PA" :
                     text=text+"            <command>property-assign</command>\n"
                case "PC" :
                     text=text+"            <command>property-cycle</command>\n"
                case "PD" :
                     text=text+"            <command>property-adjust</command>\n"
                case "PT" :
                     text=text+"            <command>property-toggle</command>\n"
                case _ :
                    text=text+"****\n"
            text=text+"            <property>"+myprops.biprop+"</property>\n\n" \
            +"        </binding>\n    </action>\n"
        text=text+"</animation>\n"            
        export(myprops.file, text)      
        return {'FINISHED'}    

class FG_PT_Effects_Panel(bpy.types.Panel):
    bl_label = "Make Effect"
    bl_idname = "FGEffect_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "FG Tools"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        myprops = context.scene.myprops
        layout.prop(myprops, "inherits")
        layout.operator("fga.exporteff")
        
class FG_OT_Effects_Operator(bpy.types.Operator):
    bl_label = "Export Effect"
    bl_idname = "fga.exporteff"
    
    def execute(self, context):
        myprops = context.scene.myprops
        selection = bpy.context.selected_objects
        text="<effect>\n    <inherits-from>"+myprops.inherits+"</inherits-from>\n"
        for obj in selection:
            text=text+"    <object-name>"+obj.name+"<object-name>\n"
        text=text+"</effect>\n"
        export(myprops.file, text)
        return {'FINISHED'}   

class FG_PT_Model_Panel(bpy.types.Panel):
    bl_label = "Place Model"
    bl_idname = "FGModel_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "FG Tools"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        myprops = context.scene.myprops
        layout.prop(myprops, "modelpath")
        layout.operator("fga.exportmodel")
        
class FG_OT_Model_Operator(bpy.types.Operator):
    bl_label = "Export Model placement"
    bl_idname = "fga.exportmodel"
    
    def execute(self, context):
        active = bpy.context.active_object
        myprops = context.scene.myprops
        text="<model>\n    <name>"+active.name+"</name>\n" \
        +"    <path>"+myprops.modelpath+"</path>\n    <offsets>\n" \
        +"        <x-m>"+str(active.location[0])+"</x-m>\n" \
        +"        <y-m>"+str(active.location[1])+"</y-m>\n" \
        +"        <z-m>"+str(active.location[2])+"</z-m>\n" \
        +"        <pitch-deg>"+str(math.degrees(active.rotation_euler[1]))+"</pitch-deg>\n" \
        +"        <heading-deg>"+str(math.degrees(active.rotation_euler[2]))+"</heading-deg>\n" \
        +"        <roll-deg>"+str(math.degrees(active.rotation_euler[0]))+"</roll-deg>\n" \
        +"    </offsets>\n</model>\n"
        export(myprops.file, text)
        return {'FINISHED'}

def update_func(self, context):
    if context.scene.myprops.type_enum=="K":
        FG_PT_Animation_Panel.knob=True
    else:
        FG_PT_Animation_Panel.knob=False
            
class MyProperties(bpy.types.PropertyGroup):
    file : bpy.props.BoolProperty(name="Export to file", default=False)
    object : bpy.props.BoolProperty(name="Use Axis Obj", description="Export axle as object", default=True)
    type_enum : bpy.props.EnumProperty(
        name="Type",
        description="Select type",
        items= [
            ("R", "Rotate", "Rotation animation"),
            ("S", "Spin", "Spin animation"),
            ("T", "Translate", "Translate animation"),
            ("K", "Knob", "Knob animation")
            ],
            update=update_func)
    bind_enum : bpy.props.EnumProperty(
        name="Binding",
        description="Select Binding",
        items= [
            ("None", "-", "No binding"),
            ("PA", "Assign", "Property Assign"),
            ("PC", "Cycle", "Property Cycle"),
            ("PD", "Adjust", "Property Adjust"),
            ("PT", "Toggle", "Property Toggle"),
            ])
    axis_enum : bpy.props.EnumProperty(
        name="Axis",
        description="Select Axis",
        items= [
            ("Xp", "+X", "+X axis through origin"),
            ("Xn", "-X", "-X axis through origin"),
            ("Yp", "+Y", "+Y axis through origin"),
            ("Yn", "-Y", "-Y axis through origin"),
            ("Zp", "+Z", "+Z axis through origin"),
            ("Zn", "-Z", "-Z axis through origin"),
            ("O", "Other", "Other axis through origin"),
            ])
    animname : bpy.props.StringProperty(name="Name", default="")
    prop : bpy.props.StringProperty(name="Property", default="surface-positions/")
    biprop : bpy.props.StringProperty(name="Bound Pr.", default="")
    factor : bpy.props.FloatProperty(name="Factor", default=1.0)
    inherits : bpy.props.StringProperty(name="Inherits", default="Effects/")
    modelpath : bpy.props.StringProperty(name="Path", default="Model/")

        
def export(file, text):
    if file:
        with open(os.path.dirname(bpy.data.filepath)+"/export.xml", "a") as f:
            f.write(text+"\n")
    else :
        print(text+"\n");
 
def add_axis_button(self, context):
    self.layout.operator(
        FGA_add_Axis.bl_idname,
        text="Add Axis",
        icon='IPO_LINEAR')

classes = [FGA_add_Axis, FG_PT_Tools_Panel,
            FG_PT_Animation_Panel, FG_OT_Animation_Operator,
            FG_PT_Effects_Panel, FG_OT_Effects_Operator,
            FG_PT_Model_Panel, FG_OT_Model_Operator,
            MyProperties
          ]
  
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.myprops = bpy.props.PointerProperty(type=MyProperties)
    bpy.types.VIEW3D_MT_mesh_add.append(add_axis_button)
 
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.myprops
    bpy.types.VIEW3D_MT_mesh_add.remove(add_axis_button)
 
if __name__ == "__main__":
    register()
