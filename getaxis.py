#Blender python file
#Print vertex coords for objects named *axis asumed to be a line object
import bpy

for col in bpy.data.collections:
   for obj in col.objects:
       if obj.name.endswith("axis"):
           v0=obj.matrix_world @ obj.data.vertices[0].co
           v1=obj.matrix_world @ obj.data.vertices[1].co
           print(obj.name)
           print("<axis>")
           print("<x1-m> {0:.4f} </x1-m>".format(v0.x))
           print("<y1-m> {0:.4f} </y1-m>".format(v0.y))
           print("<z1-m> {0:.4f} </z1-m>".format(v0.z))
           print("<x2-m> {0:.4f} </x2-m>".format(v1.x))
           print("<y2-m> {0:.4f} </y2-m>".format(v1.y))
           print("<z2-m> {0:.4f} </z2-m>".format(v1.z))
           print("</axis>")
