from pymel import all as pm
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

def get_if_connected(warp_curve,animCurve_nodes):
    '''
    Get boolean list of all connections.
    '''
    disconnect_bools = set()
    for anim_node in animCurve_nodes:
        if warp_curve != anim_node:
            disconnect_bools.add(warp_curve in pm.PyNode(anim_node).inputs())
    return disconnect_bools

def toggle_warp_connection(warp_curve,animCurve_nodes,toggle=True,disconnect_attrs=True):  
    '''
    Toggle Connection based on whether ANY item is (not) connected
    '''
    disconnect_attrs = True
    animCurve_nodes = animCurve_nodes or []
    if toggle:
        disconnect_attrs = any(get_if_connected(warp_curve,animCurve_nodes))
    
    if not disconnect_attrs:
        connect_warp_nodes(warp_curve,animCurve_nodes,disconnect_attrs=True)   
    connect_warp_nodes(warp_curve,animCurve_nodes,disconnect_attrs=disconnect_attrs)
    return disconnect_attrs

def get_animCurve_nodes(items,get_items=False):
    '''
    Tool to collect all AnimCurves for the incoming items, including Curves in AnimLayers.
    '''
    all_animCurve_nodes = []
    found_items = set()
    for item in items:
        all_history = pm.listHistory(item,leaf=False)
        history_animCurves = pm.ls(all_history,typ='animCurve')
        for anim_node in history_animCurves:
            all_animCurve_nodes += [anim_node]
            found_items.add(item)
    if get_items:
        return found_items
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

def add_to_set(warp_set):
    '''
    Add selected items to the warp set IF they're not type animCurveTT.
    '''
    items = pm.selected()
    for item in items:
        if not item.type() == 'animCurveTT':
            warp_set.add(item)
            
        else:
            if item == get_warp_node(warp_set):
                pm.error('TimeWarp node {} cannot be parent of itself.'.format(item))
                
            elif not check_warpNode_set_parentage(item,warp_set):
                warp_set.add(item)
            
            else:
                pm.error('TimeWarp node {} cannot be parent of a child TimeWarp {}.'.format(item,get_warp_node(warp_set)))

def check_warpNode_set_parentage(warp_node,this_set):
    item_set = get_warp_set(warp_node,create=False)
    parent_warp = get_warp_node(this_set)
    return pm.sets(item_set,isMember=parent_warp)

def remove_from_set(warp_curve,warp_set):
    '''
    Disconect items from Warp curve.
    Remove selected items from the given set
    '''
    items = pm.selected()
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

class TimeWarp(object):
    '''
    Make the main UI for the TimeWarp tool
    '''
    def __init__(self):
        self.win_name = 'TimeWarp_Tool'
        self.main_window = None
        self.warp_prefix = WARP_PREFIX
        self.warp_holder_layout = None
        self.refresh_button = None
        self.temp_holder_layout = None
        self.entry_rows = []
    
    def make_ui(self):
        if pm.window(self.win_name,q=1,exists=1):
            # Delete the UI if it exists.
            pm.deleteUI(self.win_name)
        
        with pm.window(self.win_name, title='TimeWarp Tool!') as self.main_window:
            # store the main Holding Layout
            self.warp_holder_layout = pm.columnLayout()
            with self.warp_holder_layout:
                # with pm.columnLayout():
                with pm.rowLayout(numberOfColumns=2):
                    # Creation "NEW" button
                    pm.button('Create New Warp',
                              command = self.add_warp_ui,
                              annotation='Create a new TimeWarp node with current selection.')
                    # Refresh all buttons
                    self.refresh_button = pm.button('Refresh',command=self.reload_ui,
                                    annotation='Refresh the UI')
                
                # Load all existing TimeWarp nodes
                self.reload_ui()

    def make_rows(self,*args,**kwargs):
        # Search through Maya for "timeWarp" animCurves, and make each item
        for warp_curve in pm.ls(self.warp_prefix + '*',typ='animCurve'):
            new_entry = TimeWarpEntry(warp_curve)
            new_entry.create_row()
            self.entry_rows.append(new_entry)

    def reload_ui(self,*args,**kwargs):
        '''
        Reload the entire interface
        '''
        self.entry_rows = [] # Empty out the existing list
        if self.temp_holder_layout:
            # Delete the Temp Holder Layout, make a new one.
            self.temp_holder_layout.delete()
        with self.warp_holder_layout:
            with pm.columnLayout('temporary_warp_holder') as self.temp_holder_layout:
                self.make_rows()

        set_selected_layout_colors(self)
        add_duplicateSelect_finder_button(self)
        
    
    def add_warp_ui(self,*args,**kwargs):
        '''
        Add new item to the UI
        '''
        new_name = get_new_name()
        if new_name:
            selected_items = pm.selected()
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
    def __init__(self,warp_curve):
        # super(TimeWarpEntry,self).__init__()
        self.warp_curve = warp_curve
        self.warp_layout = None
        self.warp_set = get_warp_set(self.warp_curve)
        self.items = self.warp_set.elements()
        self.animCurve_nodes = []
        self.toggle_button = None
        self.current_status = None
        self.this_text = None
        self.controls_button = None
        self.add_button = None
        self.subtract_button = None
    
    def create_row(self):
        '''
        Make the UI
        '''
        with pm.rowColumnLayout(self.warp_curve.name()+'_RCLayout',
                                numberOfColumns=6) as self.warp_layout:
            button_color = [0.355]*3
            # Name the Row the same as the Curve
            self.this_text = pm.text(self.warp_curve.name(),align='left',width=100,
                                     annotation='Right Click for options!')
            # Create a popup menu
            this_popup = pm.popupMenu()
            # Renaming both the Warp node and its set
            pm.menuItem('Rename Warp + Set',parent=this_popup,
                        command = self.rename_warp,
                        annotation='Rename both the Warp node and the Selection Set')
                        # command = pm.Callback(rename_warp,self.warp_curve))
            # Delete the Warp ONLY, leave the Set alone
            pm.menuItem('Delet Warp',parent=this_popup,
                        command = self.delete_warp,
                        annotation='Delete the Warp Node. The Selection Set will NOT be deleted.')
            # Select the TimeWarp node
            selection_message = '\nShift+Click to add this group to current Selection.\
                                \nCtrl+Click to remove this group from current Selection'
            pm.button('TimeWarp',command = self.select_warp,annotation='Select TimeWarp Node'+selection_message,
                      enableBackground=True,backgroundColor=button_color)
            # Select the Controls
            # self.warp_set = get_warp_set(self.warp_curve)
            self.controls_button = pm.button('Controls',
                                             command = self.select_set,
                                             annotation='Select Connected Nodes.'+selection_message,
                                             enableBackground=True,backgroundColor=button_color)
            # Enable/disable the TimeWarp for this Set
            self.toggle_button = pm.button('(Set is empty)',command = self.toggle_warp,
                                           annotation='Toggle this TimeWarp!',
                                           enableBackground=True,backgroundColor=button_color)
            self.toggle_button.setWidth(82)
            self.get_onOff()
            # Add selected Node to Set
            self.add_button = pm.button('plus_sel',label='+ Sel',command = self.add_selection,
                                      annotation='Add Selected items to this timeWarp',
                                      enableBackground=True,backgroundColor=button_color)
            # Remove the Node from this Set
            self.subtract_button = pm.button('minus_sel',label='- Sel',command = self.remove_selection,
                                              annotation='Remove Selected items to this timeWarp',
                                              enableBackground=True,backgroundColor=button_color)
    
    
    def rename_warp(self,*args,**kwargs):
        '''
        Rename the Warp Node, Sets, Layout, Text, all of it to the new name.
        '''
        new_name = get_new_name(default_text = self.warp_curve.name().split('_')[-1])
        if new_name:
            old_name = self.warp_curve.name()
            self.warp_curve = self.warp_curve.rename(WARP_PREFIX + '_'+new_name)
            self.warp_set = self.warp_set.rename(self.warp_curve.name()+'_set')
            self.warp_layout = pm.PyUI(self.warp_layout.rename(self.warp_curve.name()+'_RCLayout'))
            self.this_text = pm.PyUI(self.this_text.rename(self.warp_curve.name()))
            self.this_text.setLabel(self.warp_curve.name())
    
    def delete_warp(self,*args,**kwargs):
        '''
        Delete the current warp node.
        '''
        self.items = self.warp_set.elements()
        self.animCurve_nodes = get_animCurve_nodes(self.items)
        connect_warp_nodes(self.warp_curve,self.animCurve_nodes,disconnect_attrs=True)
        pm.evalDeferred(self.warp_layout.delete)
        pm.delete(self.warp_curve)
    
    def select_warp(self,*args,**kwargs):
        '''
        Select the Warp Node
        '''
        self.select_this(selecting_items=self.warp_curve)
    
    def select_this(self,selecting_items,*args,**kwargs):
        found_modifier = pm.getModifiers()
        if found_modifier == 1:
            pm.select(selecting_items,add=1)
        elif found_modifier == 4:
            pm.select(selecting_items,deselect=1)
        else:
            pm.select(selecting_items,replace=1)
        
        # if (found_modifier & 1) > 0: print ' Shift'
        # if (found_modifier & 4) > 0: print ' Ctrl'
        # if (found_modifier & 8) > 0: print ' Alt'
        # if (found_modifier & 16): print ' Command/Windows'
        
    def select_set(self,*args,**kwargs):
        '''
        Select all the Nodes in the Set
        '''
        self.select_this(selecting_items=self.warp_set)
        
    def toggle_warp(self,*args,**kwargs):
        '''
        Toggle the Connection from Warp Node to Set Items.
        '''
        self.items = self.warp_set.elements()
        self.animCurve_nodes = get_animCurve_nodes(self.items)
        
        if self.animCurve_nodes:
            disconnect_attrs = any(get_if_connected(self.warp_curve,self.animCurve_nodes))
            
            self.current_status = not toggle_warp_connection(self.warp_curve,self.animCurve_nodes)
            self.set_status()
        else:
            self.set_status(set_blank=True)
    
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
        self.set_status()
        self.set_active_color(True)
        # self.set_status_true()
        # self.get_onOff()
    
    def remove_selection(self,*args,**kwargs):
        '''
        Remove the selection from the Set AND disconnect it from the Warp Curve.
        '''
        remove_from_set(self.warp_curve,self.warp_set)
        self.set_active_color(False)
        self.get_onOff()
        
    
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
            self.current_status = all(get_if_connected(self.warp_curve,found_animCurve_nodes))
            self.set_status()
    
    def set_status(self,set_blank=False):
        if set_blank:
            self.set_status_blank()
        
        elif self.current_status:
            self.set_status_true()
        
        else:
            self.set_status_false()
    
    
    def set_status_blank(self):
        pm.warning("Set {} has no animated objects! "\
        "Animate items to start Warpin'!".format(self.warp_set))
        self.toggle_button.setLabel('Not Animated')
        self.toggle_button.setBackgroundColor([1,1,1])
    
    def set_status_true(self):
        self.toggle_button.setLabel('Connected')
        self.toggle_button.setBackgroundColor([0,1,0])
    
    def set_status_false(self):
        self.toggle_button.setLabel('Disconnected')
        self.toggle_button.setBackgroundColor([1,0,0])
    
    
    def set_active_color(self,set_value,*args,**kwargs):
        if set_value:
            self.warp_layout.setBackgroundColor([0,0.4,0])
        else:
            self.warp_layout.setEnableBackground(0)
    
    def set_plusSel_active(self,set_value,*args,**kwargs):
        self.add_button.setEnable(set_value)
    
    # def select_similar(self):
    #     found_items = []
    #     for item in self.items:
    #         row_counter = 0
    #         for this_row in self.entry_rows:
    #             if get_active_row(this_row,item):
    #                 row_counter += 1
    #         if row_counter > 1:
    #             found_items += [item]
                
    #     pm.select(found_items)
    #     set_selected_layout_colors(self)
        

    

def get_active_row(this_row,item):
    '''
    Get row to match scene selection.
    '''
    if pm.sets(this_row.warp_set,isMember=item) or this_row.warp_curve == item:
        return this_row
    return False

def get_all_active_rows(warp_ui,items=None):
    items = items or pm.selected()
    found_rows = {this_row:set() for this_row in warp_ui.entry_rows}
    for item in items:
        for this_row in found_rows:
            this_status = len(found_rows[this_row]) 
            active_row = get_active_row(this_row,item)
            if active_row:
                found_rows[active_row].add(True)
    return found_rows

def set_selected_layout_colors(warp_ui):
    '''
    With given UI, get the scene selection and change the UI color to reflect the currently selected
    timeWarp.
    '''
    found_rows = get_all_active_rows(warp_ui)

    for this_row in warp_ui.entry_rows:
        this_status = len(found_rows[this_row])
        this_row.set_active_color(any(found_rows[this_row]))

def select_similar(warp_ui,main_row):
    found_items = []
    for item in main_row.items:
        row_counter = 0
        for this_row in warp_ui.entry_rows:
            if get_active_row(this_row,item):
                row_counter += 1
        if row_counter > 1:
            found_items += [item]
            
    pm.select(found_items)
    set_selected_layout_colors(warp_ui)


def add_duplicateSelect_finder_button(warp_ui):
    '''
    Add a Popup to the Controls button, it'll select all duplicate Entries in the given TimeWarp
    '''
    for main_row in warp_ui.entry_rows:
        this_popup = pm.popupMenu(parent=main_row.controls_button)
        # Renaming both the Warp node and its set
        pm.menuItem('Select Duplicate Items',parent=this_popup,
                    command = pm.Callback(select_similar,warp_ui,main_row),
                    annotation='If items exist in another Set, this button will select them')


def run_it():
    warp_ui = TimeWarp()
    warp_ui.make_ui()
    # Make a scriptJob to reflect which timeWarp has the current selection.
    this_jid = pm.scriptJob(event=('SelectionChanged',
                            pm.Callback(set_selected_layout_colors,warp_ui)),
                            killWithScene=1)
    # ScriptJob to delete the above SJ in case the UI is closed. Don't want duplicates, right?
    pm.scriptJob(runOnce=True,
                 killWithScene=1,
                 uiDeleted=(warp_ui.main_window,
                            pm.Callback(pm.scriptJob,kill=this_jid)))
    set_selected_layout_colors(warp_ui)
    add_duplicateSelect_finder_button(warp_ui)



