from pymel import all as pm

found_panel = pm.getPanel(withFocus=1)
this_camera = pm.modelEditor(found_panel,q=1,av=1,cam=1)
items = pm.selected()

if not items or item[0] == this_camera.getTransform():
    pm.error('Select an object first!')

item = items[0]
if pm.objExists('trackMe_wontYou'):
    pm.delete('trackMe_wontYouHandle')

motion_path  = pm.snapshot(item,
                name='trackMe_wontYou',
                motionTrail=1,
                anchorTransform=this_camera.getTransform(),
                increment=1,
                startTime = pm.playbackOptions(q=1,min=1),
                endTime = pm.playbackOptions(q=1,max=1))
