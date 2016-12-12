import maya.cmds as mc
import mAnimLib.mConLib

# Parent Target Object to cube3. If a Parent Constraint doesn't work...
def forcedParenting(daddy,sonny):
    try:
        mc.parentConstraint( daddy, sonny, weight = 1)
    except:
        # ...it will try a Point Constraint. If THAT doesn't work...
        try:
            mc.pointConstraint( daddy, sonny, weight = 1)
        # ...do an Orient Constraint!
        except:
            mc.orientConstraint( daddy, sonny, weight = 1)
                
def bakeOff(self):
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

cubeList = []
targetList = mc.ls(sl = 1)
target = targetList[0]

mAnimLib.mConLib.createCubeCON()
cubeOne = mc.rename(target + '_cube1')
cubeList += [cubeOne]

mAnimLib.mConLib.createCubeCON()
cubeTwo = mc.rename(target + '_cube2')
mc.scale(0.8,0.8,0.8)
cubeList += [cubeTwo]

mc.parent(cubeTwo,cubeOne)

mc.parentConstraint(target,cubeTwo)
mc.parentConstraint(target, cubeOne, mo = True, skipTranslate = 'y', weight = 1)

bakeOff(cubeList)

forcedParenting(cubeTwo, target)
