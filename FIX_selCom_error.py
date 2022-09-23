# Found in:
# https://forums.autodesk.com/t5/maya-forum/error-lt-function-selcom-at-0x7f29c5c04aa0-gt/m-p/9153002/highlight/true#M76996

from maya import cmds
for _editor in cmds.lsUI(editors=True):
    if not cmds.outlinerEditor(_editor, query=True, exists=True):
        continue
    _sel_cmd = cmds.outlinerEditor(_editor, query=True, selectCommand=True)
    if not _sel_cmd or not _sel_cmd.startswith('<function selCom at '):
        continue
    cmds.outlinerEditor(_editor, edit=True, selectCommand='print("")')
