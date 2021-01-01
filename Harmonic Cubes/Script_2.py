import bpy
import math


cubes = []
count = 0
for x in range(sx,ex,2):
    temp = []
    for y in range(sy,ey,2):
#        dist = (220 - (x**2+y**2))**0.55
        bpy.ops.mesh.primitive_cube_add(location=(x,y,5),scale=(2,2,15))
        temp.append(("Cube."+str((3-len(str(count))) * '0')+str(count)))
        count+=1
    cubes.append(temp.copy())

if cubes[0][0] == 'Cube.000':
    cubes[0].pop(0)
    cubes[0].insert(0,'Cube')

bpy.ops.object.select_all(action='DESELECT')


offSet = 0.0
previousOffSets = [[0.0 for i in range(len(cubes))] for j in range(len(cubes[0]))]

factor = len(cubes)//1.5

for i in range(len(cubes)):
    for j in range(len(cubes[0])):
        previousOffSets[i][j] = ((((i-len(cubes))**2+(j-len(cubes[0]))**2))/200)**0.5 * math.pi * 2


for i in range(rotationCount):
    rotate90Clockwise(previousOffSets)


        
for f in range(0,600,10):
    for r in range(len(cubes)):
        for i in range(len(cubes[r])):
            offSet = previousOffSets[r][i] + math.pi/factor
            previousOffSets[r][i] = offSet
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[cubes[r][i]].select_set(True)
            bpy.ops.transform.resize(value=(1, 1, (3.5+math.sin(offSet))/(3.5+math.sin(offSet-math.pi/factor))), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
            bpy.data.objects[cubes[r][i]].keyframe_insert(data_path="scale",frame=f)
