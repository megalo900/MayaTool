import maya.cmds as commands
import random

class RandomCubeGeneration(object):
    def __init__(self):
        random.seed(1234)

        cubeList = commands.ls('myCube*')

        if len(cubeList)>0:
            commands.delete(cubeList)


        result = commands.polyCube(w=1, h=1, d=1, name='myCube#')
        transformName = result[0]

        instanceGroupName = commands.group(empty=True, name = transformName + '_instanceGroup#')

        for i in range(0, 50):
            instanceCreate = commands.instance(transformName, name=transformName + '_instance#')

            commands.parent(instanceCreate, instanceGroupName)

            x = random.uniform(-10, 10)
            y = random.uniform(0, 20)
            z = random.uniform(-10, 10)
            commands.move(x, y, z, instanceCreate)

            xRot = random.uniform(0, 360)
            yRot = random.uniform(0, 360)
            zRot = random.uniform(0, 360)

            commands.rotate(xRot, yRot, zRot, instanceCreate)

            scalingFactor = random.uniform(0.3, 1.5)

            commands.scale(scalingFactor, scalingFactor, scalingFactor, instanceCreate)

        commands.hide(transformName)

        commands.xform(instanceGroupName, centerPivot=True)

myCode = RandomCubeGeneration()