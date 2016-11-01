'''
Isai Calderon
What it does:
    Scales 
Instructions:
    Find the exact Start Frame and End Frame you want your shot to convert from.
Edits:
    v2.1 20161010
    - Now selects all the animation keys to scale. No need to select them in the Dope Sheet any more!
    - Added Debugging information
    v2
    - Now with input!!
'''

import maya.cmds as mc
import mAnimLib.mScene

def scaleMeLikeOneOfYourFrenchGirls():
    
    # Enter the first and last frames from the Avids file in 30 FPS.
    stFrame = input("Enter the first frame from the edit:")
    oldEnFrame = input("Enter the last frame from the edit:")
    
    # Get frame range to approved in/out
    mAnimLib.mScene.setShotTimeline()
    
    # Find old frame length
    oldFrLength = oldEnFrame - stFrame
    # Find new frame length
    newFrLength = (mc.playbackOptions( query = 1, max = 1) - 8) - (mc.playbackOptions( query = 1, min = 1) + 8)
    
    print (mc.playbackOptions( query = 1, max = 1) - 8) - (mc.playbackOptions( query = 1, min = 1) + 8)
    print newFrLength
    
    # Find new end-frame
    newEnFrame = stFrame + newFrLength
    
    #Find time multiplier
    tiMul = newFrLength / oldFrLength
    
    # Select all animation keys.
    mc.selectKey(mc.ls(typ = "animCurve"))
    
    # Scale keys from 30FPS to 24FPS. It will use the new time calculations (A, B, C, and D) as the pivot point.
    mc.scaleKey(    scaleSpecifiedKeys = 1,
                    timeScale = tiMul,
                    timePivot = (stFrame),
                    floatScale = tiMul,
                    floatPivot = (stFrame),
                    valueScale =  1,
                    valuePivot = 0)
    
    # Shift all frames to new start time to start at 1009 (assuming 8 frame handles AND start frame 1001.
    # The script will calculate for Frame Length changes approved by production as well)
    e = (mc.playbackOptions( query = 1, min = 1) + 8) - stFrame
    mc.keyframe( animation = 'keys', option = 'over', relative = 1, timeChange = (0 + e))
    
    '''
    # Set time slider to start at 1001 and end at the Shot's last frame (Double-check with the "in/out" Mel button)
    mc.playbackOptions( min = 1001.0, max = (1009.0 + 8.0 + newFrLength))
    '''
    
    mc.currentTime( mc.playbackOptions( query = 1, min = 1) + 8 )
    
    print "---Results (Useful for debugging)---"
    print "Start Frame: " + str(float(stFrame))
    print "Old end frame: " + str(float(oldEnFrame))
    print "New Frame Length: " + str(newFrLength) + " = " + str((mc.playbackOptions( query = 1, max = 1) - 8) - (mc.playbackOptions( query = 1, min = 1) + 8))
    print "Old Frame Length: " + str(oldFrLength)
    print "New End Frame: " + str(newEnFrame)
    print "Time Multiplier: " + str(tiMul)
    print "------------------------------------"
    

scaleMeLikeOneOfYourFrenchGirls()

print "Done!! Double-check it out :) Go to frames " + str(mc.playbackOptions( query = 1, min = 1) + 8) + " and frame " + str(mc.playbackOptions( query = 1, max = 1) - 8)
