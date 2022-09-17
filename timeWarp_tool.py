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

def get_if_connected(warp_curve,items):
    '''
    Get boolean list of all connections.
    '''
    disconnect_bools = []
    for item in items:
        for anim_node in pm.keyframe(item,q=1,name=1):
            disconnect_bools.append(warp_curve in pm.PyNode(anim_node).inputs())
    return disconnect_bools

def toggle_warp_connection(warp_curve,items,toggle=True):  
    '''
    Toggle Connection based on whether ANY item is (not) connected
    '''
    disconnect_attrs = True
    
    if toggle:
        disconnect_attrs = any(get_if_connected(warp_curve,items))
    
    if not disconnect_attrs:
        connect_warp_nodes(warp_curve,items,disconnect_attrs=True)   
    connect_warp_nodes(warp_curve,items,disconnect_attrs=disconnect_attrs)

def connect_warp_nodes(warp_curve,items,disconnect_attrs=False):
    '''
    Force connection onto all Items in the Set
    '''
    for item in items:
        for anim_node in pm.keyframe(item,q=1,name=1):
            if disconnect_attrs:
                pm.PyNode(anim_node).input.disconnect()
            else:
                warp_curve.output>>pm.PyNode(anim_node).input

def add_to_set(warp_set):
    '''
    Add selected items to the warp set IF they're not type animCurveTT.
    '''
    items = pm.selected()
    for item in items:
        if pm.nodeType(item) != 'animCurveTT':
            warp_set.add(item)

def remove_from_set(warp_curve,warp_set):
    '''
    Disconect items from Warp curve.
    Remove selected items from the given set
    '''
    items = pm.selected()
    connect_warp_nodes(warp_curve,items,disconnect_attrs=True)   

    for item in items:
        if item in warp_set.elements():
            warp_set.remove(item)


def get_warp_set(warp_curve):
    '''
    Get/Create a set with the same name as the Warp Curve.
    '''
    set_name = warp_curve.name()+'_set'
    if not pm.objExists(set_name):
        return pm.sets(name=set_name,empty=1)
    return pm.PyNode(set_name)

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
            new_name = False
        elif this == 'Cancel':
            return False

class TimeWarp(object):
    '''
    Make the main UI for the TimeWarp tool
    '''
    def __init__(self):
        self.win_name = 'TimeWarp_Tool'
        self.warp_prefix = WARP_PREFIX
        self.warp_holder_layout = None
        self.refresh_button = None
        self.temp_holder_layout = None
        self.entry_row = []
    
    def make_ui(self):
        if pm.window(self.win_name,q=1,exists=1):
            # Delete the UI if it exists.
            pm.deleteUI(self.win_name)
        
        with pm.window(self.win_name):
            # store the main Holding Layout
            self.warp_holder_layout = pm.columnLayout()
            with self.warp_holder_layout:
                # with pm.columnLayout():
                with pm.rowLayout(numberOfColumns=2):
                    # Creation "NEW" button
                    pm.button('Create New Warp',
                              command = self.add_warp_ui)
                    # Refresh all buttons
                    self.refresh_button = pm.button('Refresh',command=self.reload_ui)
                
                # Load all existing TimeWarp nodes
                self.reload_ui()

    def make_rows(self,*args,**kwargs):
        # Search through Maya for "timeWarp" animCurves, and make each item
        for warp_curve in pm.ls(self.warp_prefix + '*',typ='animCurve'):
            new_entry = TimeWarpEntry(warp_curve)
            new_entry.create_row()
            self.entry_row.append(new_entry)

    def reload_ui(self,*args,**kwargs):
        '''
        Reload the entire interface
        '''
        self.entry_row = [] # Empty out the existing list
        if self.temp_holder_layout:
            # Delete the Temp Holder Layout, make a new one.
            self.temp_holder_layout.delete()
        with self.warp_holder_layout:
            with pm.columnLayout('temporary_warp_holder') as self.temp_holder_layout:
                self.make_rows()
    
    def add_warp_ui(self,*args,**kwargs):
        '''
        Add new item to the UI
        '''
        new_name = get_new_name()
        if new_name:
            # Create a new node, give it the prompted name
            new_time_warp(new_name)
            # Reload the whole UI :)
            self.reload_ui(*args,**kwargs)
               

class TimeWarpEntry:
    '''
    Create an individual UI entry with a given TimeWarp Node.
    '''
    def __init__(self,warp_curve):
        self.warp_curve = warp_curve
        self.warp_layout = None
        self.warp_set = get_warp_set(self.warp_curve)
        self.items = self.warp_set.elements()
        self.toggle_button = None
        self.current_status = None
        self.this_text = None
    
    def create_row(self):
        '''
        Make the UI
        '''
        with pm.rowColumnLayout(self.warp_curve.name()+'_RCLayout',
                                numberOfColumns=6) as self.warp_layout:
            # Name the Row the same as the Curve
            self.this_text = pm.text(self.warp_curve.name(),align='left',width=100)
            # Create a popup menu
            this_popup = pm.popupMenu()
            # Renaming both the Warp node and its set
            pm.menuItem('Rename Warp + Set',parent=this_popup,
                        command = self.rename_warp)
                        # command = pm.Callback(rename_warp,self.warp_curve))
            # Delete the Warp ONLY, leave the Set alone
            pm.menuItem('Delet Warp',parent=this_popup,
                        command = self.delete_warp)
            # Select the TimeWarp node
            pm.button('TimeWarp',command = self.select_warp)
            # Select the Controls
            # self.warp_set = get_warp_set(self.warp_curve)
            pm.button('Controls',command = self.select_set)
            # Enable/disable the TimeWarp for this Set
            self.toggle_button = pm.button('(Set is empty)',command = self.toggle_warp)
            self.toggle_button.setWidth(82)
            self.get_onOff()
            # Add selected Node to Set
            pm.button('+ Sel',command = self.add_selection)
            # Remove the Node from this Set
            pm.button('- Sel',command = self.remove_selection)
    
    
    def rename_warp(self,*args,**kwargs):
        '''
        Rename the Warp Node, Sets, Layout, Text, all of it to the new name.
        '''
        new_name = get_new_name(default_text = self.warp_curve.name().split('_')[-1])
        if new_name:
            old_name = self.warp_curve.name()
            self.warp_curve = self.warp_curve.rename(WARP_PREFIX + '_'+new_name)
            self.warp_set = self.warp_set.rename(self.warp_curve.name()+'_set')
            self.warp_layout = self.warp_layout.rename(self.warp_curve.name()+'_RCLayout')
            self.this_text = pm.PyUI(self.this_text.rename(self.warp_curve.name()))
            self.this_text.setLabel(self.warp_curve.name())
    
    def delete_warp(self,*args,**kwargs):
        '''
        Delete the current warp node.
        '''
        connect_warp_nodes(self.warp_curve,self.warp_set,disconnect_attrs=True)
        pm.evalDeferred(self.warp_layout.delete)
        pm.delete(self.warp_curve)
    
    def select_warp(self,*args,**kwargs):
        '''
        Select the Warp Node
        '''
        self.warp_curve.select()
    
    def select_set(self,*args,**kwargs):
        '''
        Select all the Nodes in the Set
        '''
        self.warp_set.select()
        
    def toggle_warp(self,*args,**kwargs):
        '''
        Toggle the Connection from Warp Node to Set Items.
        '''
        toggle_warp_connection(self.warp_curve,self.items)
        self.get_onOff()
    
    def add_selection(self,*args,**kwargs):
        '''
        Add selection to the Set
        '''
        add_to_set(self.warp_set)
        self.get_onOff(self)
    
    def remove_selection(self,*args,**kwargs):
        '''
        Remove the selection from the Set AND disconnect it from the Warp Curve.
        '''
        remove_from_set(self.warp_curve,self.warp_set)
        self.get_onOff(self)
    
    def get_onOff(self,*args,**kwargs):
        '''
        Get the state of the Connections, set a color on the Connection button
        to reflect the current status. If ONE item is disconnected, it'll reflect this.
        '''
        self.items = self.warp_set.elements()
        if not self.items:
            pm.warning("Set {} has no animated objects! "\
            "Animate items to start Warpin'!".format(self.warp_set))
            self.toggle_button.setLabel('(Set is empty)')
            self.toggle_button.setBackgroundColor([0,0,0])
            self.toggle_button.noBackground(0)

        else:
            self.current_status = any(get_if_connected(self.warp_curve,self.items))
            if self.current_status:
                self.toggle_button.setLabel('Connected')
                self.toggle_button.setBackgroundColor([0,1,0])
            else:
                self.toggle_button.setLabel('Disconnected')
                self.toggle_button.setBackgroundColor([1,0,0])

if __name__ == '__main__':
    warp_ui = TimeWarp()
    warp_ui.make_ui()
