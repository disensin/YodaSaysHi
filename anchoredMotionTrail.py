from pymel import all as pm

TRACKER_NAME = 'trackMe_wontYou'

def _get_camera():
    found_panel = pm.getPanel(withFocus=1)
    this_camera = pm.modelEditor(found_panel,q=1,av=1,cam=1)
    return this_camera

def get_tracked_node():
    if pm.objExists(TRACKER_NAME):
        tracker_node = pm.PyNode(TRACKER_NAME)
        tracker_node.inputMatrix.inputs()[0].select()
        return tracker_node.inputMatrix.inputs()[0]
    return False

def delete_tracker_node():
    if pm.objExists(TRACKER_NAME):
        pm.delete(TRACKER_NAME+'Handle')

def make_tracker_node(items = None):
    items = items or pm.selected()
    this_camera = _get_camera()

    if not items or items[0] == this_camera.getTransform():
        pm.error('Select an object first!')

    item = items[0]
    delete_tracker_node()

    motion_path  = pm.snapshot(item,
                    name=TRACKER_NAME,
                    motionTrail=1,
                    anchorTransform=this_camera.getTransform(),
                    increment=1,
                    startTime = pm.playbackOptions(q=1,min=1),
                    endTime = pm.playbackOptions(q=1,max=1))
    return motion_path


