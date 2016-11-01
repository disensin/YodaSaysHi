'''
Isai Calderon

#! WARNING: This code will run the bake tool twice. Be patient.

This code will take the selection with Motion Capture Data and create 3 cubes:
    Cube 1 will have a cleaned-up version of the selection's motion
    Cube 2 will have the raw data
    Cube 3 will be parented directly under Cube 1, but it will have the offsets of Cube 2
    The original object will be constrained to Cube 3
    
Edit Cube 3's peaks and valleys to clean up all the raw data!

'''
import maya.cmds as mc
import mAnimLib.mConLib

# Bake keys!
def bakeTweaks(bakeTweakMe):
    # Stop refreshing the scene while this code runs
    mc.refresh(suspend=True)
    
    # Get all the frames in the scene.
    startingFrame = mc.playbackOptions( query = 1, min = 1)
    endingFrame = mc.playbackOptions( query = 1, max = 1)
    mc.bakeResults( bakeTweakMe,
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

def tweakMeToHell():
    # Get selected object(s)
    tweakTargetArray = mc.ls (sl = True)
    
    # If nothing is selected, tell user to select at least one object!
    if len(tweakTargetArray) == 0:
        mc.error( "Please select at least one object!")
    
    tweakCubeOneArray = []
    tweakCubeTwoList = []
    tweakCubeThreeList = []
    
    for tweakTarget in tweakTargetArray:
        
        # Create the first cube...
        tweakCubeOne = mAnimLib.mConLib.createCubeCON()
        tweakCubeOne = mc.rename(tweakCubeOne, (tweakTarget + '_cleanupCube_#'))
        print tweakTarget, tweakCubeOne
        
        #...constrain it to the target
        mc.parentConstraint( tweakTarget, tweakCubeOne, weight = 1)
        
        #...match rotation order...
        rotOrder = mc.getAttr( str(tweakTarget + ".rotateOrder"))
        rotOrderCubeOne = tweakCubeOne + ".rotateOrder"
        mc.setAttr( rotOrderCubeOne, rotOrder)
        
        #...add to list...
        tweakCubeOneArray += [tweakCubeOne]
    
    ###end Loop 1
    
    
    
    #...and bake animation.
    bakeTweaks(tweakCubeOneArray)
    
    
    for i in range(len(tweakCubeOneArray)):
        
        # Delete constraint.
        tweakCubeOne = tweakCubeOneArray[i]
        mc.select(tweakCubeOne)
        mc.delete(cn = 1)
        
        # Delete baked Scale and Visibility Animation, set both to 1.
        mc.cutKey(  tweakCubeOne,
                    cl = 1,
                    at = ('sx','sy','sz','v'))
        
        mc.setAttr( (tweakCubeOne + '.scaleX'), 1.0)
        mc.setAttr( (tweakCubeOne + '.scaleY'), 1.0)
        mc.setAttr( (tweakCubeOne + '.scaleZ'), 1.0)
        mc.setAttr( (tweakCubeOne + '.visibility'), 1.0)
        
        # Dulpicate cube1 with graphs, now cube2
        tweakCubeTwoList += mc.duplicate( rr = 1, un = 1)
        tweakCubeTwo = tweakCubeTwoList[i]
        print tweakCubeOneArray
        mc.scale(.8,.8,.8)
        
        # Duplicate cube1 without graphs, , place cube3 into a list, parent cube3 to cube1
        mc.select(tweakCubeOne)
        
        # Dulpicate cube1 with graphs, now cube2
        tweakCubeThreeList += mc.duplicate( rr = 1, un = 1)
        tweakCubeThree = tweakCubeThreeList[i]
        
        
        # List the appropriate cube2 to work with.
        tweakCubeTwo = tweakCubeTwoList[i]
        mc.parent( tweakCubeThree, tweakCubeOne)
        
        mc.parentConstraint(tweakCubeTwo, tweakCubeThree, weight = 1)
        
        .041667938234999996
        
        # Clean up cube1 graphs
        mc.select(tweakCubeOne)
        mc.bufferCurve(animation = 'keys', overwrite = 0)
        mc.filterCurve( f = 'simplify', timeTolerance = .05)
        print tweakCubeThreeList
            
    print tweakCubeThreeList
    # Bake cube3!
    bakeTweaks(tweakCubeThreeList)
    
    
    
    for i in range(len(tweakCubeOneArray)):
        
        # Delete baked Scale and Visibility Animation for cube3, set both to 1.
        tweakCubeThree = tweakCubeThreeList[i]
        mc.cutKey(  tweakCubeThree,
                    cl = 1,
                    at = ('sx','sy','sz','v'))
        mc.setAttr( (tweakCubeThree + '.scaleX'), .9)
        mc.setAttr( (tweakCubeThree + '.scaleY'), .9)
        mc.setAttr( (tweakCubeThree + '.scaleZ'), .9)
        mc.setAttr( (tweakCubeThree + '.visibility'), 1.0)
        
        # Delete constraint.
        mc.select(tweakCubeThree)
        mc.delete(cn = 1)
        
        # Parent Target Object to cube3. If a Parent Constraint doesn't work...
        try:
            mc.parentConstraint( tweakCubeThree, tweakTargetArray[i], weight = 1)
        except:
            # ...it will try a Point Constraint. If THAT doesn't work...
            try:
                mc.pointConstraint( tweakCubeThree, tweakTargetArray[i], weight = 1)
            # ...do an Orient Constraint!
            except:
                mc.orientConstraint( tweakCubeThree, tweakTargetArray[i], weight = 1)
        
    
    '''
    mc.bufferCurve(animation = 'keys', overwrite = 0)
    mc.filterCurve( f = 'simplify', timeTolerance = .041667938)
    '''
    print "Done!"
    
tweakMeToHell()
