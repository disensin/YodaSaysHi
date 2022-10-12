from pymel import all as pm

TRACKER_NAME = 'trackMe_wontYou'

def _get_camera():
    found_panel = pm.getPanel(withFocus=1)
    this_camera = pm.modelEditor(found_panel,q=1,av=1,cam=1)
    return this_camera

def get_tracked_node(select=False):
    if pm.objExists(TRACKER_NAME):
        tracker_node = pm.PyNode(TRACKER_NAME)
        tracker_node.inputMatrix.inputs()[0].select()
        if select:
            pm.select(tracker_node.inputMatrix.inputs()[0])
        return tracker_node.inputMatrix.inputs()[0]
    return False

def get_tracker_node(delete=False, select=False):
    if pm.objExists(TRACKER_NAME):
        trail_shape = pm.PyNode(TRACKER_NAME).outputs()[0].getShape()
        if delete:
            found_attrs = {}
            for attr in trail_shape.listAttr():
                try:
                    attr.set(attr.get())
                    found_attrs[attr.longName()] = attr.get()
                except:
                    pass
            pm.delete(trail_shape.getTransform())
            return found_attrs
        if select:
            trail_shape.getTransform().select()
        return False
    

def make_tracker_node(items = None, use_camera_anchor = True):
    items = items or pm.selected()
    this_camera = _get_camera()

    if not items or items[0] == this_camera.getTransform():
        pm.error('Select an object first!')

    item = items[0]
    found_attrs = get_tracker_node(delete=True) or {}

    this_anchor = None
    if use_camera_anchor:
        this_anchor = this_camera.getTransform()

    motion_path = pm.snapshot(item,
                    name=TRACKER_NAME,
                    motionTrail=1,
                    anchorTransform=this_anchor,
                    increment=1,
                    startTime = pm.playbackOptions(q=1,min=1),
                    endTime = pm.playbackOptions(q=1,max=1))
    handle_shape = motion_path[0].getShape()
    for attr,new_value in found_attrs.items():
        if hasattr(handle_shape,attr):
            try:
                handle_shape.attr(attr).set(new_value)
            except:
                pass
    pm.select(item)
    return motion_path
