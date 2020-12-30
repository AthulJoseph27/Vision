import bpy
import math

        
cubes = []
count = 0
for x in range(-8,9,1):
    temp = []
    for y in range(-8,9,1):
        bpy.ops.mesh.primitive_cube_add(location=(x,y,5))
        temp.append(("Cube."+str((3-len(str(count))) * '0')+str(count)))
        bpy.context.object.dimensions = [1, 1, 8]
        count+=1
    cubes.append(temp.copy())


cubes[0].pop(0)
cubes[0].insert(0,'Cube')
bpy.ops.object.select_all(action='DESELECT')


offSet = 0.0
      
for f in range(0,600,10):
    offSet+=math.pi/4
    for r in range(len(cubes)):
        for i in range(len(cubes[r])):
            dist = (((r-8)**2+(i-8)**2)**0.5) / ((64)**0.5) * math.pi  + offSet
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[cubes[r][i]].select_set(True)
            bpy.context.selected_objects[0].dimensions = [1, 1, (8 + 4 * math.sin(dist))]
            bpy.data.objects[cubes[r][i]].keyframe_insert(data_path="scale",frame=f)