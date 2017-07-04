'''
To run, place script in your Scripts folder, then use this code:

import pivotic;reload(pivotic);pivotic.PivotIC().createPivot() # This code creates a pivot on the selected item

import pivotic;reload(pivotic);pivotic.PivotIC().setKeyOnMainItem() # This code sets a key on the item that is being controlled

import pivotic;reload(pivotic);pivotic.PivotIC().removePivotTool() # This code removes the pivot tool.

'''

import maya.cmds as mc

class PivotIC(object):
    
    def __init__(self):
        '''
        Initialize the Class variable. In this case, get the selected objects.
        If the selected object already has a Pivot Tool applied on it, load the variables.
        '''
        if len(mc.ls(sl=1)) == 0 : # If nothing is selected, create the variables.
            self.pivotGroup,self.diamondCtrl,self.pivotCtrl,self.basePivotAnchor='','','',''
            self.pivotItems = [self.pivotGroup,self.diamondCtrl,self.pivotCtrl,self.basePivotAnchor]

        elif mc.ls(sl=1): # If there's a selection, engage the variables
            self.items = mc.ls(sl=1)

            self.pivotList = mc.ls('*_pivotTool_*')
            if len(self.items[0].split('_pivot'))>1: # Here we check if a selected item belongs to a pivot tool
                self.items = [self.items[0].split('_pivot')[0]] # If it does, replace self.item with the actual object's name.

            if self.pivotList: # If there are multiple Pivots in the list,
                for p in self.pivotList: # For every pivot in the list,
                    if self.items[0] in mc.getAttr(p+'.ItemsInPivotTool').split(): # If the first item and first Attr in the too are the same,
                        self.items = mc.getAttr(p+'.ItemsInPivotTool').split() # Replace self.item with the first item in the Attr
                        break # stop searching.

            if mc.ls(self.items[0]+"_pivotTool_*"): # If the item already has a Pivot created,
                self.diamondCtrl = mc.ls(self.items[0]+"_pivotDiamond_*")[0] # Apply the diamond control variable,
                self.pivotCtrl = mc.ls(self.items[0]+"_pivotCenter_*")[0] # Apply the pivot control variable,
                self.pivotGroup = mc.ls(self.items[0]+"_pivotTool_*")[0] # Apply the pivot group variable,
                self.basePivotAnchor = mc.ls(self.items[0]+"_pivotAnchor_*")[0] # Apply the Ancor Locator constraint variable,

                self.pivotItems = [self.pivotGroup,self.diamondCtrl,self.pivotCtrl,self.basePivotAnchor] # Create the list of variables.
                
                self.items = mc.getAttr(self.pivotItems[0]+'.ItemsInPivotTool').split() # Collect all the items that are involved with the current pivot.
                mc.select(self.pivotItems[1]) # Select the current Pivot's diamond to manipulate


    def listScenePivots(self):
        '''
        Returns all the pivots in the list.
        '''
        self.pivotList = mc.ls('*_pivotTool_*')
        return self.pivotList

    def makeNewPivotCtrl(self):
        '''
        Creates the following hierarchy:
            New Pivot Group: stores all the Pivot Tool objects, keeps it all at 0,0,0.
                New Diamond Control: use this to control the main object
                    New Pivot Control: use this one to move the pivot around 
                        New Anchor Locator Null: constrains all the items to this object.

        It returns a list with all these items.
        '''
        diamondName = self.items[0]+"_pivotDiamond_#"
        pivotName = self.items[0]+"_pivotCenter_#"
        pivotGroupName = self.items[0]+"_pivotTool_#"
        basePivotAnchorName = self.items[0]+"_pivotAnchor_#"

        # Create the first control, the Diamond. Apply a blue override color.
        self.diamondCtrl = mc.curve(n=diamondName,d=1,p=[ 
                                    (-1, 0, 0),
                                    (0 ,0 ,-1),
                                    (1 ,0 ,0 ),
                                    (0 ,0 ,1 ),
                                    (-1, 0, 0),
                                    (0 ,1 ,0 ),
                                    (1 ,0 ,0 ),
                                    (0 ,-1, 0),
                                    (-1, 0, 0),
                                    (0 ,-1, 0),
                                    (0 ,0 ,1 ),
                                    (0 ,1 ,0 ),
                                    (0 ,0 ,-1),
                                    (0 ,-1, 0)],
                                    k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
        mc.setAttr(self.diamondCtrl + '.overrideEnabled', 1)
        mc.setAttr(self.diamondCtrl + '.overrideColor', 6)

        # Create the second control, the cross. Apply a light blue override color.
        self.pivotCtrl = mc.curve(n=pivotName,d=1,p=[
                                    (-1,0,0),
                                    (1,0,0),
                                    (0,0,0),
                                    (0,0,-1),
                                    (0,0,1),
                                    (0,0,0),
                                    (0,1,0),
                                    (0,-1,0),
                                    (0,0,0),
                                    (-1,0,0),
                                    (1,0,0)],
                                    k=[0,1,2,3,4,5,6,7,8,9,10])
        mc.setAttr(self.pivotCtrl + '.overrideEnabled', 1)
        mc.setAttr(self.pivotCtrl + '.overrideColor', 18)
        # Lock and hide the Rotations of the cross.
        mc.setAttr((self.pivotCtrl+".rx"), lock=True, keyable=False, channelBox=False)
        mc.setAttr((self.pivotCtrl+".ry"), lock=True, keyable=False, channelBox=False)
        mc.setAttr((self.pivotCtrl+".rz"), lock=True, keyable=False, channelBox=False)

        self.pivotGroup = mc.group(name=pivotGroupName,em=1) # Create the null to store all the objects.

        self.basePivotAnchor = mc.group(name=basePivotAnchorName,em=1) # Create the Anchor Locator to constrain the items

        mc.parent(self.basePivotAnchor,self.pivotCtrl) # Parent the constraint null under the pivot.
        mc.parent(self.pivotCtrl,self.diamondCtrl) # Parent the pivot under the diamond.
        mc.parent(self.diamondCtrl,self.pivotGroup) # Parent the diamond under the top null.

        self.pivotItems = [self.pivotGroup,self.diamondCtrl,self.pivotCtrl,self.basePivotAnchor] # Store the variables in a main list.

        return self.pivotItems # Return the list of created objects.

    def snapToFirstItem(self,fromMe=None,toYou=None):
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

    def createPivot(self):
        '''
        INPUT: Creates a set of pivot controls for the selected items.

        OUTPUT: Selects the movable control that allows repositioning of the pivot point.
        '''
        if mc.ls(self.items[0]+"_pivotTool_*"): # If the current item already has a pivot, warn the user and select the diamond.
            print("This item already has a Pivot Control. Delete it first, then make a new one!")
            mc.select(self.pivotItems[1])

        else:
            self.makeNewPivotCtrl() # Create a new Pivot Tool hierarchy
            mc.select(cl=1) # Clear selection before running the snap tool.
            self.snapToFirstItem(self.items[0],self.pivotItems[0]) # Snap the Pivot Group to the first item.

            for item in self.items: # Constrain every item to the Pivot Tool's anchor locator.
                constraint = mc.parentConstraint(self.pivotItems[3],item,mo=1,w=1)

            multDivNode = mc.shadingNode('multiplyDivide', asUtility=True) # Create a multiply/divide node,
            mc.connectAttr((self.pivotItems[2]+'.translate'), (multDivNode+'.input1'),f=1) # connect the Pivot Locator to the MultDiv,
            mc.setAttr(multDivNode+".input2X",-1) # Reverse the values of X.
            mc.setAttr(multDivNode+".input2Y",-1) # Reverse the values of Y.
            mc.setAttr(multDivNode+".input2Z",-1) # Reverse the values of Z.
            mc.connectAttr((multDivNode+'.output'), (self.pivotItems[3]+'.translate'),f=1) # Connect the MultDiv to the Anchor Locator.
            
            # KEY MOMENT, connects the Diamond's rotatePivot to the Pivot Locator.
            mc.connectAttr((self.pivotItems[2]+'.translate'), (self.pivotItems[1]+'.rotatePivot'),f=1)

            mc.addAttr(self.pivotItems[0],ln="ItemsInPivotTool",dt='string') # On the top Pivot Group, add an attribute that'll receive strings.
            mc.setAttr((self.pivotItems[0]+'.ItemsInPivotTool'), e=1,channelBox=True)

            writeIn = ''
            for item in self.items: # Create a string with all the items separated by a space " "...
                writeIn += "{0} ".format(item)
                
            mc.setAttr((self.pivotItems[0]+'.ItemsInPivotTool'),writeIn,type="string") # and store them all in the top group for later use.

            print('Pivot Tool created. Enjoy!')
            mc.select(self.pivotItems[1]) # Selects the diamond. Go play!

    def setKeyOnMainItem(self):
        '''
        Set a key on the items driven by the objects controlled by the current pivot. Sets the "blendParent" values to 1.
        '''
        print("{0} will be key'd".format(self.items))
        mc.setKeyframe(self.items)
        for item in self.items:
            mc.setAttr((item+".blendParent1"), 1)

    def removePivotTool(self):
        '''
        Removes the Pivot Tool without needing to open the Outliner!
        '''
        mc.delete(self.pivotItems)
        print('Tool as been removed!')

