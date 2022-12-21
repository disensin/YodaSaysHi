from pymel import all as pm

# Main UI class
class TreeTool(object):
    def __init__(self,this_tree):
        self.this_tree = this_tree
        self.button_count = 3
        self.buttons_right = False
        self.backgroundColor = None
        self.highlightColor = None
        self.selectionColor = None
        self.children = self.get_children()
        # self.set_select_command('fart')
    
    # Set button count
    def set_button_count(self,count):
        pm.treeView(self.this_tree, e=1, numberOfButtons = count)
        self.button_count = count
        
    def get_button_count(self):
        get_button_count(self.this_tree)
    
    # Set button side (left or right)
    def set_buttons_right_side(self,side):
        pm.treeView(self.this_tree, e=1, attachButtonRight = side)
        self.buttons_right = side
    
    # Change all colors
    def set_color_background(self,color):
        pm.treeView(self.this_tree, e=1, backgroundColor = color)
        self.backgroundColor = color
    
    def set_color_highlight(self,color):
        pm.treeView(self.this_tree, e=1, highlightColor = color)
        self.highlightColor = color
    
    # Add a row
    def add_row(self,new_name,parent=''):
        # pm.treeView( self.this_tree, e=True, addItem = (new_name, parent))
        new_row = TreeRow(self.this_tree,new_name,self.button_count)
        new_row.create_row()
        self.children = []
        for child in pm.treeView(self.this_tree, q=1, children = True):
            self.children += [TreeRow(self.this_tree,child,self.button_count)]
        return new_row
    
    def get_row(self,name):
        if self.object_exists(name):
        # if pm.treeView( self.this_tree, q=True, itemExists = name):
            return TreeRow(self.this_tree,name,self.button_count)
        return False
    
    def object_exists(self,name):
        # print 'searching for ',name,pm.treeView( self.this_tree, q=True, itemExists = name)
        return pm.treeView( self.this_tree, q=True, itemExists = name)
    
    def get_children(self,this_parent=''):
        # Get all children
        self.all_children = []        
        for c in pm.treeView(self.this_tree,q=1,children=this_parent) or []:
            if this_parent != c:
                self.all_children += [get_row(self,c)]
                # self.all_children += [BranchTool(self.this_tree,c)]
        return self.all_children
    
    def get_button(self, button_num):
        return RowButton(self.this_tree,button_num)
    
    # Remove a row
    def remove_row(self,remove_name):
        found_row = self.get_row(remove_name)
        found_row.delete_row()
        # pm.treeView( self.this_tree, e=True, removeItem = remove_name)
    
    def remove_all(self):
        pm.treeView(self.this_tree, e=1, removeAll = True)
        
    def set_select_command(self,value,*args,**kwargs):
        # print 'here'
        return pm.treeView(self.this_tree, e=1, selectCommand = value)
        # pm.treeView(self.this_tree, e=1, selectCommand = self.test_command)
        # return True
    
    def set_doubleClick_command(self,value,*args,**kwargs):
        return pm.treeView(self.this_tree, e=1, itemDblClickCommand = value)
    
    def set_rightPress_command(self,value = None):
        # contextMenuCommand
        pm.treeView(self.this_tree, e=1, contextMenuCommand = value)
        # pm.treeView(self.this_tree, e=1, rightPressCommand = [self.button_num,value])
        self.contextMenu_command = value
        # print(self.button_tooltip)
        return True
    
    
    def set_dragAndDrop_command(self,value = None):
        # dragAndDropCommand
        pm.treeView(self.this_tree, e=1, dragAndDropCommand = value)
        self.dragAndDrop_command = value
        return True
    
    def get_selected(self):
        found_selected = []
        for warp in pm.treeView(self.this_tree, q=1, selectItem = True) or []:
            found_selected += [TreeRow(self.this_tree,warp,self.button_count)]
            
        # print found_selected
        return found_selected
        
    
    def test_command(self,*args,**kwargs):
        print 'now'
    
    def clear_selection(self):
        pm.treeView(self.this_tree, e=1, clearSelection = True)



def get_button_count(tree_layout):
    button_count = -1
    start_time = pm.timerX()
    while True:
        button_count += 1
        try:
            pm.treeView(tree_layout, e=1, buttonVisible=['fart',button_count,1])
            # pm.treeView(self.this_tree, q=1, numberOfButtons = button_count)
        except:
            return button_count-1
        if pm.timerX()-start_time > 5:
            break
    

# Single Entry class
class TreeRow(object):
    def __init__(self,
                 this_tree,
                 row_name,
                 number_of_buttons,
                 row_parent = '',):
        self.this_tree = this_tree
        self.row_name = row_name
        self.row_parent = row_parent
        self.button_count = 0
        self.ornament = self.get_ornament()
        self.selection_color = [0.5,0.5,0.5]
        
        # __name__ = self.row_name
    
    def __str__(self):
        return self.row_name
    
    # Create row
    def create_row(self):
        if not pm.treeView( self.this_tree, q=True, itemExists = self.row_name):
            pm.treeView( self.this_tree, e=True, addItem = (self.row_name, self.row_parent))
            # print 'added ',self.row_name
            # pm.treeView( self.this_tree, e=True, selectionColor = [self.row_name]+self.selection_color)
            
    def set_highlite(self,value):
        pm.treeView( self.this_tree, e=True, highlite = [self.row_name,value])
        
    def set_selection(self,value):
        # print 'setting',value
        pm.treeView( self.this_tree, e=True, selectItem= [self.row_name,value])
        
    # def rename_row_command(self,new_name):
    #     new_name
    
    # Delete row
    def delete_row(self):
        pm.treeView( self.this_tree, e=True, removeItem = self.row_name)
    
    # Reparent rows
    def set_parent(self,new_parent,index = 0):
        created_items = []
        for child in pm.treeView(self.this_tree,q=1,children=self.row_name):
            old_index = pm.treeView(self.this_tree,q=1,itemIndex=child)
            parent = pm.treeView(self.this_tree,q=1,itemParent=child) or False
            if child == self.row_name:
                parent = new_parent
                old_index = index
            created_items.append([child,parent,old_index])
        
        self.delete_row()
        pm.treeView(self.this_tree,e=1,insertItem=created_items)
        
        self.row_parent = parent
    
    # Get row parent
    def get_parent(self):
        self.row_parent = pm.treeView(self.this_tree, q=1, itemParent = self.row_name)
        return self.row_parent
    
    def get_buttons(self):
        self.button_count = button_count(self.this_tree)
        
        found_buttons = []
        for num in range(self.button_count):
            found_buttons += [self.get_button(num+1)]
        return found_buttons
    
    def get_button(self, button_num):
        return RowButton(self.this_tree,button_num,self.row_name)
    
    def get_ornament(self):
        self.ornament = TreeOrnament(self.this_tree,self.row_name)
        return self.ornament
        
    
# Button class
class RowButton(object):
    def __init__(self,this_tree,button_num,row_name=None):
        self.this_tree = this_tree
        self.row_name = row_name
        self.button_num = button_num
        self.button_state = 0
        self.button_style = 0
        self.button_icon = ''
        self.button_tooltip = ''
    
    def __str__(self):
        return '_'.join([self.this_tree,self.row_name,str(self.button_num)])
    
    # Change button status
    def set_state(self,value = 0, query = False):
        options = ['buttonUp', 'buttonDown', 'buttonThirdState']
        if query: 
            return options

        this_value = options[value]
        pm.treeView(self.this_tree, e=1, buttonState = [self.row_name,self.button_num,this_value])
        self.button_state = [value,this_value]
    
    # Change button style (# of button presses, 1, 2, or 3)
    def set_style(self,value = 0, query = False):
        options = ['pushButton','2StateButton','3StateButton']
        if query:
            return options
        this_value = options[value]
        pm.treeView(self.this_tree, e=1, buttonStyle = [self.row_name,self.button_num,this_value])
        self.button_icon = [value,this_value]
    
    # Change button icon
    def set_icon(self,value = '', query = False):
        if query:
            return pm.treeView(self.this_tree, q=1, buttonTextIcon = [self.row_name,self.button_num,button_icon])

        pm.treeView(self.this_tree, e=1, buttonTextIcon = [self.row_name,self.button_num,value])
        self.button_icon = value
    
    def set_tooltip(self,value = ''):
        pm.treeView(self.this_tree, e=1, buttonTooltip = [self.row_name,self.button_num,value])
        self.button_tooltip = value
    
    def set_press_command(self,value = None):
        pm.treeView(self.this_tree, e=1, pressCommand = [self.button_num,value])
        self.button_command = value
    
    
    def set_rightPress_command(self,value = None):
        contextMenuCommand
        pm.treeView(self.this_tree, e=1, contextMenuCommand = [self.button_num,value])
        self.button_command = value
        return True
    
    
    def set_color(self,value = []):
        if value:
            pm.treeView(self.this_tree, e=1, buttonTransparencyOverride = [self.row_name,self.button_num,1])
            pm.treeView(self.this_tree, e=1, buttonTransparencyColor = [self.row_name,self.button_num]+value)
        else:
            pm.treeView(self.this_tree, e=1, buttonTransparencyOverride = [self.row_name,self.button_num,0])
            
        self.button_color = value
    
    
        
class TreeOrnament(object):
    def __init__(self,this_tree,row_name):
        self.this_tree = this_tree
        self.row_name = row_name
        self.on = False
        self.dotted = False
        self.radius = 1
        self.currentColor = [0,0,0]
        

    def set_on(self,num1):
        pm.treeView(self.this_tree, e=1, ornament = [self.row_name,num1,self.dotted,self.radius])
        self.on = num1
    
    def set_dotted(self,num2):
        pm.treeView(self.this_tree, e=1, ornament = [self.row_name,self.on,num2,self.radius])
        self.dotted = num2
    
    def set_radius(self,num3):
        pm.treeView(self.this_tree, e=1, ornament = [self.row_name,self.on,self.dotted,num3])
        self.radius = num3
    
    def set_color(self,ornament_color):
        pm.treeView(self.this_tree, e=1, ornamentColor = [self.row_name]+ornament_color)
        self.currentColor = ornament_color
    
