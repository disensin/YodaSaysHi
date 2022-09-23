# From this link:
# https://forums.autodesk.com/t5/maya-forum/error-cannot-find-procedure-quot-dcf-updateviewportlist-quot/m-p/10076660/highlight/true#M86786

import maya.cmds as mc
import re

for script_node in mc.ls(type='script'):
    bs = mc.scriptNode(script_node, q=True, beforeScript=True)
    if 'DCF_updateViewportList' in bs:
        bs = bs.replace(r'DCF_updateViewportList;', '')
        mc.scriptNode(script_node, e=True, beforeScript=bs)
        mc.scriptNode(script_node, executeBefore=True)

