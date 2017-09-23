'''
window = Rename it!
	column = Main Column
		column

Instructions:
To run, use this code:

import siRenamer as sr;reload(sr);sr.Renamer().renamerTool()

'''

import maya.mel as mel
import maya.cmds as mc

class Renamer(object):

	def __init__(self):
		'''
		Load UI Name Variable. Changing the name here will propegate it across the whole script.
		'''
		self.RnmWin = 'RenameMe'

	def deleteRenamerUI(self):
		'''
		If UI exists, Delete UI
		'''
		if (mc.window(self.RnmWin, exists=True)):
			mc.deleteUI(self.RnmWin, window = True)


	def getSelectedItems(self):
		'''
		Create a list of editable input fields for each selected item
		'''
		# Make the window a columnLayout and adjustable
		rightColumn = mc.rowColumnLayout('rightColumn', adj = 1,numberOfColumns=2)

		# Query your selection
		sel = mc.ls(sl=1)

		for each in range(len(sel)):

			mc.text(label = each,parent=rightColumn)
			mc.nameField( object = sel[each],parent = rightColumn,width = 200)


	def renamerTool(self):
		'''
		Engage the Renamer tool. It will create a window with a Close button and a scrollable column.
		'''
		
		# Check if the window exists already
		self.deleteRenamerUI()

		# Create the window
		self.RnmWin = mc.window(self.RnmWin,title = 'Rename It!')

		mainColumn = mc.columnLayout('Main Column')

		#//Button on window for closing out our Renaming Tool
		mc.button( label = "CLOSE", command = "sr.Renamer().deleteRenamerUI()",parent = mainColumn)

		# Enable scrolling
		scrollLayout = mc.scrollLayout(
			horizontalScrollBarThickness=16,
			verticalScrollBarThickness=16)

		self.getSelectedItems()

		# Shows our Renaming Window
		mc.showWindow(self.RnmWin)

