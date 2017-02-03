"""
ISAI CALDERON
January 25th, 2017
Assignment 01 - Robit machine!!
Instructor: Geordie Martinez
Class: Learn Python Inside Maya
School: CG Society
"""

import maya.cmds as mc



def dPipe(name,radius,height,thickness,subAxis,subCaps,subHeight,troof,trans=(0,0,0),rots=(0,0,0)):
    self = mc.polyPipe(name = 'eye_GEO', r=radius, h=height, t=thickness, sa=subAxis, sc=subCaps, sh=subHeight, rcp=troof)
    mc.xform(self, t = trans, ro=rots, ws=True)
    return self

def dCyl(name,radius,height,subAxis,subCaps,trans=(0,0,0),rots=(0,0,0)):
    self = mc.polyCylinder(name='headCylinder_GEO', r=radius, h=height, sa=subAxis, sc=subCaps)
    mc.xform(self, t = trans, ro=rots, ws=True)
    return self

selectedThingy = mc.ls(sl=1)
selectedThingyCH = mc.listHistory(selectedThingy, fw=True)[1]
print mc.listAttr(selectedThingyCH, k=True)


print mc.getAttr(selectedThingyCH,s=True,cb=True)
print mc.polyPipe(selectedThingy,h=True,query=True)


# GROUP FOR MIRRORED BODY PARTS
leftSideArray = []
rightSideArray = []
mirrorGRP = mc.group(em=True, name='mirror_GRP')

# GROUP FOR THE ROBIT GEO
robitGRP = mc.CreateEmptyGroup()
robitGRP = mc.rename(robitGRP,'robit_GRP')


# HEAD
## EYE
eyeGEO = dPipe('eye_GEO', .3, .8, .1, 20, 3,1,True, (.38,6.857,.865), (90,0,0))
# eyeGEO = mc.polyPipe(name = 'eye_GEO', r=.3, h=.8, t=.1, sa=20, sc=3, sh=1, rcp=True)
# mc.xform(eyeGEO, t = (.38,6.857,.865), ro=(90,0,0), ws=True)
leftSideArray += [eyeGEO]
## HEAD CYLINDER
headCylinderGEO = dPipe('headCylinder_GEO', 1, 1.5, 20, 1,(0,6.392,0,(0,0,0))
# headCylinderGEO = mc.polyCylinder(name='headCylinder_GEO', r=1, h=1.5, sa=20, sc=1)
# mc.xform(headCylinderGEO, t = (0,6.392,0), ro=(0,0,0), ws=True)
mc.parent(headCylinderGEO,robitGRP)
## HEAD CAP
headCapGEO = mc.polySphere(name='headCap_GEO', r=1, sa=20, sh=1)
mc.xform(headCapGEO, t = (0,7.142,0), ro=(0,0,0), ws=True)
mc.parent(headCapGEO,robitGRP)
## ANTENNA BASE
antennaBaseGEO = mc.polySphere(name='antennaBase_GEO', r=.3, sa=20, sh=1)
mc.xform(antennaBaseGEO, t = (0,8.078,0), ro=(0,0,0), ws=True)
mc.parent(antennaBaseGEO,robitGRP)
## ANTENNA CYLINDER
antennaCylinderGEO = mc.polyCylinder(name='antennaCylinder_GEO', r=.1, h=.5, sa=12, sc=1)
mc.xform(antennaCylinderGEO, t = (0,8.234,0), ro=(0,0,0), ws=True)
mc.parent(antennaCylinderGEO,robitGRP)
## ANTENNA SPIKE
antennaSpikeGEO = mc.polyCone(name='antennaSpike_GEO', r=.1, h=3, sa=12, sc=1)
mc.xform(antennaSpikeGEO, t = (0,8.299,0), ro=(0,0,0), ws=True)
mc.parent(antennaSpikeGEO,robitGRP)
## ANTENNA TIP
antennaTipGEO = mc.polySphere(name='antennaTip_GEO', r=.1, sa=20, sh=1)
mc.xform(antennaTipGEO, t = (0,9.799,0), ro=(0,0,0), ws=True)
mc.parent(antennaTipGEO,robitGRP)
## ANTENNA RING 01
antennaRing01GEO = mc.polyTorus(name='antennaRing01_GEO', r=.5, sr=.023, tw=0, sa=20, sh=20)
mc.xform(antennaRing01GEO, t = (0,8.82,0), ro=(-11.813,0,-18.381), ws=True)
mc.parent(antennaRing01GEO,robitGRP)
## ANTENNA RING 02
antennaRing02GEO = mc.polyTorus(name='antennaRing02_GEO', r=.4, sr=.03, tw=0, sa=20, sh=20)
mc.xform(antennaRing02GEO, t = (0,9.334,0), ro=(-0.723,0,13.894), ws=True)
mc.parent(antennaRing02GEO,robitGRP)


# TORSO
## NECK
neckGEO = mc.polyCylinder(name='neck_GEO', r=.4, h=1, sa=20, sh=1, sc=1)
mc.xform(neckGEO, t = (0,5.438,0), ro=(0,0,0), ws=True)
mc.parent(neckGEO,robitGRP)
## CHEST
chestGEO = mc.polyCylinder(name='chest_GEO', r=.8, h=1.5, sa=20, sc=1)
mc.xform(chestGEO, t = (0,4.582,0), ro=(0,0,0), s=(1.22,1,.925), ws=True)
mc.parent(chestGEO,robitGRP)
## EMBLEM
chestEmblemGEO = mc.polyCylinder(name='emblem_GEO', r=.2, h=.5, sa=20, sc=1)
mc.xform(chestEmblemGEO, t = (0.214,4.867,0.522), ro=(90,15.499,0), s=(1,1,1), ws=True)
mc.parent(chestEmblemGEO,robitGRP)
## SHOULDER CAP
shoulderCapGEO = mc.polyCone(name='shoulderCap_GEO', r=.3, h=.01, sa=20, sc=6, rcp=True)
mc.xform(shoulderCapGEO, t = (1.144,4.98,0), ro=(17.548,0,-160.1), s=(1.329,1,1.166), ws=True)
leftSideArray += [shoulderCapGEO]
## SHOULDER BALL
shoulderBallGEO = mc.polySphere(name='shoulderBall_GEO', r=.19, sa=20, sh=20)
mc.xform(shoulderBallGEO, t = (1.26,4.99,0), ro=(0,0,0), ws=True)
leftSideArray += [shoulderBallGEO]
## UPPER CYLINDER
upperCylinderGEO = mc.polyCylinder(name='upperCylinder_GEO', r=.2, h=.1, sa=20, sc=1)
mc.xform(upperCylinderGEO, t = (1.26,4.784,0), ro=(0,0,0), s=(1,1,1), ws=True)
leftSideArray += [upperCylinderGEO]
## UPPER ARM CYLINDER
upperArmGEO = mc.polyCylinder(name='upperArm_GEO', r=.075, h=1.2, sa=20, sc=1)
mc.xform(upperArmGEO, t = (1.26,4.31,0), ro=(0,0,0), s=(1,1,1), ws=True)
leftSideArray += [upperArmGEO]
## ELBOW
elbowGEO = mc.polySphere(name='elbow_GEO', r=.25, sa=20, sh=20)
mc.xform(elbowGEO, t = (1.26,3.71,0), ro=(0,0,0), ws=True)
leftSideArray += [elbowGEO]
## ELBOW CYLINDER
elbowCylinderGEO = mc.polyCylinder(name='elbowCylinder_GEO', r=.4, h=.2, sa=20, sc=1)
mc.xform(elbowCylinderGEO, t = (1.26,3.46,0), ro=(0,0,0), s=(.924,1,1), ws=True)
leftSideArray += [elbowCylinderGEO]
## FOREARM
forearmGEO = mc.polyCylinder(name='forearm_GEO', r=.1, h=1, sa=20, sc=1)
mc.xform(forearmGEO, t = (1.26,3.05,0), ro=(0,0,0), s=(1,1,1), ws=True)
leftSideArray += [forearmGEO]
## WRIST
wristGEO = mc.polyCylinder(name='wrist_GEO', r=.45, h=.8, sa=20, sc=1)
mc.xform(wristGEO, t = (1.26,2.902,0), ro=(0,0,0), s=(1,1,1), ws=True)
leftSideArray += [wristGEO]
## THUMB JOINT 01
thumbJoint01GEO = mc.polyCylinder(name='thumbJoint01_GEO', r=.1, h=.1, sa=20, sc=1)
mc.xform(thumbJoint01GEO, t = (0.989,2.506,0.122), ro=(69.457,0,-90), s=(1,1,1), ws=True)
leftSideArray += [thumbJoint01GEO]
## THUMB 01
thumb01GEO = mc.polyCube(name='thumb01_GEO', w=.2, h=.4, d=.1, sw=1, sh=1, sd=1)
mc.xform(thumb01GEO, t = (0.989,2.313,0.122), ro=(0,-69.457,0), s=(1,1,1), ws=True)
leftSideArray += [thumb01GEO]
## THUMB JOINT 02
thumbJoint02GEO = mc.polyCylinder(name='thumbJoint02_GEO', r=.08, h=.08, sa=12, sc=1)
mc.xform(thumbJoint02GEO, t = (0.989,2.105,0.122), ro=(69.457,0,-90), s=(1,1,1), ws=True)
leftSideArray += [thumbJoint02GEO]
## THUMB 02
thumb02GEO = mc.polyCube(name='thumb02_GEO', w=.2, h=.2, d=.1, sw=1, sh=1, sd=1)
mc.xform(thumb02GEO, t = (0.989,1.982,0.122), ro=(0,-69.457,0), s=(1,1,1), ws=True)
leftSideArray += [thumb02GEO]
## THUMB JOINT 03
thumbJoint03GEO = mc.polyCylinder(name='thumbJoint03_GEO', r=.08, h=.08, sa=12, sc=1)
mc.xform(thumbJoint03GEO, t = (0.989,1.861,0.122), ro=(69.457,0,-90), s=(1,1,1), ws=True)
leftSideArray += [thumbJoint03GEO]
## THUMB 03
thumb03GEO = mc.polyCube(name='thumb03_GEO', w=.2, h=.15, d=.1, sw=1, sh=1, sd=1)
mc.xform(thumb03GEO, t = (0.989,1.768,0.122), ro=(0,-69.457,0), s=(1,1,1), ws=True)
leftSideArray += [thumb03GEO]
## INDEX JOINT 01
indexJoint01GEO = mc.polyCylinder(name='indexJoint01_GEO', r=.1, h=.1, sa=20, sc=1)
mc.xform(indexJoint01GEO, t = (1.315,2.506,0.32), ro=(39.787,0,90), s=(.951,.951,.951), ws=True)
leftSideArray += [indexJoint01GEO]
## INDEX 01
index01GEO = mc.polyCube(name='index01_GEO', w=.2, h=.4, d=.1, sw=1, sh=1, sd=1)
mc.xform(index01GEO, t = (1.315,2.322,0.32), ro=(0,39.787,0), s=(0.951,0.951,0.951), ws=True)
leftSideArray += [index01GEO]
## INDEX JOINT 02
indexJoint02GEO = mc.polyCylinder(name='indexJoint02_GEO', r=.08, h=.08, sa=12, sc=1)
mc.xform(indexJoint02GEO, t = (1.315,2.125,0.32), ro=(39.787,0,90), s=(.951,.951,.951), ws=True)
leftSideArray += [indexJoint02GEO]
## INDEX 02
index02GEO = mc.polyCube(name='index02_GEO', w=.2, h=.35, d=.1, sw=1, sh=1, sd=1)
mc.xform(index02GEO, t = (1.315,1.944,0.32), ro=(0,39.787,0), s=(0.951,0.951,0.951), ws=True)
leftSideArray += [index02GEO]
## MID JOINT 01
midJoint01GEO = mc.polyCylinder(name='midJoint01_GEO', r=.1, h=.1, sa=20, sc=1)
mc.xform(midJoint01GEO, t = (1.465,2.504,0.147), ro=(60,0,90), s=(1,1,1), ws=True)
leftSideArray += [midJoint01GEO]
## MID 01
mid01GEO = mc.polyCube(name='mid01_GEO', w=.2, h=.35, d=.1, sw=1, sh=1, sd=1)
mc.xform(mid01GEO, t = (1.465,2.311,0.147), ro=(0,60,0), s=(1,1,1), ws=True)
leftSideArray += [mid01GEO]
#mc.parent(mid01GEO,mirrorGRP)
## MID JOINT 02
midJoint02GEO = mc.polyCylinder(name='midJoint02_GEO', r=.08, h=.08, sa=12, sc=1)
mc.xform(midJoint02GEO, t = (1.465,2.103,0.147), ro=(60,0,90), s=(1,1,1), ws=True)
leftSideArray += [midJoint02GEO]
## MID 02
mid02GEO = mc.polyCube(name='mid02_GEO', w=.2, h=.35, d=.1, sw=1, sh=1, sd=1)
mc.xform(mid02GEO, t = (1.465,1.912,0.147), ro=(0,60,0), s=(1,1,1), ws=True)
leftSideArray += [mid02GEO]
## PINKY JOINT 01
pinkyJoint01GEO = mc.polyCylinder(name='pinkyJoint01_GEO', r=.1, h=.1, sa=20, sc=1)
mc.xform(pinkyJoint01GEO, t = (1.545,2.506,-0.086), ro=(77.734,0,90), s=(0.951,0.951,0.951), ws=True)
leftSideArray += [pinkyJoint01GEO]
## PINKY 01
pinky01GEO = mc.polyCube(name='pinky01_GEO', w=.2, h=.4, d=.1, sw=1, sh=1, sd=1)
mc.xform(pinky01GEO, t = (1.545,2.322,-0.086), ro=(0,77.734,0), s=(0.951,0.951,0.951), ws=True)
leftSideArray += [pinky01GEO]
## PINKY JOINT 02
pinkyJoint02GEO = mc.polyCylinder(name='pinkyJoint02_GEO', r=.08, h=.08, sa=12, sc=1)
mc.xform(pinkyJoint02GEO, t = (1.545,2.125,-0.086), ro=(77.734,0,90), s=(0.951,0.951,0.951), ws=True)
leftSideArray += [pinkyJoint02GEO]
## PINKY 02
pinky02GEO = mc.polyCube(name='pinky02_GEO', w=.2, h=.35, d=.1, sw=1, sh=1, sd=1)
mc.xform(pinky02GEO, t = (1.545,1.944,-0.086), ro=(0,77.734,0), s=(0.951,0.951,0.951), ws=True)
leftSideArray += [pinky02GEO]
## WAIST
waistGEO = mc.polyCylinder(name='waist_GEO', r=.5, h=.4, sa=20, sc=1)
mc.xform(waistGEO, t = (0,3.76,0), ro=(0,0,0), s=(1,1,1), ws=True)
mc.parent(waistGEO,robitGRP)

# BOTTOM HALF
## BELT
beltGEO = mc.polyCylinder(name='belt_GEO', r=.65, h=.3, sa=20, sc=1)
mc.xform(beltGEO, t = (0,3.531,0), ro=(0,0,0), s=(1.3,1,.969), ws=True)
mc.parent(beltGEO,robitGRP)
## BELT BUCKLE 01
buckle01GEO = mc.polyPipe(name='buckle01_GEO', r=.2, h=.25, t=.05, sa=20, sc=0)
mc.xform(buckle01GEO, t = (0,3.516,.631), ro=(90,0,0), s=(1,1,1), ws=True)
mc.parent(buckle01GEO,robitGRP)
## BELT BUCKLE 02
belt02GEO = mc.polyCylinder(name='belt02_GEO', r=.145, h=.2, sa=20, sc=1)
mc.xform(belt02GEO, t = (0,3.531,.631), ro=(90,0,0), s=(1,1,1), ws=True)
mc.parent(belt02GEO,robitGRP)
## HIP
hipGEO = mc.polyCone(name='hip_GEO', r=.6, h=.01, sa=20, sc=10, rcp=True)
mc.xform(hipGEO, t = (0,3.589,0), ro=(0,0,0), s=(1.153,1,1), ws=True)
mc.parent(hipGEO,robitGRP)
## SOCKET CYLINDER
socketCylinderGEO = mc.polyCylinder(name='socketCylinder_GEO', r=.45, h=.25, sa=20, sc=1)
mc.xform(socketCylinderGEO, t = (0.368,3.293,0.023), ro=(-10.084,0,34.591), s=(1,1,1), ws=True)
leftSideArray += [socketCylinderGEO]
## SOCKET TORUS
socketTorusGEO = mc.polyTorus(name='socketTorus_GEO', r=.35, sr=.1, tw=0, sa=20, sh=20)
mc.xform(socketTorusGEO, t = (0.438,3.192,0.045), ro=(-10.084,0,34.591), ws=True)
leftSideArray += [socketTorusGEO]
## HIP JOINT
hipJointGEO = mc.polySphere(name='hipJoint_GEO', r=.3, sa=20, sh=20)
mc.xform(hipJointGEO, t = (0.529,3.059,0.074), ro=(0,0,0), ws=True)
leftSideArray += [hipJointGEO]
## FEMUR
femurGEO = mc.polyCylinder(name='femur_GEO', r=.12, h=1.2, sa=20, sc=1)
mc.xform(femurGEO, t = (0.529,2.379,0.074), ro=(0,0,0), s=(1,1,1), ws=True)
leftSideArray += [femurGEO]
## KNEE
kneeGEO = mc.polySphere(name='knee_GEO', r=.3, sa=20, sh=20)
mc.xform(kneeGEO, t = (0.529,1.779,0.074), ro=(0,0,0), ws=True)
leftSideArray += [kneeGEO]
## SHIN
shinGEO = mc.polyCylinder(name='shin_GEO', r=.1, h=1, sa=20, sc=1)
mc.xform(shinGEO, t = (0.529,1.119,0.074), ro=(0,0,0), s=(1,1,1), ws=True)
leftSideArray += [shinGEO]
## SHIN GUARD
shinGuardGEO = mc.polyCylinder(name='shinGuard_GEO', r=.45, h=.8, sa=20, sc=1)
mc.xform(shinGuardGEO, t = (0.529,1.059,0.074), ro=(0,0,0), s=(.833,1,1), ws=True)
leftSideArray += [shinGuardGEO]
## ANKLE
ankleGEO = mc.polySphere(name='ankle_GEO', r=.3, sa=20, sh=20)
mc.xform(ankleGEO, t = (0.529,.516,0.074), ro=(0,0,0), ws=True)
leftSideArray += [ankleGEO]
## FOOT
footGEO = mc.polyCone(name='foot_GEO', r=.8, h=.01, sa=20, sc=12, rcp=True)
mc.xform(footGEO, t = (0.529,0,0.374), ro=(-180,0,0), s=(.619,.68,1), ws=True)
leftSideArray += [footGEO]

## RENAME AND CREATE GEO TO MIRROR
for i in range(0,len(leftSideArray)):
    leftSideArray[i][0] = mc.rename(leftSideArray[i][0], 'left_' + leftSideArray[i][0]) ## RENAME LEFT SIDE
    rightItem = mc.duplicate(leftSideArray[i][0], name = 'right_' + leftSideArray[i][0][5:]) ## DUPLICATE AND RENAME RIGHT SIDE
    mc.parent(leftSideArray[i][0], robitGRP) ## ADD LEFT-SIDE GEO TO MAIN GRP
    mc.parent(rightItem,mirrorGRP) ## ADD RIGHT-SIDE GEO TO MIRROR GRP


mc.scale(-1,1,1,mirrorGRP,xyz=True) ## MIRROR THE RIGHT SIDE ITEMS
rightSideArray = mc.ls(mirrorGRP,dag=1)[1::2] ## ADD RIGHT-SIDE ITEMS TO ARRAY...
mc.parent(rightSideArray, robitGRP) ## ...AND PUT THEM ALL INTO THE MAIN GRP
mc.delete(mirrorGRP) ## DELETE THE MIRROR GRP

mc.select(robitGRP) ## SELECT THE ROBOT'S GROUP!

## FIN


