import maya.cmds as mc
import mAnimLib.mConLib

foot = ''
ball = ''
toe = ''
pinky = ''
biggie = ''
heel = ''

def neoCube(target):
    newCube = mAnimLib.mConLib.createCubeCON()
    
    #...match rotation order...
    rotOrder = mc.getAttr( str(target + ".rotateOrder"))
    rotOrderCubeOne = newCube + ".rotateOrder"
    mc.setAttr( rotOrderCubeOne, rotOrder)
    return newCube

# Here all the feet controls are collected into a list
def addFeetHere(side):
    footList = []
    foot = '*:*:%sfootCON' % side
    ball = '*:*:%sballCON' % side
    toe = '*:*:%stoeCON' % side
    pinky = '*:*:%sFootOutPivotNUL' % side
    biggie = '*:*:%sFootInPivotNUL' % side
    heel = '*:*:%sFootHeelPivotNUL' % side
    fList = [foot, ball, toe, pinky, biggie, heel]
    for i in range(len(fList)):
        allItems = (mc.listRelatives ( fList[i] ))
    
        self = mc.select(allItems[0])
        footList += mc.pickWalk (d = 'up')
    return footList

# Create the cubes that will inherit the motion capture data.
def addLoactorCubes(self):
    bakeDems = []
    for i in range(len(self)):
        if i == 0:
            continue
        target = mc.ls(self)[i]
        mc.select( target )
        targetBox = neoCube(target) # Create follow cube
        targetBox = mc.rename(targetBox,(target + '_') + 'modBox') # Rename cube to "targetName_cleanCube"
        mc.scale(.05,.3,.05)
        if i == 1:
            mc.parentConstraint(self[0],targetBox,w=1,mo=1)
        if i == 2:
            mc.move(0,.2,0,r = 1)
            mc.scale(.05,.05,.05)
            mc.parentConstraint(target,targetBox,w=1,mo=1)
        if i == 3 or i == 4:
            mc.parentConstraint(self[2],targetBox,w=1,mo=1)
        if i == 5:
            mc.parentConstraint(target,targetBox,w=1)
        bakeDems += [targetBox] # Add cube to baking list
        
    return bakeDems

# Use this to bake anything's T and R
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
    mc.delete(cn = 1) # Delete all Constraints

### Main process HERE!!
bakeCubes = []
bakeList = []

leftFootItems = addFeetHere('L')
rightFootItems = addFeetHere('R')

print leftFootItems
print rightFootItems
### End maing process HERE!!

bakeList += addLoactorCubes(leftFootItems)
bakeList += addLoactorCubes(rightFootItems)

mc.select(bakeList)

bakeOff(bakeList)

#Next up, constrain everything to the foot!!


