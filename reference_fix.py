####### REFERENCE EDIT
from maya import cmds as mc
from pymel import all as pm
# import json
# import os

CONTROL_DICT = {u'RIG_neefa': {u'L_downLipSec01_CTRL': u'group1|null17',
                    u'L_downLipSec02_CTRL': u'group2|null17',
                    u'L_downLipSec03_CTRL': u'group3|null17',
                    u'L_downLipSec04_CTRL': u'group4|null17',
                    u'L_downLipSec05_CTRL': u'group5|null17',
                    u'L_downLipSec06_CTRL': u'group6|null17',
                    u'L_downLipSec07_CTRL': u'group7|null17',
                    u'L_downLipSec08_CTRL': u'group8|null17',
                    u'L_downLipSec09_CTRL': u'group9|null17',
                    u'L_downLipSec10_CTRL': u'group10|null17',
                    u'L_downLipSec11_CTRL': u'group11|null17',
                    u'L_upLipSec01_CTRL': u'group24|null18',
                    u'L_upLipSec02_CTRL': u'group25|null18',
                    u'L_upLipSec03_CTRL': u'group26|null18',
                    u'L_upLipSec04_CTRL': u'group27|null18',
                    u'L_upLipSec05_CTRL': u'group28|null18',
                    u'L_upLipSec06_CTRL': u'group29|null18',
                    u'L_upLipSec07_CTRL': u'group30|null18',
                    u'L_upLipSec08_CTRL': u'group31|null18',
                    u'L_upLipSec09_CTRL': u'group32|null18',
                    u'L_upLipSec10_CTRL': u'group33|null18',
                    u'L_upLipSec11_CTRL': u'group34|null18',
                    u'M_downLipSec_CTRL': u'group12|null17',
                    u'M_upLipSec_CTRL': u'group35|null18',
                    u'R_downLipSec01_CTRL': u'group23|null17',
                    u'R_downLipSec02_CTRL': u'group22|null17',
                    u'R_downLipSec03_CTRL': u'group21|null17',
                    u'R_downLipSec04_CTRL': u'group20|null17',
                    u'R_downLipSec05_CTRL': u'group19|null17',
                    u'R_downLipSec06_CTRL': u'group18|null17',
                    u'R_downLipSec07_CTRL': u'group17|null17',
                    u'R_downLipSec08_CTRL': u'group16|null17',
                    u'R_downLipSec09_CTRL': u'group15|null17',
                    u'R_downLipSec10_CTRL': u'group14|null17',
                    u'R_downLipSec11_CTRL': u'group13|null17',
                    u'R_upLipSec01_CTRL': u'group46|null18',
                    u'R_upLipSec02_CTRL': u'group45|null18',
                    u'R_upLipSec03_CTRL': u'group44|null18',
                    u'R_upLipSec04_CTRL': u'group43|null18',
                    u'R_upLipSec05_CTRL': u'group42|null18',
                    u'R_upLipSec06_CTRL': u'group41|null18',
                    u'R_upLipSec07_CTRL': u'group40|null18',
                    u'R_upLipSec08_CTRL': u'group39|null18',
                    u'R_upLipSec09_CTRL': u'group38|null18',
                    u'R_upLipSec10_CTRL': u'group37|null18',
                    u'R_upLipSec11_CTRL': u'group36|null18'},
                u'RIG_theo': {u'L_browMid_CTRL': u'null14|L_brow_CTRL',
                              u'R_browMId_CTRL': u'null13|R_brow_CTRL'}}

# def _get_file(file_path,file_name):
#     for this_file in os.listdir(file_path):
#         if this_file.startswith(file_name) and this_file.endswith('.json'):
#             return os.path.join(file_path,this_file)
#     return False

# def get_json_file():
#     project_directory = mc.workspace(q=1,active=1)
#     file_path = os.path.join(project_directory, '1_Assets', 'Tools')
#     file_name = 'rig_rename_fix'
#     json_path = _get_file(file_path,file_name)
#     return json_path

# def _write_json(file_path,control_dict):
#     with open(file_path,'w') as outfile:
#         outfile.write(json.dumps(control_dict, indent=4))

# def _read_json(file_path):
#     with open(file_path,'r') as open_file:
#         json_dict = json.load(open_file)
#     return json_dict


def update_rig_names():
    items = []
    for namespace in pm.namespaceInfo(listOnlyNamespaces=1):
        child_nodes = pm.Namespace(namespace).listNodes()
        
        for child in child_nodes:
            if child.endswith('_ctl'):
                items += [child]
                break
            
    edited_references = set()
    for item in items:
        new_namespace = item.split(':')[0]+':'
        reference_node = mc.referenceQuery(str(item),referenceNode=1)
        all_nodes = mc.referenceQuery(reference_node,nodes=1,showDagPath=1)
        control_dict = CONTROL_DICT
        edited_references.update(_edit_referenceEdits(new_namespace,control_dict))
    update_reference_nodes(edited_references)
    
    
def _edit_referenceEdits(new_namespace,change_dict):
    edited_references = set()
    swap_namespace = lambda x:pm.NameParser(x).swapNamespace(new_namespace)

    for rig_name,control_dict in change_dict.items():

        if new_namespace.startswith(rig_name):

            for control,old_control in control_dict.items():
                if not new_namespace.endswith(':'):
                    new_namespace = new_namespace + ':'

                old_control = str(swap_namespace(old_control))
                namespace_control = str(swap_namespace(control))
                if mc.objExists(namespace_control):
                    reference_node = mc.referenceQuery(namespace_control,referenceNode=1)
                    pm.referenceEdit(reference_node,changeEditTarget=[old_control,namespace_control])
                    old_control
                    edited_references.add(reference_node)
                    # print 'Changed: ',control
    return edited_references

def update_reference_nodes(edited_references):
    for ref_node in edited_references:
        mc.referenceEdit(ref_node,applyFailedEdits=1)
        mc.warning('Updated:',ref_node)

update_rig_names()

# ####### COLLECT NEEFA'S FACE CTRLs
# # mc.select('*'+old_control)
# # old_control.split('RIG_neefa_ANIM:Neefa|')[-1]
# # mc.ls(sl=1,l=1)[0].split('RIG_neefa_ANIM:Neefa|')[-1]
# control_dict = _read_json(json_path)
# # control_dict = {}
# old_rig_namespace = 'RIG_neefa_AnimReady:'
# NEW_rig_namespace = 'RIG_neefa_AnimReady8:'
# items = mc.ls([old_rig_namespace+'lowerLip_fol*',old_rig_namespace+'upperLip_fol*'],typ='transform')
# for i in items:
#     for ii in mc.listRelatives(i,children=1):
#         if ':group' in ii:
#             new_group = ii.replace(old_rig_namespace,NEW_rig_namespace)
#             if mc.objExists(new_group):
#                 new_child = str(pm.PyNode(mc.listRelatives(new_group,children=1,path=1)[0]).stripNamespace())
#                 child = str(pm.PyNode(mc.listRelatives(ii,children=1,path=1)[0]).stripNamespace())
#                 # control_dict.update({str(new_child.stripNamespace()):str(pm.PyNode(child).stripNamespace())})
#                 # control_dict.setdefault(character_name,{}).setdefault(new_child,child)
#                 new_dict.setdefault(character_name,{}).setdefault(new_child,child)

# _edit_referenceEdits(old_rig_namespace,new_dict)
# #######

# new_namespace,change_dict = old_rig_namespace,new_dict
# new_dict = {}
# for key,value in control_dict.items():
#     # if pm.objExists(value):
#         character_name = '_'.join(key.split(':')[0].split('_')[:2])
#         # new_dict.setdefault(character_name,{}).setdefault(key.split(':')[-1],str(pm.PyNode(value).stripNamespace()))
#         new_dict.setdefault(character_name,{}).setdefault(key,value)
# new_dict.pop('RIG_neefa')

# for node in mc.ls([old_rig_namespace+'lowerLip_fol*',old_rig_namespace+'upperLip_fol*'],typ='transform'):
#     new_node = node.replace(old_rig_namespace,NEW_rig_namespace)
#     if pm.objExists(new_node):
#         for child in mc.listRelatives(node,allDescendents=1,typ='transform'):
#             if child.endswith('null17') or child.endswith('null18'):
#                 # break
#                 for new_child in mc.listRelatives(new_node,allDescendents=1,typ='transform'):
#                     if new_child.endswith('_CTRL'):
#                         found_child = new_child
#                         control_dict.update({new_child:child.replace(old_rig_namespace,NEW_rig_namespace)})
# _write_json(get_json_file(),control_dict)

####### COLLECT THEO'S BROW CTRLs
# control_dict = _read_json(get_json_file())
# old_rig_namespace = 'RIG_theo_AnimReady:'
# NEW_rig_namespace = 'RIG_theo_AnimReadyWIP:'
# swap_namespace = lambda x:pm.PyNode(pm.NameParser(x).swapNamespace(NEW_rig_namespace))
# new_dict = {}
# items = mc.ls(old_rig_namespace+'*_brow_CTRL')
# for old_control in items:
#     parent_node = pm.listRelatives(old_control,parent=1)[0]
#     new_parent_node = swap_namespace(parent_node.stripNamespace())
#     new_control = new_parent_node.getChildren()[0]
#     if new_control.getShape() and new_control.getShape().nodeType() == 'nurbsCurve':
#         character_name = '_'.join(NEW_rig_namespace.split(':')[0].split('_')[:2])
        
#         new_child = str(new_control.stripNamespace())
#         if 'browmid' in new_child.lower():
#             child = str(pm.PyNode(old_control).stripNamespace())
#             new_dict.setdefault(character_name,{}).setdefault(new_child,child)

# # control_dict.pop('RIG_theo')
# # control_dict.update(new_dict)
# _write_json(get_json_file(),control_dict)
# _edit_referenceEdits(old_rig_namespace,new_dict)
#######

