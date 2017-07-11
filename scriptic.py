def matchymatchFrame(items = mc.ls(sl=1),direction=1, rotates=[1,1,1], translates=[1,1,1]):
    '''
    This function will take an input object and copy the desired rotates or translates
    into the next frame, useful to keep foot on the floor.
    To use on multiple objects, run this in a for loop.

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
    
matchymatchFrame(rotates=[1,1,1],translates=[0,1,0])
