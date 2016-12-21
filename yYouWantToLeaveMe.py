import maya.cmds as mc
import mAnimLib.mConLib

foot = ''
ball = ''
toe = ''
pinky = ''
biggie = ''
heel = ''
leftFootList = []
rightFootList = []

# Parent son to dad
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
        if side == 'L':
            leftFootList = footList
        elif side == 'R':
            rightFootList = footList
    return footList
    
def addFootCubes(self):
    # Add cubes
    bakeDems = []
    for i in range(len(self)):
        if i == 0: # Skip foot control
            continue
        target = mc.ls(self)[i]
        mc.select( target )
        targetBox = neoCube(target) # Create follow cube
        targetBox = mc.rename(targetBox,(target + '_') + 'modBox') # Rename cube to "targetName_modBox"
        mc.scale(.05,.3,.05)
        if i == 1: # Ball of foot
            mc.parentConstraint(self[0],targetBox,w=1,mo=1)
        if i == 2: # Toe control
            mc.move(-0.2,0.2,0,r = 1,os=1,wd=1)
            mc.scale(.05,.05,.05)
            mc.parentConstraint(target,targetBox,w=1,mo=1)
            mc.select( target )
            toeBox = neoCube(target) # Create follow cube
            toeBox = mc.rename(toeBox,(target + '_toe_') + 'modBox') # Rename cube to "targetName_modBox"
            mc.scale(.13,.13,.13)
            mc.parentConstraint(target,toeBox,w=1)
            bakeDems += [toeBox]
            
        if i == 3 or i == 4: # Pinky and Big Toe controls
            mc.parentConstraint(self[2],targetBox,w=1,mo=1)
        if i == 5: # Heel control
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

# Create retargetting cubes
def createRetargetingCubes(self):
    retargetCubes = []
    sourceList = self
    targetList = [sourceList[0],sourceList[3],sourceList[4],sourceList[5]] # Get selected objects into a list EXCEPT Toe Aim Control
    print targetList
    for i in range(len(targetList)):
        target = targetList[i] # Put first item in a variable
        
        cleanCube = neoCube(target) # Create follow cube
        cleanCube = mc.rename(cleanCube,(target + '_') + 'cleanCube') # Rename cube to "targetName_cleanCube"
        mc.scale(.14,.14,.14)
        mc.parentConstraint(target,cleanCube,w=1)
        retargetCubes += [cleanCube] # Add cube to baking list
        
        floorCube = neoCube(target) # Create floor cube
        floorCube = mc.rename(floorCube,(target + '_') + 'floorCube') # Rename cube to "targetName_floorCube"
        mc.rotate(rotateXZ = 1) # Reset X and Z rotations to Zero.
        mc.scale(.2,.2,.2)
        mc.parentConstraint(target,floorCube, w=1,mo=1,sr=['x','z'],st='y') # Constrain floor cube to stay on the floor while following the target object.
        retargetCubes += [floorCube] # Add cube to baking list
        
        mc.parent(cleanCube,floorCube)
    return retargetCubes


### Main process HERE!!
bakeList = []
trackingLocators = []

# Get foot control names
leftFootTargets = addFeetHere('L')
rightFootTargets = addFeetHere('R')

# Create source controls
leftFootItems = addFootCubes(leftFootTargets)
rightFootItems = addFootCubes(rightFootTargets)
bakeList += leftFootItems
bakeList += rightFootItems

toeMain = leftFootTargets[2]

# Create retargetting controls
leftRetargets = createRetargetingCubes(leftFootItems)
rightRetargets = createRetargetingCubes(rightFootItems)
print leftFootItems

bakeList += leftRetargets
bakeList += rightRetargets

### End maing process HERE!!
mc.select(bakeList)

print bakeList
bakeOff(bakeList)

#Next up, constrain everything to the foot!!

targets = leftFootTargets
modBoxes = leftFootItems
retargets = leftRetargets

print targets
print modBoxes
print retargets
mc.select(modBoxes)

footMain = targets[0]
ballMain = targets[1]
toeMain = targets[2]
pinkyToeMain = targets[3]
biggieMain = targets[4]
heelMain = targets[5]

ballModBox = modBoxes[0]
toeModBox = modBoxes[1]
aimModBox = modBoxes[2]
pinkyModBox = modBoxes[3]
biggieModBox = modBoxes[4]
heelModBox = modBoxes[5]


mc.parentConstraint(ballModBox,footMain,mo=1,w=1)
mc.aimConstraint( heelModBox,
                  ballModBox,
                  mo=1,
                  w=1,
                  aimVector = [1, 0, 0,],
                  upVector = [0, 1, 0],
                  worldUpType = "object",
                  worldUpObject = aimModBox)
mc.pointConstraint(toeModBox,toeMain,w=1)
mc.orientConstraint(toeModBox,toeMain,
                    offset = [0, 0, 0],
                    skip = ['y', 'z'],
                    weight = 1)
mc.pointConstraint(biggieModBox,toeModBox,w=0.5,mo=1)
mc.pointConstraint(pinkyModBox,toeModBox,w=0.5,mo=1)
mc.parentConstraint(biggieModBox,aimModBox,w=0.5,mo=1)
mc.parentConstraint(pinkyModBox,aimModBox,w=0.5,mo=1)
mc.cutKey(toeModBox,
          cl = 1,
          t = [0:],
          f = [0:],
          at = ['ry','rz'])
mc.aimConstraint( biggieModBox,
                  toeModBox,
                  mo=1,
                  w=1,
                  aimVector = [0, 0, 1,],
                  upVector = [0, 1, 0],
                  worldUpType = "object",
                  worldUpObject = aimModBox,
                  sk = ['y','z'])



### MUST HAPPEN AT THE END ###
# Constrain each target to its assigned cube AND limit Y translation to 0.
targetList = [ballModBox,pinkyModBox,biggieModBox,heelModBox] # Get selected objects into a list EXCEPT Toe Aim Control
print targetList
print retargets
for i in range(len(targetList)):
    #i = 1
    target = targetList[i]
    cleanCube = retargets[i*2]
    print target
    print cleanCube
    #if i == 0:
    mc.pointConstraint(cleanCube,target,w=1,mo=1)
    #elif i == 1:
    #    mc.parentConstraint(cleanCube,toeModBox,w=1,mo=1)
    #else:
    #    forceParent(cleanCube,target)
    # Enable to limit Y translation!!!
    minVal = mc.getAttr(str(cleanCube + '.translateY'))
    mc.transformLimits ( cleanCube, ty = (minVal, 1), ety = (1 ,0))
    
    

