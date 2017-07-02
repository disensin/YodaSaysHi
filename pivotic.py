'''
To run, place script in your Scripts folder, then use this code:

import pivotic
reload(pivotic)

'''

import maya.cmds as mc

class PivotIC(object):
    
    def __init__(self):
        '''
        Initialize the Class variable. In this case, get the selected objects.
        If the selected object already has a Pivot Tool applied on it, load the variables.
        '''
        if mc.ls(sl=1): # if there's a selection, engage the variables
            self.items = mc.ls(sl=1)
            self.pivotList = mc.ls('*_pivotTool_*') # let's find any pivot tools out there...
            for piv in self.pivotList: # ...and compare the selected object to them all.
                piv = self.pivotList[0]
                newGuy = mc.getAttr(piv+'.ItemsInPivotTool')

                if self.items[0] in newGuy.split(): # if the selected object is in one of the pivots
                    self.items = newGuy.split() # replace list with the original selection order
                    break

            print self.items
            if mc.ls(self.items[0]+"_pivotTool_*"):
                self.diamondCtrl = mc.ls(self.items[0]+"_pivotDiamond_*")[0]
                self.pivotCtrl = mc.ls(self.items[0]+"_pivotCenter_*")[0]
                self.pivotGroup = mc.ls(self.items[0]+"_pivotTool_*")[0]
                self.basePivotRef = mc.ls(self.items[0]+"_pivotRef_*")[0]

                self.pivotList = [self.pivotGroup,self.diamondCtrl,self.pivotCtrl,self.basePivotRef]
                
                self.items = mc.getAttr(self.pivotList[0]+'.ItemsInPivotTool').split()
                print self.pivotList,self.items
                mc.select(self.pivotList[1])
            else:
                pass

        else:
            self.pivotGroup,self.diamondCtrl,self.pivotCtrl,self.basePivotRef='','','',''
            self.pivotList = [self.pivotGroup,self.diamondCtrl,self.pivotCtrl,self.basePivotRef]



    def listScenePivots(self):
        '''
        Returns all the pivots in the list.
        '''
        self.pivotList = mc.ls('*_pivotTool_*')
        return self.pivotList

    def makeNewPivotCtrl(self):
        '''
        Creates the following hierarchy:
            New Pivot Group
                New Diamond Control
                    New Pivot Control
                        New Pivot Group

        It returns a list with all these items.
        '''
        diamondName = self.items[0]+"_pivotDiamond_#"
        pivotName = self.items[0]+"_pivotCenter_#"
        pivotGroupName = self.items[0]+"_pivotTool_#"
        basePivotRefName = self.items[0]+"_pivotRef_#"

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

        # setAttr -lock true -keyable false -channelBox false "pivotCenter_1.rx";
        mc.setAttr((self.pivotCtrl+".rx"), lock=True, keyable=False, channelBox=False)
        # setAttr -lock true -keyable false -channelBox false "pivotCenter_1.ry";
        mc.setAttr((self.pivotCtrl+".ry"), lock=True, keyable=False, channelBox=False)
        # setAttr -lock true -keyable false -channelBox false "pivotCenter_1.rz";
        mc.setAttr((self.pivotCtrl+".rz"), lock=True, keyable=False, channelBox=False)

        self.pivotGroup = mc.group(name=pivotGroupName,em=1)

        self.basePivotRef = mc.group(name=basePivotRefName,em=1)

        mc.parent(self.basePivotRef,self.pivotCtrl)
        mc.parent(self.pivotCtrl,self.diamondCtrl)
        mc.parent(self.diamondCtrl,self.pivotGroup)

        self.pivotList = [self.pivotGroup,self.diamondCtrl,self.pivotCtrl,self.basePivotRef]

        return self.pivotList

    def snapToFirstItem(self,fromMe=None,toYou=None):
        '''
        Snaps the first selected item to the second item.

        The items are then selected in the same order
        '''

        if mc.ls(sl=1):
            fromMe = mc.ls(sl=1)[0]
            toYou = mc.ls(sl=1)[1]
        mc.xform(toYou, ro= (mc.xform(fromMe,ro=1,q=1,ws=1)), ws=1)
        mc.xform(toYou, t= (mc.xform(fromMe,t=1,q=1,ws=1)), ws=1)
        mc.select(fromMe,toYou)

    def createPivot(self):
        '''
        Creates a set of pivot controls for the selected items.

        Selects the movable control that allows positioning.
        '''
        if mc.ls(self.items[0]+"_pivotTool_*"):
            print "This item already has a Pivot Control. Delete it first, then make a new one!"
        else:
            controls = self.makeNewPivotCtrl()
            print controls[0]
            print self.items[0]
            mc.select(cl=1)
            self.snapToFirstItem(self.items[0],controls[0])

            for item in self.items:
                constraint = mc.parentConstraint(controls[3],item,mo=1,w=1)

            multDivNode = mc.shadingNode('multiplyDivide', asUtility=True)
            mc.connectAttr((controls[2]+'.translate'), (multDivNode+'.input1'),f=1)
            mc.setAttr(multDivNode+".input2Y",-1)
            mc.setAttr(multDivNode+".input2X",-1)
            mc.setAttr(multDivNode+".input2Z",-1)
            mc.connectAttr((multDivNode+'.output'), (controls[3]+'.translate'),f=1)
            mc.connectAttr((controls[2]+'.translate'), (controls[1]+'.rotatePivot'),f=1)

            mc.addAttr(self.pivotList[0],ln="ItemsInPivotTool",dt='string')
            mc.setAttr((self.pivotList[0]+'.ItemsInPivotTool'), e=1,channelBox=True)
            writeIn = ''
            for item in self.items:
                writeIn += "{0} ".format(item)
                
            mc.setAttr((self.pivotList[0]+'.ItemsInPivotTool'),writeIn,type="string")

            mc.select(self.pivotList[1])

    def setKeyOnMainItem(self):
        '''
        Set a key on the items driven by the objects controlled by the current pivot.
        '''
        print self.items, "will be key'd"
        mc.setKeyframe(self.items)
        for item in self.items:
            mc.setAttr((item+".blendParent1"), 1)

    def removePivotTool(self):
        mc.delete(self.pivotList)
        print('Tool as been removed!')






