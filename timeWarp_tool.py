from pymel import all as pm
WARP_PREFIX = 'timeWarp'


def toggle_warp_connection(warp_curve,toggle=True):
    items = get_warp_set(warp_curve).elements()
    
    disconnect_attrs = True
    
    if toggle:
        for item in items:
            for anim_node in pm.keyframe(item,q=1,name=1):
                disconnect_attrs = warp_curve in pm.PyNode(anim_node).inputs()
                break
            break
    if not disconnect_attrs:
        connect_warp_nodes(warp_curve,items,disconnect_attrs=True)   
    connect_warp_nodes(warp_curve,items,disconnect_attrs=disconnect_attrs)

def connect_warp_nodes(warp_curve,items,disconnect_attrs=False):
    for item in items:
        for anim_node in pm.keyframe(item,q=1,name=1):
            if disconnect_attrs:
                pm.PyNode(anim_node).input.disconnect()
            else:
                warp_curve.output>>pm.PyNode(anim_node).input

def add_to_set(warp_curve):
    warp_set = get_warp_set(warp_curve)
    items = pm.selected()
    for item in items:
        warp_set.add(item)

def remove_from_set(warp_curve):
    warp_set = get_warp_set(warp_curve)    
    items = pm.selected()
    for item in items:
        warp_set.remove(item)


def get_warp_set(warp_curve):
    set_name = warp_curve.name()+'_set'
    if not pm.objExists(set_name):
        # if pm.selected():
        #     return pm.sets(set_name)
        return pm.sets(name=set_name,empty=1)
    return pm.PyNode(set_name)


def warp_row(warp_curve):
    with pm.rowColumnLayout(warp_curve.name()+'_RCLayout',numberOfColumns=6):
        # Name the Row the same as the Curve
        this_text = pm.text(warp_curve.name(),align='left',width=100)
        # Create a popup menu
        this_popup = pm.popupMenu()
        # Renaming both the Warp node and its set
        pm.menuItem('Rename Warp + Set',parent=this_popup,
                    command = pm.Callback(rename_warp,warp_curve))
        # Delete the Warp ONLY, leave the Set alone
        pm.menuItem('Delet Warp',parent=this_popup,
                    command = pm.Callback(delete_warp,warp_curve))
        # Select the TimeWarp node
        pm.button('TimeWarp',command=pm.Callback(warp_curve.select))
        # Select the Controls
        pm.button('Controls',command=pm.Callback(get_warp_set(warp_curve).select))
        # Enable/disable the TimeWarp for this Set
        pm.button('Toggle Warp',command=pm.Callback(toggle_warp_connection,warp_curve))
        # Add selected Node to Set
        pm.button('+ Sel',command=pm.Callback(add_to_set,warp_curve))
        # Remove the Node from this Set
        pm.button('- Sel',command=pm.Callback(remove_from_set,warp_curve))

def add_warp_ui(warp_holder_layout):
    new_name = get_new_name()
    if new_name:
        warp_curve = pm.createNode('animCurveTT',name=WARP_PREFIX+'_'+new_name)
        startFrame = pm.playbackOptions(q=1,minTime=1)
        endFrame = pm.playbackOptions(q=1,maxTime=1)

        pm.setKeyframe(warp_curve, time=startFrame, value=startFrame,inTangentType='linear',outTangentType='linear')
        pm.setKeyframe(warp_curve, time=endFrame, value=endFrame,inTangentType='linear',outTangentType='linear')

        with warp_holder_layout:
            warp_row(warp_curve)
    
def get_new_name(default_text = None):
    default_text = default_text or ''
    this = pm.promptDialog(title='Warp Curve Name', 
                    message='Name:',
                    text=default_text,
                    button=['Ok', 'Cancel'],
                    cancelButton='Cancel',
                    defaultButton='Ok',
                    dismissString='')
    if this == 'Ok':
        return pm.promptDialog(q=1,text=1)
    return False
    # return pm.promptBox('Warp Curve', 'Name:', 'Ok', 'Cancel')

def rename_warp(warp_curve):
    new_name = get_new_name(default_text = warp_curve.name().split('_')[-1])
    if new_name:
        old_name = warp_curve.name()
        warp_set = get_warp_set(warp_curve)
        warp_curve.rename(WARP_PREFIX + '_'+new_name)
        warp_set.rename(warp_curve.name()+'_set')
        pm.PyUI(old_name+'_RCLayout').rename(warp_curve.name()+'_RCLayout')
        pm.PyUI(old_name).rename(warp_curve.name())
        pm.PyUI(warp_curve.name()).setLabel(warp_curve.name())

def delete_warp(warp_curve):
    if pm.objExists(warp_curve):
        items = get_warp_set(warp_curve).elements()
        connect_warp_nodes(warp_curve,items,disconnect_attrs=True)
        rcLayout = pm.PyUI(warp_curve.name()+'_RCLayout')
        pm.evalDeferred(rcLayout.delete)
        
        pm.delete(warp_curve)
    
def make_ui():
    # Create the UI
    win_name = 'TimeWarp Tool'
    if pm.window(win_name,q=1,exists=1):
        pm.deleteUI(win_name)
    with pm.window(win_name):
        warp_holder_layout = pm.columnLayout()
        with warp_holder_layout:
            with pm.columnLayout():
                # Creation button
                with pm.rowLayout(numberOfColumns=2):
                    pm.button('Create New Warp',
                              command = pm.Callback(add_warp_ui,
                                                    warp_holder_layout))
                    refresh_button = pm.button('Refresh')
            
            make_rows()
            refresh_button.setCommand(pm.Callback(reload_ui,warp_holder_layout))

def make_rows():
    with pm.columnLayout('temporary_warp_holder'):
        for warp_curve in pm.ls(WARP_PREFIX + '*',typ='animCurve'):
            warp_row(warp_curve)


def reload_ui(warp_holder_layout,):
    pm.PyUI('temporary_warp_holder').delete()
    with warp_holder_layout:
        make_rows()

