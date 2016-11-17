import maya.cmds as mc
import mAnimLib.mConLib

weapon = mc.ls(sl = 1)
bakeMyReTarget = []

'''
handRetargeter
    weaponOffsetControl
        weaponMain
targetHandMain
'''


# Original Hand control
handMain = weapon[1]
mAnimLib.mConLib.createCubeCON()
handRetargeter = mc.rename(handMain+'_retargeter_handSource')
mc.parentConstraint(handMain, handRetargeter)
mc.scale(1.5,1.5,1.5)

# Weapon Offset control
mAnimLib.mConLib.createCubeCON()
weaponOffsetControl = mc.rename(handMain+'_retargeter_offset')
mc.scale(1.25,1.25,1.25)
mc.parent(weaponOffsetControl, handRetargeter)
mc.makeIdentity(a=1, s=1)


# Main weapon control
weaponMain = weapon[0]
mAnimLib.mConLib.createCubeCON()
weaponMainRetargeter = mc.rename(weaponMain+'_retargeter_weapon')
mc.parent(weaponMainRetargeter, weaponOffsetControl)
mc.parentConstraint(weaponMain, weaponMainRetargeter)


# Target Hand control
targetHandMain = weapon[2]
mAnimLib.mConLib.createCubeCON()
targetHandRetargeter = mc.rename(targetHandMain+'_retargeter_handTarget')
mc.parentConstraint(targetHandMain, targetHandRetargeter)
mc.scale(3,3,3)

bakeMyRetarget = mc.ls(weaponMainRetargeter,handRetargeter,targetHandRetargeter)


# Bake hand and weapon
# Stop refreshing the scene while this code runs
mc.refresh(suspend=True)

# Get all the frames in the scene.
startingFrame = mc.playbackOptions( query = 1, min = 1)
endingFrame = mc.playbackOptions( query = 1, max = 1)
mc.bakeResults( bakeMyRetarget,
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
# Clean up all the rotation curves
mc.filterCurve(f = 'euler')

# Enable scene refresh :)
mc.refresh(suspend=False)
mc.refresh(force=True)

mc.select(bakeMyRetarget)
mc.delete(cn = 1)

mc.parentConstraint(targetHandMain, targetHandRetargeter)
mc.parentConstraint(targetHandRetargeter, handRetargeter)

mc.select(weaponOffsetControl)
mc.ScaleToolWithSnapMarkingMenu()
'''
for i in range(len(weapon)):
    weaponOriginal = weapon[i]
    
    mAnimLib.mConLib.createCubeCON()
    weaponRetargeter = mc.rename(weaponOriginal+'_retargeter')
    
    mc.parentConstraint(weaponOriginal, weaponRetargeter)
    '''
