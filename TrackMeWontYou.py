import maya.cmds as mc

selectedObjects = mc.ls(sl = 1)

def cubeMe(getMe):
    splinedCube = mc.curve(
        degree = 1,
        point = [
            (1, 1, 1),
            (1,-1,1),
            (1,-1,-1),
            (1,1,-1),
            (-1,1,-1),
            (-1,-1,-1),
            (-1,-1,1),
            (-1,1,1),
            (1,1,1),
            (1,-1,1),
            (-1,-1,1),
            (-1,1,1),
            (-1,1,-1),
            (-1,-1,-1),
            (1,-1,-1),
            (1,1,-1),
            (1,1,1)
        ],
        knot = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16))

    splinedCube = mc.rename(splinedCube, getMe+'_curveCube')
    mc.matchTransform(splinedCube, getMe)
    return splinedCube

def bakeOff(self):
    # Select objects to bake, accepts lists, single objects, any kind of variable with an object stored in it
    mc.select(self)
    mc.refresh(suspend=True)

    # Get all the frames in the scene.
    startingFrame = mc.playbackOptions( query = 1, min = 1)
    endingFrame = mc.playbackOptions( query = 1, max = 1)
    mc.bakeResults( self,
                    at = ['tx','ty','tz','rx','ry','rz'],
                    simulation = 1,
                    time = (startingFrame, endingFrame),
                    sampleBy = 1,
                    disableImplicitControl = 1,
                    preserveOutsideKeys = 1,
                    sparseAnimCurveBake = 0,
                    removeBakedAttributeFromLayer = 0,
                    removeBakedAnimFromLayer = 1,
                    bakeOnOverrideLayer = 0,
                    minimizeRotation = 1,
                    controlPoints = 0,
                    shape = 1
                    )
    mc.filterCurve(f = 'euler')

    # Enable scene refresh :)
    mc.refresh(suspend=False)
    mc.refresh(force=True)

    mc.select(self)
    mc.delete(cn = 1)

targetCubeOffset = cubeMe(selectedObjects[0])
targetCubeOffset = mc.rename(targetCubeOffset,
                             (selectedObjects[0] + '_offset_curveCube'))


targetCubeBaked = cubeMe(selectedObjects[0])
mc.scale(.8,.8,.8, targetCubeBaked)
targetCubeBaked = mc.rename(targetCubeBaked,
                            (selectedObjects[0] + '_baked_curveCube'))

if len(selectedObjects) == 2:
    targetCubeDad = cubeMe(selectedObjects[1])
    targetCubeDad = mc.rename(targetCubeDad,
                              (selectedObjects[0] + '_dad_curveCube'))


mc.parent(targetCubeBaked,targetCubeOffset)
if len(selectedObjects) == 2:
    mc.parent(targetCubeOffset,targetCubeDad)

mc.parentConstraint(selectedObjects[0],targetCubeBaked)

bakeOff(targetCubeBaked)
