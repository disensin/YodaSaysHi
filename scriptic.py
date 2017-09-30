import maya.cmds as mc
import splineShapes as ss
import maya.mel as mel
import json

def testing123():
	return mc.warning("Going strong!")

def setColor(self,color = 1):
	'''
	Set the color for the current object.

	self: Object
	color: Pick a color from 1 to
	'''
	self = self or mc.ls(sl=1)[0]
	mc.setAttr( self + ".overrideEnabled",1)
	mc.setAttr( self + '.overrideColor', color)

def zeroEm(zeroMe=None,translate = None, rotate = None, scale = None, all = True):
	'''
	Zero the desired transforms of the first object.
	fromMe: Default is first selected item.

	toYou: Default is second selected item.

	translate: Zero the translation only. Default is False.

	rotate: Zero the rotation only. Default is False.

	scale: Zero the scale only. Default is False.

	all: Zero all transforms. Default is True.

	##
	'''
	zeroMe = zeroMe or mc.ls(sl=1)[0]
	if translate or all: mc.xform(zeroMe,t=([0,0,0]),ws=1)
	if rotate or all: mc.xform(zeroMe,ro=([0,0,0]),ws=1)
	if scale or all: mc.xform(zeroMe,s=([0,0,0]),ws=1)

def matchEm(fromMe=0,toYou=0,translate = 0, rotate = 0, scale = 0, all = 1):
	'''
	Match the desired transforms from first object to second object.
	fromMe: Default is first selected item.

	toYou: Default is second selected item.

	translate: Match the translation only. Default is False.

	rotate: Match the rotation only. Default is False.

	scale: Match the scale only. Default is False.

	all: Match all transforms. Default is True.

	##
	'''
	fromMe = fromMe or mc.ls(sl=1)[0]
	toYou = toYou or mc.ls(sl=1)[1]
	if translate: mc.xform(toYou,t=(mc.xform(fromMe,t=1,ws=1,q=1)),ws=1)
	if rotate: mc.xform(toYou,ro=(mc.xform(fromMe,ro=1,ws=1,q=1)),ws=1)
	if scale: mc.xform(toYou,s=(mc.xform(fromMe,s=1,ws=1,q=1)),ws=1)
	if translate or rotate or scale: mc.select(fromMe,toYou); pass
	elif all: mc.xform(toYou,m=(mc.xform(fromMe,m=1,ws=1,q=1)),ws=1); mc.select(fromMe,toYou)

def matchingShape(name="",shapey='diamond',scaleToObject=True):
	'''Creates a shape at the location of the current object.
	name = "InsertNameHere" # Name the object. Use a string

	shapey = 'shapeYouWantToUse' # Choose from available shapes.

	scaleToObject = True # It will match the new object's scale plus 80% to the master object.
	##
	'''
	name = name or "diamondObj"
	if mc.ls(sl=1):
		object = mc.ls(sl=1)[0]
		name = object + "_diamObj"
	pp,kk,dd = ss.getShape[shapey]

	diamondMe = mc.curve(name = name,p= pp, k=kk, d=dd)

	if mc.ls(sl=1):
		matchEm(fromMe = object,toYou = diamondMe)

	if scaleToObject:
		scaleB2A(object,diamondMe)

	if mc.getAttr(name + '.scaleX') < 0.01:
		# print 'dang, that's one tiny shape'
		mc.setAttr(name + '.scaleX',0.1)
		mc.setAttr(name + '.scaleY',0.1)
		mc.setAttr(name + '.scaleZ',0.1)

	mc.makeIdentity(diamondMe,apply=1,scale=1)

	return diamondMe

def makeJoint(object=''):
	object = object or mc.ls(sl=1)[0]
	mc.select(cl=1)
	return mc.joint(name = object + '_jnt#',p=(mc.xform(object,t=1,q=1,ws=1)))

def addJointChain(pointers=[]):

	for i in range(len(pointers)+1):
		mc.parent(i,(i+1))


# def IkFkMe(pointers=[],ikAim='',ikDefault = False):
# 	pointers = pointers or mc.ls(sl=1)
# 	ikAim = pointers[-1] or
# 	pointerJoints = [makeJoint(i) for i in pointers]
# 	addJointChain(pointers)

# 	mc.parent(pointerJoints[1],pointerJoints[0])
# 	mc.parent(pointerJoints[2],pointerJoints[1])
# 	mc.joint(pointerJoints,edit=1,orientJoint = 'xyz', children = True, zeroScaleOrient = True)

# 	aimWithMe = mc.group(em=1)
# 	matchEm(pointerJoints[1],aimWithMe)
# 	mc.parent(aimWithMe,pointerJoints[1])
# 	mc.xform(aimWithMe,t=[-2,-2,0])

def showShapes():
	return ss.getShape.keys()

def selectAnimatedChildren():
	'''
	Select top most node, run this script. It will find and select all animated children.
	###
	'''
	children = mc.listRelatives(allDescendents=1)

	animChildren = []

	for c in children:
		if mc.keyframe(c, q=1):
			animChildren.append(c)

	mc.select(animChildren)
	mc.warning('Animated children selected.')
	return animChildren

def breakTangs():
	'''Unlock, Free, and Break animation curve tangents.
	#####'''
	mc.keyTangent(edit=1, weightedTangents=True)
	mc.keyTangent(weightLock=False)
	mc.keyTangent(lock=False)

def unifyTangs():
	'''Unify tangents.
	#####'''
	mc.keyTangent(lock=True)

def doubleSideMe(IO=2):
	'''Toggles each item's double-sided-ness.
	IO = 2
		default value, 2, will toggle the current mesh's display.
		1 will enable all double-sided.
		0 will disable all double-sided.
	#####'''
	for i in mc.ls(sl=1):
		if IO == 2:
			value = mc.getAttr(i+".doubleSided")
			mc.setAttr( i+".doubleSided", (not value))
		elif IO == 1:
			mc.setAttr( i+".doubleSided", 1)
		elif IO == 0:
			mc.setAttr( i+".doubleSided", 0)
	mc.warning('Down with the Double-sided-ness!!')

def keyTickDisplay():
	'''Toggle between displaying all active keys or selected channel box.
	#####'''
	playbackSlider = mel.eval('$tmpVar=$gPlayBackSlider')
	active = mc.timeControl(playbackSlider, q=1,showKeysCombined=1)
	if active:
		mc.timeControl(playbackSlider, edit = 1, showKeys = "active")
		mc.warning('All active keys!!')
	else:
		mc.timeControl(playbackSlider, edit = 1, showKeys = "mainChannelBox")

		mc.timeControl(playbackSlider, e=1,showKeysCombined=1)
		mc.warning('Combined keys. Select Channel or show all!')

def deformingListy(gSelect=True, gList=False, gJoints=False, gTransforms=False):
	'''Select mesh, run script.
	Returns list with influences as:
		list[deformingJoints][transforms]
	Get one of the following items:
		gSelect = boolean # Get all the items back as a selection.
		gList = boolean # Get list of all the items.
		gJoints = boolean # Get all the Joints.
		gTransforms = boolean # Get all the Transforms.

	####
	'''
	if gSelect+gList+gJoints+gTransforms != 1:
		return mc.error("Must use only 1 flag!")

	qMeshes = mc.ls(sl=1)

	deformingList = [[],[]]
	for mesh in qMeshes:
		for i in mc.skinCluster(mesh,q=1,influence=1):
			if mc.nodeType(i) == 'joint':
				deformingList[0].append(i)
			else:
				deformingList[1].append(i)
	if gSelect:
		mc.select(deformingList[0],deformingList[1])
	elif gList:
		return deformingList[0],deformingList[1]
	elif gJoints:
		return "Joints: "+str(len(deformingList[0]))
	elif gTransforms:
		return "Transforms: "+str(len(deformingList[1]))
	# return deformingList,"Joints: "+str(len(deformingList[0])),"Transforms: "+str(len(deformingList[1]))

def getOsSep():
	'''Get operating system'''
	if mc.about(os=1) == 'mac':
		return '/'
	elif mc.about(os=1) == 'win64':
		return '\''

def saveIncrementSI():
	'''This function will save an increment of a working Maya file.
	Supported file name format:
	"BIGNAME_sample-animation-name_v004_INITIALS.mb"
	Where the file info is separated with "_" and the version is in the [-2] position.
	'''

	# Get file name and path
	oldName = mc.file(q=1,exn=1)

	# Store file path
	filePath = '/'.join(oldName.split('/')[:-1])

	# Isolate filename
	fileName = oldName.split('/')[-1]

	# Split filename
	modifiedPathList = fileName.split('_')

	# Get the current version of the file
	currentIter = int(modifiedPathList[-2][1:])

	# Calculate the new version and recreate it into a string with a 'v###' format.
	newVer = 'v'+'0'*(3-len(str(currentIter+1)))+str(currentIter+1)

	# Insert the new version number
	modifiedPathList.pop(-2)
	modifiedPathList.insert(-1,newVer)

	# Create the finale Save Path
	savePath = filePath + '/' + '_'.join(modifiedPathList)

	# Save it out!
	mc.file(rename = savePath)
	mc.file(force=1,save=1)

def displaysForAnim(allPanels=0):
	'''Hides all unnecessary items from the viewport.
	Only shows Curves, Polygons, and Image Planes.

	allPanels = False # If True, visibility changes will reverse settings on all panels.
	####
	'''
	demPanels = [mc.getPanel(withFocus=True)]
	if allPanels:
		demPanels = mc.getPanel(vis=1)
	for panelName in demPanels:
		if "modelPanel" in panelName:
			if mc.modelEditor(panelName,query=1,joints=True):
				mc.modelEditor(panelName,edit=1, allObjects = False, nurbsCurves = True, polymeshes = True, imagePlane=True)
				mc.warning('Ready to animate!')
			else:
				mc.modelEditor(panelName,edit=1, allObjects = True)
				mc.warning('Showing everything!')

def playblastCustom():
	'''Create a playblast with the current file-name.
	####
	'''
	# get file name and path
	oldName = mc.file(q=1,exn=1)

	# store file path
	filePath = '/'.join(oldName.split('/')[:-1])

	# isolate filename
	fileName = oldName.split('/')[-1].split('.')[-2]

	# Create Playblast
	mc.playblast(fp=3, offScreen=1, clearCache=1, showOrnaments=0, sequenceTime=0, format='avfoundation', percent=100, filename="movies/"+fileName, viewer=1, quality=100, compression="H.264")

def optimizeFBX(selectToDelete=[]):
	'''Optimizes imported FBX to match settings. Will delete all static channels and desired items.

	selectToDelete = [ "*:JustRig" ] # Use quotations and * as a wild-card.
	'''
	mc.select(clear=1)
	selectToDelete = selectToDelete or ["JustRig",
										"*multiConnect",
										"head_end",
										"blends",
										"eyeAimMain",
										"CharacterSpace",
										"jaw_end"]

	deletedItems = []
	for i in selectToDelete:
		if mc.ls(i):
			mc.select(i,add=1)
		elif mc.ls("*:"+i):
			mc.select("*:"+i,add=1)

	deletedItems = mc.ls(sl=1)
	mc.delete()

	mc.delete(staticChannels=1,all=1)

	keyChannels = [
						'translateX',
						'translateY',
						'translateZ',
						'rotateX',
						'rotateY',
						'rotateZ',
						'scaleX',
						'scaleY',
						'scaleZ'
					]

	mc.select('*:mainGroup',hierarchy=True)

	start,stop = startStopFrames()

	mc.setKeyframe(time=start,attribute=keyChannels)
	mc.setKeyframe(time=stop,attribute=keyChannels)

	mc.warning("Deleted static channels, set book-end keys on everything, and the following items were deleted: ", deletedItems)

def bakeOff(self=[],delCon=0):
	'''
	stops all refreshes and bakes all the 'self' items' channels.
	self = [listOfItems]

	delCon = 0 # Deletes constraints after it is done baking.
	'''
	mc.warning("Baking, please wait . . .")

	self = self or mc.ls(sl=1)

	mc.select(self)
	mc.refresh(suspend=True)

	# Get all the frames in the scene.
	StEn = startStopFrames()

	mc.bakeResults(self,
			sparseAnimCurveBake=False,
			minimizeRotation=True,
			removeBakedAttributeFromLayer=False,
			removeBakedAnimFromLayer=False,
			oversamplingRate=1,
			bakeOnOverrideLayer=False,
			preserveOutsideKeys=True,
			simulation=False,
			sampleBy=1,
			shape=True,
			t=(StEn[0],StEn[1]),
			disableImplicitControl=True,
			controlPoints=False)

	mc.filterCurve(f = 'euler')
	# Enable scene refresh :)
	mc.refresh(suspend=False)
	mc.refresh(force=True)

	mc.select(self)
	if delCon:
		mc.delete(self,cn = 1) # Delete all Constraints

	mc.warning('The range {} has been baked!'.format(StEn))

def startStopFrames():
	''' Returns a list with the start and end frames. It will prioritize range highlight first.

	Returns the frame range as a list with two floats.
	example: [ 0.0 , 125.0 ]
	####
	'''
	timeSlide = mel.eval('$tmpVar=$gPlayBackSlider')
	selectedRange = mc.timeControl(timeSlide,rangeArray=True,q=1)

	if selectedRange[1] - selectedRange[0] == 1:
		selectedRange = [mc.playbackOptions(q=True,min=True),mc.playbackOptions(q=True,max=True)]

	return selectedRange

def bakeShape(constrainToSelected=0):
	'''
	1. Creates a shape
	2. Snaps it to the selected items,
	3. parentConstrains it to the selected item
	4. Bakes the animation
	5. Parent constrains original item to new shape
	##
	'''
	mainList = mc.ls(sl=1)
	bakedList = []

	for mainShape in mainList:
		bakedShape = matchingShape(name=mainShape+"_bakedShape")
		bakedList += [bakedShape]
		mc.parentConstraint(mainShape,bakedShape,w=1)

	bakeOff(bakedList,delCon=1)

	if constrainToSelected:
		for mainShape in mainList:
			mc.parentConstraint(bakedShape,mainShape,w=1)


	mc.select(bakedList)

def IkFk():
	iKfKbake = {'switch':"*:shoulder_L_FKIK_Switch",
				'ik':['*:shoulder_L_IK_PoleVector','*:hand_L_IK_Handle_control'],
				'fk':['*:shoulder_L_FK_control','*:elbow_L_FK_control','*:hand_L_FK_control']}
	iKfKbake['switch']

	#if IK is on
	fkio = iKfKbake['switch']+'.FKIK_Blend'
	if mc.getAttr(fkio):
		pass
	elif not mc.getAttr(fkio):
		pass

def poserLoader(write = False, read = False):
	if write + read != 1:
		mc.error("Use the bool only for READ or WRITE, not both")
		return
	if write:
		poses = {}

		items = mc.ls(sl=1)

		for i in mc.ls(sl=1):
			attributeValues = {}
			for a in mc.listAttr(i,k=1):
				if mc.getAttr(i+'.'+a,se=1):
					attributeValues[a] = mc.getAttr(i+'.'+a)
					poses[i] = attributeValues

		with open('poseLoader.json','w') as outfile:
			json.dump(poses,outfile,indent=4)
		mc.warning("Done writing!")
		return

	elif read:

		gotcha = {}
		with open('poseLoader.json','r') as infile:
			gotcha = json.load(infile)

		if len(mc.ls(sl=1))>0:
			editingThese = mc.ls(sl=1)
		else:
			editingThese = gotcha.keys()

		for i in editingThese:
			if i in gotcha.keys():
				for a in gotcha[i].keys():
					if a in mc.listAttr(i) and mc.getAttr(i+'.'+a,se=1):
						print( "keys set in ",i,a)
						mc.setAttr(i+'.'+a,gotcha[i][a])
		mc.warning("Done reading!")
		return

	mc.error("You must enable either read or write.")

def matchFrame(items = None,direction=1, rotates=[1,1,1], translates=[1,1,1]):
	'''
	This function will take an input object and copy the desired rotates or translates
	into the next frame, useful to keep foot on the floor.
	To use on multiple objects, run this in a for loop.
	example:
	matchFrame(rotates=[1,1,1],translates=[0,1,0])
	    will match all the rotations, and only the Y translate.
	items = mc.ls(sl=1)
	    use these objects. This function will iterate through a list.
	direction = 1
	    enter 1 or -1, depending on which direction to copy the pose to.
	rotates = [1,1,1]
	    input a list of the channels to hold on to. 1 will apply the new value, 0 will maintain the old value.
	translates = [1,1,1]
	    input a list of the channels to hold on to. 1 will apply the new value, 0 will maintain the old value.
	'''

	items = items or mc.ls(sl=1)

	if not items:
		mc.error("Select something first.")

	for item in items:
		fromFrameRot = mc.xform(item,ro=1,q=1,ws=1)
		fromFrameTra = mc.xform(item,t=1,q=1,ws=1)

		print( fromFrameRot, fromFrameTra )
		mc.currentTime(mc.currentTime(q=1)+direction,e=1)

		nextFrameRot = mc.xform(item,ro=1,q=1,ws=1)
		nextFrameTra = mc.xform(item,t=1,q=1,ws=1)

		for r in range(len(rotates)):
			if not rotates[r]:
				fromFrameRot[r] = nextFrameRot[r]

		for t in range(len(translates)):
			if not translates[t]:
				fromFrameTra[t] = nextFrameTra[t]


		print( fromFrameRot, fromFrameTra )

		mc.xform(item, ro= (fromFrameRot), ws=1)
		mc.xform(item, t= (fromFrameTra), ws=1)

def scaleBB(item):
	'''Gets the largest side of the current item's Bounding Box.
	####
	'''
	itemBB= mc.xform(item,bb=1,q=1,ws=1)
	returnSender= 0.0
	for i in range(len(itemBB[:3])):
		checkDifference = itemBB[3+i]-itemBB[i]
		if checkDifference > returnSender:
			returnSender = itemBB[3+i]-itemBB[i]
	return returnSender

def scaleB2A(A=None,B=None,scaleValue=1.7):
	'''Scales incoming B item to match A item, plus 70% larger.
	A,B = mc.ls(sl=1) # A is object 1, B is object 2.
	scaleValue = 1.7 # Scales the matching item up 70%.
	'''
	A,B = A,B or mc.ls(sl=1)
	Alargest,Blargest = scaleBB(A),scaleBB(B)
	differenceBB = Alargest/Blargest
	BoldScale = mc.xform(B,scale=1,q=1,r=1)[0]
	Bfinal = BoldScale*differenceBB*scaleValue
	mc.xform(B,scale=[Bfinal]*3)
	mc.xform(A,bb=1,q=1)

def forceParent(dad = '',sons = [], mOffset = 0):
    '''
    Parents all sons onto dad (the first selected item).
    Will try parent constraint first, then point constraint, then orient constraint.

	dad = selectedItems[0] # will use the first item as the parent.
	sons = selectedItems[1:] # will use from the second object onward.
	mOffset = False
	
	#
    '''
    dad = dad or mc.ls(sl=1)[0]
    sons = sons or mc.ls(sl=1)[1:]

    # For each child, run the parent command!
    for son in sons:
        # Parent Target Object to cube3. If a Parent Constraint doesn't work...
        try:
            mc.parentConstraint( dad, son, weight = 1, mo = mOffset)
        except:
            # ...it will try a Point Constraint. If THAT doesn't work...
            try:
                mc.pointConstraint( dad, son, weight = 1, mo = mOffset)
            # ...do an Orient Constraint!
            except:
                mc.orientConstraint( dad, son, weight = 1, mo = mOffset)

def skipFrame(count=None):
	'''Skip a certain number of frames!
	count=2 # Change this value to a positive or negative number,
			# put it on a hot key or your favorite burger!
	'''
	count = count or 2
	mc.currentTime(mc.currentTime(q=1)+count,e=1)

def freezeWithGroup(item = None):
	'''Freeze the selected item with by creating an empty group,
	match the incoming item's TRS, parent the new group under the item's original parent,
	and parenting the item under the group.

	item = None # Input the item you'd like to perform this action on!
	'''
	item = item or mc.ls(sl=1)[0] # Get the item

	mainParent = mc.listRelatives(item, allParents=1)[0] # Get the item's parent

	newGroup = mc.group(name=(item + '_null'),empty=1) # Make an empty group

	matchEm(item,newGroup) # Match the new group to the item

	mc.makeIdentity(newGroup,apply=1,scale=1) # Freeze the new group's scale

	mc.parent(item,newGroup)

	mc.parent(newGroup,mainParent)
