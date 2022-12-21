'''
TimeWarp Tool
Author: Isai Calderon III

version 2.0.0

- Now uses Maya's TreeView

This tool creates and manages TimeWarps in the scene. The tool detects all 
timeWarps in the scene that start with the string "timeWarp".
Upon creation, the tool creates the TimeWarp node and a Selection Set.

When Enabled, it connects the TimeWarps to all objects in the selection.

When a timeWarp is deleted, the Selection Set remains in the scene. This is 
so the user can re-use the Set for other things. Sometimes, a timeWarp needs
to be "reset" to default. The easiest way to do this is to delete the timeWarp,
and create a New Warp with the same name. The tool will detect the Selection Set
on creation, and use it for the new TimeWarp.

Selecting a row in the UI will select the TimeWarp in the scene.
Selecting a child of a TimeWarp will reflect which timeWarps the object is parented under.

To add a new object to a TimeWarp, press the + button. To remove it, press the -.

TimeWarps can be nested either by selecting a TimeWarp and pressing the + on another TimeWarp,
or by simply middle-click dragging the 
'''

from pymel import all as pm
import treeview
reload(treeview)
WARP_PREFIX = 'timeWarp'

# Functional Code
def new_time_warp(new_name):
    '''
    Create a new TimeWarp node with the given Name.
    '''
    warp_curve = pm.createNode('animCurveTT',name=WARP_PREFIX+'_'+new_name)
    startFrame = pm.playbackOptions(q=1,minTime=1)
    endFrame = pm.playbackOptions(q=1,maxTime=1)
    # Add keyframes, otherwise it won't work! These must be 1:1 with Time:Value
    pm.setKeyframe(warp_curve,
                   time=startFrame,
                   value=startFrame,inTangentType='linear',
                   outTangentType='linear')
    pm.setKeyframe(warp_curve,
                   time=endFrame,
                   value=endFrame,inTangentType='linear',
                   outTangentType='linear')
    
    return warp_curve

def get_if_connected(warp_curve,animCurve_nodes,check_all=False):
    '''
    Get boolean list of all connections.
    '''
    disconnect_bools = set()
    if animCurve_nodes:
        disconnect_bools = [warp_curve in pm.listHistory(animCurve_nodes,leaf=False)]
        if check_all:
            for anim_node in animCurve_nodes:
                if warp_curve != anim_node:
                    # disconnect_bools.add(warp_curve in pm.listConnections(anim_node,t='animCurveTT'))
                    disconnect_bools.add(warp_curve in pm.PyNode(anim_node).inputs())
            #         print 'tested'
    return disconnect_bools

def toggle_warp_connection(warp_curve,animCurve_nodes,toggle=True,disconnect_attrs=True):  
    '''
    Toggle Connection based on whether ANY item is (not) connected
    '''
    disconnect_attrs = True
    animCurve_nodes = animCurve_nodes or []
    if toggle:
        disconnect_attrs = any(get_if_connected(warp_curve,animCurve_nodes))
        # disconnect_attrs = get_if_connected(warp_curve,animCurve_nodes)
    
    if not disconnect_attrs:
        connect_warp_nodes(warp_curve,animCurve_nodes,disconnect_attrs=True)   
    connect_warp_nodes(warp_curve,animCurve_nodes,disconnect_attrs=disconnect_attrs)
    return disconnect_attrs

def get_animCurve_nodes(items = []):#,get_items=False):
    '''
    Tool to collect all AnimCurves for the incoming items, including Curves in AnimLayers.
    '''
    all_animCurve_nodes = []
    # found_items = set()
    # start_time = pm.timerX()
    if items:
        all_history = pm.listHistory(items,leaf=False)
        all_animCurve_nodes = pm.ls(all_history,typ='animCurve') or []
        
    
    # for item in items:
    #     all_history = pm.listHistory(item,leaf=False)
    #     history_animCurves = pm.ls(all_history,typ='animCurve') or []
    #     # for anim_node in history_animCurves:
    #     #     all_animCurve_nodes += [anim_node]
    #     #     found_items.add(item)
    #     if history_animCurves:
    #         all_animCurve_nodes += history_animCurves
    #         # found_items.add(item)
    
    # print 'time taken:',pm.timerX(startTime=start_time),'length:',len(all_animCurve_nodes)
    # if get_items:
    #     return found_items
    return all_animCurve_nodes

def connect_warp_nodes(warp_curve,animCurve_nodes,disconnect_attrs=False):
    '''
    Force connection onto all Items in the Set
    '''
    for anim_node in animCurve_nodes:
        anim_node_py = pm.PyNode(anim_node)
        if anim_node_py != warp_curve:
            if disconnect_attrs:
                anim_node_py.input.disconnect()
            elif warp_curve not in anim_node_py.inputs():
                warp_curve.output>>anim_node_py.input

def filter_child_warps(warp_set):
    found_child_warps = []
    for item in warp_set.elements():
        if item.type() == 'animCurveTT':
            found_child_warps += [item]
    return found_child_warps

def add_to_set(warp_set,items = None):
    '''
    Add selected items to the warp set IF they're not type animCurveTT.
    '''
    items = items or pm.selected()
    for item in items:
        item = pm.PyNode(item)
        if not item.type() == 'animCurveTT':
            warp_set.add(item)
            
        else:
            if item == get_warp_node(warp_set):
                pm.error('TimeWarp node {} cannot be parent of itself.'.format(item))
                
            elif not check_warpNode_set_parentage(item,warp_set):
                warp_set.add(item)
            
            else:
                pm.error('TimeWarp node {} cannot be parent '
                'of a child TimeWarp {}.'.format(item,get_warp_node(warp_set)))

def check_warpNode_set_parentage(warp_node,this_set):
    item_set = get_warp_set(warp_node,create=False)
    parent_warp = get_warp_node(this_set)
    return pm.sets(item_set,isMember=parent_warp)

def remove_from_set(warp_curve, warp_set, items = None):
    '''
    Disconect items from Warp curve.
    Remove selected items from the given set
    '''
    items = items or pm.selected()
    animCurve_nodes = get_animCurve_nodes(items)
    connect_warp_nodes(warp_curve,animCurve_nodes,disconnect_attrs=True)   

    for item in items:
        if item in warp_set.elements():
            warp_set.remove(item)


def get_warp_set(warp_curve, create=True):
    '''
    Get/Create a set with the same name as the Warp Curve.
    '''
    set_name = warp_curve.name()+'_set'
    if not pm.objExists(set_name):
        if create:
            return pm.sets(name=set_name,empty=1)
        return False
    return pm.PyNode(set_name)

def get_warp_node(warp_set):
    '''
    Get/Create a set with the same name as the Warp Curve.
    '''
    warp_curve_name = warp_set.name()[:-4]
    # set_name = warp_curve.name()+'_set'
    if not pm.objExists(warp_curve_name):
        # if create:
            # return pm.sets(name=set_name,empty=1)
        return False
    return pm.PyNode(warp_curve_name)

# UI Code
def get_new_name(default_text = None):
    '''
    Get new name, confirm it doesn't clash with anything.
    '''
    default_text = default_text or ''
    new_name = False
    ui_message = 'Name:'
    while True:
        this = pm.promptDialog(title='Warp Curve Name', 
                        message=ui_message,
                        text=default_text,
                        button=['Ok', 'Cancel'],
                        cancelButton='Cancel',
                        defaultButton='Ok',
                        dismissString='')
        if this == 'Ok':
            new_name = pm.promptDialog(q=1,text=1)
            if not pm.objExists(WARP_PREFIX+'_'+new_name):
                return new_name
            ui_message = 'Name exists!\nName:'
            default_text = new_name
            new_name = False
        elif this == 'Cancel':
            return False

def use_undoChunk(func):
    
    def wrapped(*args,**kwargs):
        return func(*args,**kwargs)
    with pm.UndoChunk():
        results = wrapped(*args,**kwargs)
    # self.reload_ui()
    return wrapped

class TimeWarp(object):
    '''
    Make the main UI for the TimeWarp tool
    '''
    def __init__(self):
        self.this_tree = None
        self.tree_ui = None
        self.win_name_tree = 'TimeWarp_Tool_Tree'

        self.win_name = 'TimeWarp_Tool'
        self.main_window = None
        self.warp_prefix = WARP_PREFIX
        self.warp_holder_layout = None
        self.refresh_button = None
        self.temp_holder_layout = None
        self.entry_rows = {}
        
        self.popup_menu = None
    
    def make_ui(self):
        if pm.window(self.win_name_tree,q=1,exists=1):
            # Delete the UI if it exists.
            pm.deleteUI(self.win_name_tree)
        
        with pm.window(self.win_name_tree) as self.main_window:
            with pm.formLayout(width=250,height=200) as form_layout:
                with pm.rowLayout(numberOfColumns=3) as button_row_layout:
                    pm.button('New Warp',command = self.add_warp_ui)
                    pm.button('Refresh',command=self.reload_ui)
                self.this_tree = pm.treeView( numberOfButtons = 4)
        
        separation_value = 5

        pm.formLayout(form_layout,e=True,attachForm=(button_row_layout, 'top', separation_value))
        pm.formLayout(form_layout,e=True,attachForm=(button_row_layout, 'right', separation_value))
        pm.formLayout(form_layout,e=True,attachForm=(button_row_layout, 'left', separation_value))

        pm.formLayout(form_layout,e=True,attachForm=(self.this_tree, 'left', separation_value))
        pm.formLayout(form_layout,e=True,attachForm=(self.this_tree, 'right', separation_value))
        pm.formLayout(form_layout,e=True,attachForm=(self.this_tree, 'bottom', separation_value))

        pm.formLayout(form_layout,e=True,attachControl=(self.this_tree,'top',separation_value,button_row_layout))
        self.tree_ui = treeview.TreeTool(self.this_tree)

        self.reload_ui()

        self.tree_ui.set_select_command(self.select_command)
        self.tree_ui.set_doubleClick_command(self.double_click_command)
        self.tree_ui.set_dragAndDrop_command(self.dragAndDrop_command)

        self.this_popup = pm.popupMenu(button=3,parent=self.this_tree)
        self.tree_ui.set_rightPress_command(self.right_click_command)
        
        self.tree_ui.get_button(1).set_press_command(self.select_set)
        self.tree_ui.get_button(2).set_press_command(self.toggle_warp)    
        self.tree_ui.get_button(3).set_press_command(self.add_selection)
        self.tree_ui.get_button(4).set_press_command(self.remove_selection)

        # self.tree_ui.get_button(1).set_tooltip(value = 'Select all warped Items.')
        # self.tree_ui.get_button(2).set_tooltip(value = 'Toggle Warp ON/OFF')
        # self.tree_ui.get_button(3).set_tooltip(value = 'Add selection to this Warp')
        # self.tree_ui.get_button(4).set_tooltip(value = 'Remove selection from this Warp')

        # Create ScriptJobs to run on Selection
        self.make_scriptJobs()
        self.set_selected_layout_colors()
        
    def make_scriptJobs(self):
        # Make a scriptJob to reflect which timeWarp has the current selection.
        this_jid = pm.scriptJob(event=('SelectionChanged',
                                pm.Callback(self.set_selected_layout_colors)),
                                killWithScene=1)
        # ScriptJob to delete the above SJ in case the UI is closed. Don't want duplicates, right?
        pm.scriptJob(runOnce=True,
                     killWithScene=1,
                     uiDeleted=(self.main_window,
                                pm.Callback(pm.scriptJob,kill=this_jid)))


    ### Button Commands
    
    # @use_undoChunk
    def select_command(self,*args,**kwargs):
        current_row = self.entry_rows[args[0]]
        this_row = args[0]
        selected = args[1]
        if selected:        
            current_row.select_warp()
        else:
            current_row.deselect_warp()
        return True

    # @use_undoChunk
    def select_set(self,*args):
        with pm.UndoChunk():
            current_row = self.get_row(args[0])
            current_row.select_set()
            self.set_selected_layout_colors()
        
    # @use_undoChunk
    def toggle_warp(self,*args):
        with pm.UndoChunk():
            current_row = self.get_row(args[0])
            current_row.toggle_warp(*args)
    
    # @use_undoChunk
    def add_selection(self,*args):
        with pm.UndoChunk():
            items = pm.selected()
            current_row = self.get_row(args[0])
            current_row.add_selection(*args)
            self.set_selected_layout_colors()
            pm.select(items)
            self.reload_ui()
        
    # @use_undoChunk
    def remove_selection(self,*args):
        with pm.UndoChunk():
            items = pm.selected()
            current_row = self.get_row(args[0])
            self.entry_rows[args[0]].remove_selection(*args)
            self.set_selected_layout_colors()
            pm.select(items)
            self.reload_ui()
    
    # @use_undoChunk
    def double_click_command(self,*args):
        with pm.UndoChunk():
            current_row = self.get_row(args[0])
            if current_row.rename_warp(*args):
                self.reload_ui()
        
    def dragAndDrop_command(self,*args):
        # with pm.UndoChunk():
        # print 'drag and drop args:'
        # print 'moved items',args[0]
        # print 'old parent',args[1][0]
        # print 'old index',args[2]
        # print 'new parent',args[3]
        # print '',args[4]
        # print '',args[5]
        # print '',args[6]
        items = pm.selected()
        
        for old_parent in args[1]:
            if old_parent:
                self.remove_selection(old_parent)
        new_parent = args[3]
        if new_parent:
            self.entry_rows[args[3]].add_selection()
        pm.select(items)
            
    
    ####### scriptJob scripts
    def right_click_command(self,*args,**kwargs):
        '''
        The right-click menu is generated whenever the menu item is right-clicked.
        '''
        self.this_popup.deleteAllItems()
        if args[0]:
            pm.menuItem('Select Items',parent=self.this_popup,
                        command = pm.Callback(self.select_set, args[0]),
                        annotation='Select the objects in this Warp Set.')
            pm.menuItem('Toggle Warp ON/OFF',parent=self.this_popup,
                        command = pm.Callback(self.toggle_warp, args[0]),
                        annotation='Toggle the Warp on or off.',
                        checkBox=self.entry_rows[args[0]].current_status)
            
            pm.menuItem(divider=1,parent=self.this_popup)

            pm.menuItem('Add selected to Warp',parent=self.this_popup,
                        command = pm.Callback(self.add_selection, args[0]),
                        annotation='Add selected objects to Warp Set.')
            pm.menuItem('Remove selected from Warp',parent=self.this_popup,
                        command = pm.Callback(self.remove_selection, args[0]),
                        annotation='Remove selected objects from Warp Set.')

            pm.menuItem(divider=1,parent=self.this_popup)

            pm.menuItem('Rename Warp',parent=self.this_popup,
                        command = pm.Callback(self.double_click_command, args[0]),
                        annotation='Rename Warp and Warp Set.')
                        
            pm.menuItem(divider=1,parent=self.this_popup,dividerLabel='Extra Options')

            new_menu_item = pm.menuItem('Select Duplicate Items',parent=self.this_popup,
                        command = pm.Callback(self.select_similar,args[0]),
                        annotation='If items exist in another Set, this button will select them')
            pm.menuItem(divider=1,parent=self.this_popup)
            # Delete the Warp ONLY, leave the Set alone
            pm.menuItem('Delete Warp',parent=self.this_popup,
                        command = pm.Callback(self.delete_warp,args[0]),
                        annotation='Delete the Warp Node. The Selection Set will NOT be deleted.')
            return True
    
    # @use_undoChunk
    def delete_warp(self,this_warp,*args,**kwargs):
        self.entry_rows[this_warp].delete_warp()
        self.entry_rows.pop(this_warp)
        self.reload_ui()

    # @use_undoChunk
    def select_similar(self,this_warp,*args,**kwargs):
        found_items = []
        
        this_warp_set = get_warp_set(pm.PyNode(this_warp))
        for item in self.entry_rows.values():
            if item.warp_set != this_warp_set:
                found_items += pm.sets(this_warp_set,intersection=item.warp_set)

        pm.select(found_items)
        self.set_selected_layout_colors()
    
    def print_test(child,*args,**kwargs):
        print child
    
    def get_active_row(self,this_row,items):
        '''
        Get row to match scene selection.
        '''
        return set(pm.sets(this_row.warp_set, isMember=item) for item in items)
    
    def set_selected_layout_colors(self):
        '''
        With given UI, get the scene selection and change the UI color to reflect the currently selected
        timeWarp.
        '''
        found_rows = self.get_all_active_rows()

        for this_row in self.entry_rows.values():
            this_status = len(found_rows[this_row])
            this_row.set_active_color(any(found_rows[this_row]))
        
        self.highlight_rows()
        # self.get_warp_parents()
        
            
    def highlight_rows(self):
        for item in self.entry_rows.keys():
            self.entry_rows[item].row_ui.set_selection(item in pm.selected())
            

    def get_all_active_rows(self,items=None):
        items = items or pm.selected()
        found_rows = {this_row:self.get_active_row(this_row,items) for this_row in self.entry_rows.values()}    
        
        return found_rows


    #########

    

    def get_row(self,warp_curve):
        return self.entry_rows[warp_curve]


    def make_rows(self,*args,**kwargs):
        self.entry_rows = {}
        for warp_curve in pm.ls(self.warp_prefix + '*',typ='animCurve'):
            self.entry_rows[warp_curve.name()] = TimeWarpEntry(self.tree_ui,warp_curve)
            self.entry_rows[warp_curve.name()].create_row(parent = '')
        
        self.set_warp_parents()
        
            
    def set_warp_parents(self):
        
        parentage = []
        
        for this_row in self.entry_rows.values():
            for parent_row_ui in self.entry_rows.values():
                # if this_row != parent_row_ui:
                    if pm.sets(parent_row_ui.warp_set, isMember=this_row.warp_curve):
                        this_row.warp_parent = get_warp_node(parent_row_ui.warp_set)

        for this_row in self.entry_rows.values():
            this_row.row_ui.set_parent(this_row.warp_parent)
        
        for this_row in self.entry_rows.values():
            
            this_row.update_row_data(this_row.warp_curve,update_items=True, update_status = True)
            this_row.button_setup()
    
    # def make_hierarchy(self):
    #     for this_row in self.entry_rows.values():
    #         # str(this_row.warp_curve),str(this_row.warp_parent)
    #         if str(this_row.warp_parent):
    #             if self.tree_ui.object_exists(str(this_row.warp_parent)):
    #                 # create row ui
    #                 pass
    #         else:
    #             # make the row ui
    #             # str(this_row.warp_curve)
    #             self.entry_rows[warp_curve.name()].create_row(parent = '')
    
    # def get_child_items(self,item):
    #     item

        
    def reload_ui(self,*args,**kwargs):
        '''
        Reload the entire interface
        '''
        self.tree_ui.remove_all()
        self.make_rows()
        
    
    def add_warp_ui(self,new_name=None,*args,**kwargs):
        '''
        Add new item to the UI
        '''
        new_name = new_name or get_new_name()

        if new_name:
            selected_items = pm.selected() or []
            # Create a new node, give it the prompted name
            new_warp_curve = new_time_warp(new_name)
            new_warp_set = get_warp_set(new_warp_curve)
            pm.select(selected_items)
            add_to_set(new_warp_set)
            # Reload the whole UI :)
            self.reload_ui(*args,**kwargs)



class TimeWarpEntry(TimeWarp,object):
    '''
    Create an individual UI entry with a given TimeWarp Node.
    '''
    def __init__(self,found_tree,warp_curve):
        # super(TimeWarpEntry,self).__init__()
        self.toggle_button = None
        self.current_status = None
        self.this_text = None
        self.controls_button = None
        self.add_button = None
        self.subtract_button = None
        ######
        self.warp_curve = pm.PyNode(warp_curve)
        self.warp_set = get_warp_set(self.warp_curve)
        self.warp_parent = ''
        self.child_warps = filter_child_warps(self.warp_set)
        
        self.tree_ui = found_tree
        self.row_ui = None
        self.ornament_ui = None
        self.toggle_checkbox = None

        self.toggle_button = None
        self.animCurve_nodes = []
        self.items = self.warp_set.elements()
        self.current_status = None

        self.is_selected = False
    
        
    def create_row(self, parent = '', *args, **kwargs):
        '''
        Make the UI
        '''
        self.row_ui = self.tree_ui.add_row(self.warp_curve.name(), parent = parent)

        # self.button_setup()
        # self.update_row_data(self.warp_curve,update_items=True, update_status = True)


    def button_setup(self):
        self.row_ui.get_button(1).set_icon('Sel')
        self.row_ui.get_button(3).set_icon('+')
        self.row_ui.get_button(4).set_icon('-')
        
        self.row_ui.get_button(1).set_tooltip(value = 'Select all warped Items.')
        self.row_ui.get_button(2).set_tooltip(value = 'Toggle Warp ON/OFF')
        self.row_ui.get_button(3).set_tooltip(value = 'Add selection to this Warp')
        self.row_ui.get_button(4).set_tooltip(value = 'Remove selection from this Warp')

        self.ornament_ui = self.row_ui.get_ornament()
        self.toggle_button = self.row_ui.get_button(2)
        
        
    def update_row_data(self,warp_curve,update_items = False, update_status = False):
        
        self.warp_curve = pm.PyNode(warp_curve)
        self.warp_set = get_warp_set(self.warp_curve)
        self.row_ui = self.tree_ui.get_row(self.warp_curve.name())
        self.ornament_ui = self.row_ui.get_ornament()
        self.toggle_button = self.row_ui.get_button(2)
        self.controls_button = self.row_ui.get_button(2)
        
        if update_items:
            self.items = self.warp_set.elements()
            self.animCurve_nodes = get_animCurve_nodes(self.items)
            self.current_status = None
            self.current_status = any(get_if_connected(self.warp_curve,self.animCurve_nodes))
        
        if update_status:
            if self.animCurve_nodes:
                self.toggle_button.set_icon(['Off','On'][self.current_status])
                self.toggle_button.set_color([[1,0,0],[0,1,0]][self.current_status])
                # self.toggle_checkbox.value(self.current_status)
            
            else:
                self.set_status_blank()
    # ### GET commands
    
    def get_warp_curve(self):
        return pm.PyNode(self.warp_curve)

    def get_warp_set(self):
        return get_warp_set(self.get_warp_curve())
    
    def get_items(self):
        return self.get_warp_set().elements()
    
    def get_child_warps(self):
        return filter_child_warps(self.get_warp_set())
    
    def get_parent_warp(self):
        return self.warp_parent

    # ###
    def add_ornament(self):
        self.found_row = self.tree_ui.get_row(self.warp_curve)
        self.ornament_ui = self.found_row.get_ornament()
        self.ornament_ui
        self.ornament_ui.set_on(True)
    
    def rename_warp(self,*args,**kwargs):
        '''
        Rename the Warp Node, Sets, Layout, Text, all of it to the new name.
        '''
        new_name = get_new_name(default_text = self.warp_curve.name().split('_')[-1])
        if new_name:
            old_name = self.warp_curve.name()

            self.warp_curve = self.warp_curve.rename(WARP_PREFIX + '_'+new_name)
            self.warp_set = self.warp_set.rename(self.warp_curve.name()+'_set')

            return True
        return False
            
    
    def delete_warp(self,*args,**kwargs):
        '''
        Delete the current warp node.
        '''
        self.items = self.warp_set.elements()
        self.animCurve_nodes = get_animCurve_nodes(self.items)
        connect_warp_nodes(self.warp_curve,self.animCurve_nodes,disconnect_attrs=True)
        # pm.evalDeferred(self.warp_layout.delete)
        self.row_ui.delete_row()
        pm.delete(self.warp_curve)
    
    def select_warp(self,*args,**kwargs):
        '''
        Select the Warp Node
        '''
        self.select_this(selecting_items=self.warp_curve)
    
    def deselect_warp(self,*args,**kwargs):
        '''
        Select the Warp Node
        '''
        pm.select(self.warp_curve,deselect=1)
    
    
    def select_this(self,selecting_items,found_modifier=None,*args,**kwargs):
        found_modifier = found_modifier or pm.getModifiers()
        # print 'found_modifier',found_modifier
        if found_modifier == 1:
            pm.select(selecting_items,add=1)
        elif found_modifier == 16:
            pm.select(selecting_items,toggle=1)            
        elif found_modifier == 4:
            pm.select(selecting_items,deselect=1)
        else:
            pm.select(selecting_items,replace=1)
        
    def select_set(self,*args,**kwargs):
        '''
        Select all the Nodes in the Set
        '''
        self.select_this(selecting_items=self.warp_set)
        return True
    

    def update_warp_info(self,*args):
        if args:
            self.update_row_data(args[0])
        
        
    def toggle_warp(self,*args,**kwargs):
        '''
        Toggle the Connection from Warp Node to Set Items.
        '''
        self.update_row_data(args[0],update_items=True)
        
        if self.animCurve_nodes:
            self.current_status = not toggle_warp_connection(self.warp_curve,self.animCurve_nodes)

        else:
            self.set_status(set_blank=True)

        self.update_row_data(args[0],update_items=True, update_status = True)
    
    def add_selection(self,*args,**kwargs):
        '''
        Add selection to the Set
        '''
        add_to_set(self.warp_set)
        self.items = self.warp_set.elements()
        self.animCurve_nodes = get_animCurve_nodes(self.items)

        if not self.current_status:
            connect_warp_nodes(self.warp_curve,self.animCurve_nodes,disconnect_attrs=True)
        connect_warp_nodes(self.warp_curve,self.animCurve_nodes,disconnect_attrs=not self.current_status)
        self.set_active_color(True)
        if args:
            self.update_row_data(args[0],update_items=True, update_status = True)
    
    def remove_selection(self,*args,**kwargs):
        '''
        Remove the selection from the Set AND disconnect it from the Warp Curve.
        '''
        self.update_row_data(*args)
        remove_from_set(self.warp_curve,self.warp_set)
        self.set_active_color(False)
        self.set_status_false()
        self.update_row_data(args[0],update_items=True, update_status = True)
         
    
    def get_onOff(self,*args,**kwargs):
        '''
        Get the state of the Connections, set a color on the Connection button
        to reflect the current status. If ONE item is disconnected, it'll reflect this.
        '''
        self.items = self.warp_set.elements()
        
        found_animCurve_nodes = get_animCurve_nodes(self.items)
        
        if not found_animCurve_nodes:
            self.set_status_blank()

        else:
            self.current_status = all(get_if_connected(self.warp_curve,found_animCurve_nodes,check_all=True))
            self.set_status()
    
    def set_status(self,set_blank=False):
        if set_blank:
            self.set_status_blank()
        
        elif self.current_status:
            self.toggle_button.set_icon('On')
            self.toggle_button.set_color([0,1,0])
        
        else:
            self.toggle_button.set_icon('Off')
            self.toggle_button.set_color([1,0,0])

    
    def set_status_blank(self):
        pm.warning("Set {} has no animated objects! "\
        "Animate items to start Warpin'!".format(self.warp_set))
        self.toggle_button.set_icon('N/A')
        self.toggle_button.set_color([0.2]*3)
    
    def set_status_true(self):
        self.ornament_ui.set_color([0,1,0])
    
    def set_status_false(self):
        self.ornament_ui.set_color([1,0,0])
    
    
    def set_active_color(self,set_value,*args,**kwargs):
        self.update_warp_info(*args)
        if set_value:
            self.ornament_ui.set_on(True)
            self.ornament_ui.set_radius(4)
            self.ornament_ui.set_color([0,0.6,0])
        else:
            self.ornament_ui.set_on(False)

def run_it():
    warp_ui = TimeWarp()
    warp_ui.make_ui()



# run_it()
