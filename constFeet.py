import maya.cmds as mc

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

# Snap second object (kid) to parent obect (pops)
def snapTo(pops,kid):
    mc.parentConstraint(pops,kid,mo=0)
    mc.select(mc.listRelatives(c=1,typ = 'constraint'))
    mc.delete()

def yLimitMe(self):
    minVal = mc.getAttr(str(self + '.translateY'))
    mc.transformLimits ( self, ty = (minVal, 1), ety = (1 ,0))


# Get the foot list
footList = addFeetHere('L')

# Create scene variables...
foot = footList[0]
ball = footList[1]
toe = footList[2]
pinky = footList[3]
biggie = footList[4]
heel = footList[5]

# ...and organize them into a list
footList = [foot,
            ball,
            toe,
            pinky,
            biggie,
            heel]
footListLOC = [] # List for the locators to be created

headGroup = mc.group(em=True, name = (footList[0] + '_flatFootted_rig')) # Parent Null to store everything

# Create a locator for each item and store in the "footListLOC". Parent each one under "headGroup"
for i in range(len(footList)):
    item = footList[i]
    nullItem = mc.group(em=True, name=(item + '_null' ))
    snapTo(item,nullItem)
    mc.parent(nullItem, headGroup)
    footListLOC += [nullItem]

# Get each new locator labeled
footLOC = footListLOC[0]
ballLOC = footListLOC[1]
toeLOC = footListLOC[2]
pinkyLOC = footListLOC[3]
biggieLOC = footListLOC[4]
heelLOC = footListLOC[5]

# Ball setup.
mc.parentConstraint(ballLOC,foot,mo=1)
FootMcNUL = mc.pickWalk(foot,d='up')
mc.parentConstraint(FootMcNUL,ballLOC,mo=1)
yLimitMe(ballLOC)

# Heel setup. pConst from: footLOC to BallLOC toFootMcNUL
mc.parentConstraint(FootMcNUL,heelLOC,mo=1)
mc.aimConstraint(heelLOC,ballLOC,mo=1)



