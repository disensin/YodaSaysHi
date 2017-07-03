# Flatten item motion to the ground! Select all the objects you want, and run this bad boy :)
import maya.cmds as mc
import mAnimLib.mConLib

# Creates a new cube and copies the target's rotation order
def neoCube(target):
    newCube = mAnimLib.mConLib.createCubeCON()
    
    #...match rotation order...
    rotOrder = mc.getAttr( str(target + ".rotateOrder"))
    rotOrderCubeOne = newCube + ".rotateOrder"
    mc.setAttr( rotOrderCubeOne, rotOrder)
    return newCube

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

def forceParent(son,dad):
    # Parent Target Object to cube3. If a Parent Constraint doesn't work...
    try:
        mc.parentConstraint( son, dad, weight = 1)
    except:
        # ...it will try a Point Constraint. If THAT doesn't work...
        try:
            mc.pointConstraint( son, dad, weight = 1)
        # ...do an Orient Constraint!
        except:
            mc.orientConstraint( son, dad, weight = 1)

bakeList = []
targetList = mc.ls(sl = 1) # Get selected objects into a list
print targetList

# Create cubes
for i in range(len(targetList)):
    target = targetList[i] # Put first item in a variable
    
    cleanCube = neoCube(target) # Create follow cube
    cleanCube = mc.rename(cleanCube,(target + '_') + 'cleanCube') # Rename cube to "targetName_cleanCube"
    mc.scale(.6,.6,.6)
    mc.parentConstraint(target,cleanCube,w=1)
    bakeList += [cleanCube] # Add cube to baking list
    
    floorCube = neoCube(target) # Create floor cube
    floorCube = mc.rename(floorCube,(target + '_') + 'floorCube') # Rename cube to "targetName_floorCube"
    mc.rotate(rotateXZ = 1) # Reset X and Z rotations to Zero.
    mc.scale(.8,.8,.8)
    mc.parentConstraint(target,floorCube, w=1,mo=1,sr=['x','z'],st='y') # Constrain floor cube to stay on the floor while following the target object.
    bakeList += [floorCube] # Add cube to baking list
    
    mc.parent(cleanCube,floorCube)

bakeOff(bakeList) #Bake all items in bakeOff list.

# Constrain each target to its assigned cube AND limit Y translation to 0.
for i in range(len(targetList)):
    target = targetList[i]
    cleanCube = bakeList[i*2]
    print cleanCube
    forceParent(cleanCube,target)
    ''' # Enable to limit Y translation!!!
    minVal = mc.getAttr(str(cleanCube + '.translateY'))
    mc.transformLimits ( cleanCube, ty = (minVal, 1), ety = (1 ,0))
    '''
