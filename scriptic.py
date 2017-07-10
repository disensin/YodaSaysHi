def matchFrame(direction=1, rotates=[1,1,1], translates=[1,1,1]):
    
    if not mc.ls(sl=1):
        mc.error("Select something first.")
        
    thisFrame = mc.ls(sl=1)[0]
    
    fromFrameRot = mc.xform(thisFrame,ro=1,q=1,ws=1)
    fromFrameTra = mc.xform(thisFrame,t=1,q=1,ws=1)
    
    print fromFrameRot, fromFrameTra 
    mc.currentTime(mc.currentTime(q=1)+direction,e=1)
    
    nextFrameRot = mc.xform(thisFrame,ro=1,q=1,ws=1)
    nextFrameTra = mc.xform(thisFrame,t=1,q=1,ws=1)
    
    for r in range(len(rotates)):
        if not rotates[r]:
            fromFrameRot[r] = nextFrameRot[r]
            
    for t in range(len(translates)):
        if not translates[t]:
            fromFrameTra[t] = nextFrameTra[t]
    
    
    print fromFrameRot, fromFrameTra 
    #return
    

    mc.xform(thisFrame, ro= (fromFrameRot), ws=1)
    mc.xform(thisFrame, t= (fromFrameTra), ws=1)
    
