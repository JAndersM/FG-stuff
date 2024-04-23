#Blender python file
#Print animation info for objects named *axis asumed to be a line object
import bpy


for col in bpy.data.collections:
   for obj in col.objects:
       if obj.name.endswith("axis"):
           name=obj.name
           v0=obj.matrix_world @ obj.data.vertices[0].co
           v1=obj.matrix_world @ obj.data.vertices[1].co
           print(name)
#           print("  <center>")
#           print("    <x-m> {0:.4f} </x-m>".format((v0.x+v1.x)/2))
#           print("    <y-m> {0:.4f} </y-m>".format((v0.y+v1.y)/2))
#           print("    <z-m> {0:.4f} </z-m>".format((v0.z+v1.z)/2))
#           print("  </center>")
#           v=v1 -v0
#           print("  <axis>")
#           print("    <x-m> {0:.4f} </x-m>".format(v.x))
#           print("    <y-m> {0:.4f} </y-m>".format(v.y))
#           print("    <z-m> {0:.4f} </z-m>".format(v.z))
#           print("  </axis>")
           print("  <axis>")
           print("    <x1-m> {0:.4f} </x1-m>".format(v0.x))
           print("    <y1-m> {0:.4f} </y1-m>".format(v0.y))
           print("    <z1-m> {0:.4f} </z1-m>".format(v0.z))
           print("    <x2-m> {0:.4f} </x2-m>".format(v1.x))
           print("    <y2-m> {0:.4f} </y2-m>".format(v1.y))
           print("    <z2-m> {0:.4f} </z2-m>".format(v1.z))
           print("  </axis>")
