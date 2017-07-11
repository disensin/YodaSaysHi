def matchFrame(items = mc.ls(sl=1),direction=1, rotates=[1,1,1], translates=[1,1,1]):
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
    
    if not items:
        mc.error("Select something first.")
        
    items = items or mc.ls(sl=1)
    
    for item in items:
        fromFrameRot = mc.xform(item,ro=1,q=1,ws=1)
        fromFrameTra = mc.xform(item,t=1,q=1,ws=1)
        
        print fromFrameRot, fromFrameTra 
        mc.currentTime(mc.currentTime(q=1)+direction,e=1)
        
        nextFrameRot = mc.xform(item,ro=1,q=1,ws=1)
        nextFrameTra = mc.xform(item,t=1,q=1,ws=1)
        
        for r in range(len(rotates)):
            if not rotates[r]:
                fromFrameRot[r] = nextFrameRot[r]
                
        for t in range(len(translates)):
            if not translates[t]:
                fromFrameTra[t] = nextFrameTra[t]
        
        
        print fromFrameRot, fromFrameTra 

        mc.xform(item, ro= (fromFrameRot), ws=1)
        mc.xform(item, t= (fromFrameTra), ws=1)
    

def bakeOff(self):
    '''
    stops all thebakes all the 'self' items' X Y Z values, then deletes constraints.
    '''
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

def snapToFirstItem(fromMe=None,toYou=None):
    '''
    INPUT: Snaps the first selected item to the second item. If there's a selection, it'll snap the second object to the first.

    OUTPUT: The items are then selected in the same order.

    fromMe - string item, get the location from this one

    toYou - string item, apply location to this one
    '''

    if mc.ls(sl=1): # If there's a selection
        fromMe = mc.ls(sl=1)[0]
        toYou = mc.ls(sl=1)[1]
    mc.xform(toYou, ro= (mc.xform(fromMe,ro=1,q=1,ws=1)), ws=1)
    mc.xform(toYou, t= (mc.xform(fromMe,t=1,q=1,ws=1)), ws=1)
    mc.select(fromMe,toYou)


def forceParent(dad = mc.ls(sl=1)[0],sons = mc.ls(sl=1)[1:], mOffset = 0):
    '''
    Parents all sons onto dad (the first selected item).
    Will try parent constraint first, then point constraint, then orient constraint.
    '''
    
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
