'''
The tool will automatically look for all Selection Sets called `*:export_anim`

Before running the tool, check that the frame-range in the shot is correct.

To run this script, place this script in your Scripts folder,
then run the following Python:

import fbx_asset_export as fae;
fae.export_assets_now(selection_sets=None,
                      check_duplicates = True,
                      test_range=False,
                      prefix=None,
                      force_set_flag= False)

'''

from maya import cmds as mc
from pymel import all as pm
from pprint import pprint
import json
import os
TOOL_VERSION = '1.6.4'

FBX_EXPORT_JSON = 'fbx_export_log'
CSV_EXPORT_LOG_NAME = 'fbx_export_csv_log'
CAMERA_SET_NAME = 'camera:export_anim'
CAMERA_NAME_LIST = ['*_RenderCam','*_TransferCamera']


SORT_LIST = ['this_name',
             'source_file_path',
             'shot_number',
             'sel_set',
             'min_time',
             'max_time',
             'json_prefix',
             'file_path',
             'file_name',
             'tool_version',
             'custom_upAxis',
             'custom_moveToOrigin',
             'custom_modelFileMode',
             'custom_fileSplitType',
             'custom_exportTypeIndex',
             'custom_exportSetIndex',
             'custom_animClips__exportAnimClip',
             'custom_animClips__animClipSrcNode',
             'custom_animClips__animClipId',
             'base_node_parent',
             'base_node']

def debug_get_shot_folder(*args,**kwargs):
    pm.warning('Start Debug...')
    error_message = "No path detected. Open a Shot file saved in the Box Drive Project."
    this_path = mc.file(q=1,sceneName=1) or error_message
    print 'Scene Path:',this_path
    
    if this_path == error_message:
        pm.error(error_message)

    split_path = os_split_path(this_path)

    found_index = [f for f in enumerate(split_path) if 'Animation' in f]
    print 'Animation Directory Index:',found_index
    
    if not all(i in split_path for i in ['4_Production','5_Shots','Animation']):
        pm.error('Directory Error! Make sure the Maya file is saved in the correct Box Shot Directory.\n'
                 'Contact Isai Calderon for further help!')
    
    if not found_index:
        pm.error('"Animation" directory not found!')
    
    found_path = os.sep.join(split_path[:found_index[0][0]+2])
    print 'Target Path:',found_path
    
    shot_name = split_path[found_index[0][0]+2]
    print 'Shot Name:',shot_name
    
    found_path,shot_name
    
    ue_parent_folder = os.sep.join(os_split_path(found_path)+['UE Exports'])
    export_folder = os.path.join(ue_parent_folder,shot_name)
    
    print 'UE Export Path:',export_folder
    
    if not os.path.isdir(export_folder):
        pm.error('Export path not found! Check that it is synced from Box:',export_folder)

    pm.warning('...Target Filepath looks good!')
    
    return found_path,shot_name


JSON_DATA_DEFAULTS = {
    'custom_exportSetIndex':3,
    'custom_exportTypeIndex':2,
    'custom_fileSplitType':2,
    'custom_modelFileMode':1,
    'custom_moveToOrigin':False,
    'custom_upAxis':2,
    'custom_animClips__animClipSrcNode':'None',
    'custom_animClips__exportAnimClip':True,
    'custom_animClips__animClipId':0,
    }

###### Functional Code
def os_split_path(this_path):
    return os.path.normpath(this_path).split(os.path.sep)

def get_shot_folder():
    this_path = mc.file(q=1,sceneName=1)
    if not this_path:
        pm.error("A valid Luka Scene was not opened. Open a shot before running this tool!")

    split_path = os_split_path(this_path)

    found_index = [f for f in enumerate(split_path) if 'Animation' in f]
    found_path = os.sep.join(split_path[:found_index[0][0]+2])
    shot_name = split_path[found_index[0][0]+2]
    return found_path,shot_name

def get_ue_shot_folder():
    this_file_path,shot_name = get_shot_folder()

    ue_parent_folder = os.sep.join(os_split_path(this_file_path)+['UE Exports'])
    export_folder = os.path.join(ue_parent_folder,shot_name)
    if not os.path.isdir(export_folder):
        pm.error('Filepath does not exist! Is it synced from BOX?',export_folder)
    return shot_name,export_folder

def get_fbx_export_settings_folder():
    project_directory = mc.workspace(q=1,active=1)
    directory_path = os.path.join(project_directory, '1_Assets', 'Tools','scripts')
    return directory_path

def _get_file(directory_path,file_name, extension='json', make_file=False,all_logs=False):
    found_logs = []
    for this_file in os.listdir(directory_path):
        if this_file.startswith(file_name) and this_file.endswith('.'+extension):
            if not all_logs:
                return os.path.join(directory_path,this_file)
            found_logs += [os.path.join(directory_path,this_file)]
    if make_file:
        file_path = os.path.join(directory_path,file_name+'.'+extension)
        return _write_json(file_path,{})

    if all_logs:
        return found_logs

    pm.error('FBX Export settings not detected.'
            'Check for the file here:\n'+os.path.join(directory_path,file_name+'.'+extension))

def _get_json_file():
    directory_path = get_fbx_export_settings_folder()
    file_name = 'fbx_export_settings'
    json_path = _get_file(directory_path,file_name)
    return json_path

def _write_json(file_path,control_dict):
    with open(file_path,'w') as outfile:
        outfile.write(json.dumps(control_dict, indent=4))
    return file_path

def _read_json(file_path):
    with open(file_path,'r') as open_file:
        json_dict = json.load(open_file)
    return json_dict

def _get_json_log(all_logs=False):
    directory_path = get_fbx_export_settings_folder()
    file_name = FBX_EXPORT_JSON
    json_path = _get_file(directory_path,file_name, make_file=not all_logs, all_logs=all_logs)
    return json_path

def _combine_excess_json_files(*args,**kwargs):
    all_files = _get_json_log(all_logs=True)
    parent_file = [a for a in all_files if a.endswith(FBX_EXPORT_JSON+'.json')][0]
    this_dict = _read_json(parent_file)
    for this_file in all_files:
        if this_file != parent_file:
            this_dict.update(_read_json(this_file))

    _write_json(parent_file,this_dict)
    print(parent_file)
    return parent_file

def _get_csv_log():
    directory_path = get_fbx_export_settings_folder()
    file_name = CSV_EXPORT_LOG_NAME
    csv_path = _get_file(directory_path,file_name, extension='csv', make_file=True)
    return csv_path

def convert_json_to_csv(get_path = False):
    import csv
    
    directory_path = get_fbx_export_settings_folder()
    csv_file_path = os.path.join(directory_path,CSV_EXPORT_LOG_NAME+'.csv')

    json_file = _get_json_log()
    json_dict = _read_json(json_file)

    list_of_dicts = []
    list_of_keys = set()
    for date_time in sorted(json_dict.keys(), reverse=1):
        entry_dict = json_dict[date_time]
        csv_dict = entry_dict.copy()
        csv_dict['timestamp'] = date_time
        list_of_keys.update(set(csv_dict.keys()))
        list_of_dicts += [csv_dict]
        
    list_of_keys = sorted(list_of_keys,reverse=True)
    
    
    with open(csv_file_path,'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list_of_keys)
        writer.writeheader()
        writer.writerows(list_of_dicts)

    if get_path:
        print(csv_file_path)
        return csv_file_path

# def _write_json(file_path,control_dict):
#     with open(file_path,'w') as outfile:
#         outfile.write(json.dumps(control_dict, indent=4))
#     return file_path

# def _read_json(file_path):
#     with open(file_path,'r') as open_file:
#         json_dict = json.load(open_file)
#     return json_dict



# # json_fbxExport_data = _get_json_file()
# directory_path = get_fbx_export_settings_folder()
# file_name = 'fbx_export_settings'
# file_path = os.path.join(directory_path,file_name+'.json')

# _write_json(file_path,{})
# # shot_number,file_path = get_ue_shot_folder()
# _write_json(_get_json_file(),json_fbxExport_data)
# # _read_json(_get_json_file())

def get_json_data():
    return _read_json(_get_json_file())

# fbx_dict = get_json_data()
# fbx_dict.setdefault("json_prefix",'')
# fbx_dict
# _write_json(_get_json_file(),fbx_dict)

def compile_final_path(file_path,this_name,shot_number):
    return os.path.join(file_path,this_name+'_'+shot_number+'.fbx')

def fill_settings_game_exporter(shot_number,file_path,this_name,
                                min_time,max_time,sel_set,
                                custom_animClips__animClipId,
                                custom_animClips__animClipSrcNode,
                                custom_animClips__exportAnimClip,
                                custom_exportSetIndex,
                                custom_exportTypeIndex,
                                custom_fileSplitType,
                                custom_modelFileMode,
                                custom_moveToOrigin,
                                custom_upAxis,
                                json_prefix,
                                *args,**kwargs):
    pm.mel.eval('gameFbxExporter')

    pm.PyUI('gameExporterWindow|gameExporterTabFormLayout|gameExporterTabLayout').setSelectTabIndex(2)
    pm.mel.eval('gameExp_CurrentTabChanged();gameExp_UpdatePrefix;gameExp_PopulatePresetList();'
                'gameExp_CreateExportTypeUIComponents();')
    exporter_node = get_exporter_node()
    
    pm.mel.eval('gameExp_CurrentTabChanged();gameExp_UpdatePrefix;gameExp_PopulatePresetList();'
                'gameExp_CreateExportTypeUIComponents();')
        
    # JSON Attributes
    exporter_node.exportSetIndex.set(custom_exportSetIndex) # 2 == Set to Export Selection
    exporter_node.selectionSetName.set(sel_set.name()) # Use WITH .exportSetIndex == 3
    
    exporter_node.exportTypeIndex.set(custom_exportTypeIndex)
    exporter_node.fileSplitType.set(custom_fileSplitType)
    exporter_node.modelFileMode.set(custom_modelFileMode)
    exporter_node.moveToOrigin.set(custom_moveToOrigin)
    exporter_node.upAxis.set(custom_upAxis) # 2 == Set to Z
    exporter_node.animClips[0].animClipSrcNode.set(custom_animClips__animClipSrcNode)
    exporter_node.animClips[0].exportAnimClip.set(custom_animClips__exportAnimClip)
    exporter_node.animClips[0].animClipId.set(custom_animClips__animClipId)
    clip_num = pm.getAttr(exporter_node.animClips,size=1)
    if clip_num > 1:
        for num in range(1,clip_num):
            exporter_node.animClips[num].exportAnimClip.set(False)
    
    # json_prefix = json_prefix
    # if json_prefix and not json_prefix.endswith('_'): json_prefix += '_'
    
    # Per-asset Attributes
    exporter_node.animClips[0].animClipName.set(shot_number)
    exporter_node.animClips[0].animClipStart.set(min_time)
    exporter_node.animClips[0].animClipEnd.set(max_time)
    pm.mel.eval('gameExp_CreateExportTypeUIComponents()')
    exporter_node.exportFilename.set(json_prefix+this_name)
    exporter_node.exportPath.set(file_path)

    pm.mel.eval('gameExp_CurrentTabChanged();gameExp_UpdatePrefix;gameExp_PopulatePresetList();'
                'gameExp_CreateExportTypeUIComponents();')
    

def run_exporter():
    pm.mel.eval(THIS_MEL_COMMAND) # Create custom DoExport command
    # pm.mel.eval('gameExp_DoExport();') # Original Export Command
    pm.mel.eval('NEW_gameExp_DoExport();') # Modified Export Command
    

def _build_kwargs(jFbxData,
                  sel_set,
                  shot_number,
                  file_path,
                  min_time,
                  max_time,
                  test_range,
                  prefix,
                  camera_pre_roll,
                  camera_post_roll,
                  up_axis=None,
                  world_reparent=True):
    kwargs_dict = jFbxData
    if up_axis:
        kwargs_dict['custom_upAxis'] = up_axis
        
    kwargs_dict['sel_set'] = sel_set
    kwargs_dict['tool_version'] = TOOL_VERSION
    
    base_node_parent,base_node = get_parent_and_world(sel_set)
    kwargs_dict['base_node_parent'] = base_node_parent
    kwargs_dict['base_node'] = base_node
    
    kwargs_dict['reparent_successful'] = world_reparent
    
    this_namespace = sel_set.parentNamespace()
    this_name = this_namespace
    if this_namespace.lower().startswith('rig_'):
        this_name = '_'.join(this_namespace.split('_')[1:])

    # up_axis = 2 # 1 == Y, 2 == Z

    kwargs_dict['shot_number'] = shot_number
    kwargs_dict['file_path'] = file_path
    kwargs_dict['source_file_path'] = mc.file(q=1,sceneName=1)
    

    if test_range:
        max_time = min_time + 10
        this_name += '_TEST'
    
    this_name = prefix+this_name
    
    this_name = this_name.replace(':','__')
    
    kwargs_dict['this_name'] = this_name+'_'
    
    if sel_set == CAMERA_SET_NAME:
        min_time = min_time - camera_pre_roll
        max_time = max_time + camera_post_roll
    
    kwargs_dict['min_time'] = min_time
    kwargs_dict['max_time'] = max_time

    file_name = compile_final_path(file_path,this_name,shot_number)
    kwargs_dict['file_name'] = this_name+'_'+shot_number+'.fbx'

    return kwargs_dict,file_name

def _build_args_list(selection_sets = None,
                     test_range=False,
                     prefix=None, 
                     jFbxData = None, 
                     force_set_flag = False,
                     custom_path = None,
                     frame_range = None,
                     up_axis = None,
                     world_reparent = True,
                     camera_prePost_roll = None):
    
    if force_set_flag and not selection_sets:
        pm.error('A selection set was not given.')
    
    found_sets = selection_sets or get_all_sets()
    
    
    jFbxData = jFbxData or get_json_data() or JSON_DATA_DEFAULTS
    overriding_assets = []
    kwargs_lists = []

    prefix = prefix or jFbxData['json_prefix'] or ''
    if prefix:
        if not prefix.endswith('_'):
            prefix += '_'
        
    min_time = pm.playbackOptions(q=1,minTime=1)
    max_time = pm.playbackOptions(q=1,maxTime=1)
    if frame_range:
        min_time,max_time = frame_range

    camera_pre_roll,camera_post_roll = camera_prePost_roll

    shot_number,file_path = get_ue_shot_folder()
    if custom_path:
        file_path = custom_path
    kwargs_dict = {}
    for sel_set in found_sets:
        kwargs_dict = {}
        kwargs_dict,file_name = _build_kwargs(jFbxData,
                                              sel_set,
                                              shot_number,
                                              file_path,
                                              min_time,
                                              max_time,
                                              test_range,
                                              prefix,
                                              camera_pre_roll,
                                              camera_post_roll,
                                              up_axis,
                                              world_reparent,)
        kwargs_lists.append(kwargs_dict.copy())
        
        if os.path.isfile(file_name):
            overriding_assets += [kwargs_dict['this_name']]
        
    return kwargs_lists,overriding_assets

def export_assets_now(selection_sets=None,
                      check_duplicates = True,
                      test_range=False,
                      prefix=None,
                      force_set_flag= False,
                      custom_path = None,
                      frame_range = None,
                      from_ui=False,
                      print_kwargs_only = False,
                      up_axis = 2,
                      world_reparent=True,
                      camera_prePost_roll = None):
    kwargs_lists,overriding_assets = _build_args_list(selection_sets = selection_sets,
                                                      test_range = test_range,
                                                      prefix = prefix,
                                                      force_set_flag = force_set_flag,
                                                      custom_path = custom_path,
                                                      frame_range = frame_range,
                                                      camera_prePost_roll = camera_prePost_roll,
                                                      up_axis = up_axis,
                                                      world_reparent = world_reparent)
    if print_kwargs_only:
        pprint(sorted(kwargs_lists[0].keys(),reverse=1))
        pprint(kwargs_lists)
        
        return kwargs_lists
    
    dialog_result = None

    pre_min_time = pm.playbackOptions(q=1,minTime=1)
    pre_animMin_time = pm.playbackOptions(q=1,animationStartTime=1)
    
    pre_max_time = pm.playbackOptions(q=1,maxTime=1)
    pre_animMax_time = pm.playbackOptions(q=1,animationEndTime=1)
    
    if overriding_assets and check_duplicates:
        dialog_result = pm.confirmDialog( title='The following files will be overriden',
                                        message='\n'.join(overriding_assets),
                                        button=['Yes','No'], defaultButton='Yes', 
                                        cancelButton='No', dismissString='No' )
    if dialog_result == "No":
        pm.error('User Cancelled.')
    
    for kwargs in kwargs_lists:
        fill_settings_game_exporter(**kwargs)
    
        base_node_parent = kwargs['base_node_parent']
        base_node = kwargs['base_node']
        if isinstance(world_reparent,bool) and world_reparent and base_node_parent != 'world':
            try:
                base_node.setParent(world=True)
            except:
                kwargs['reparent_successful'] = False
        
        run_exporter()

        reparent_state = kwargs['reparent_successful']
        
        if isinstance(reparent_state,bool) and reparent_state and base_node_parent != 'world':
            base_node.setParent(base_node_parent)
        
        write_json_log(kwargs)

    convert_json_to_csv()
    
    pm.warning('DONE! Exported:\n'+'\n'.join([k['sel_set'].name() for k in kwargs_lists]))
    
    pm.playbackOptions(e=1,minTime=pre_min_time)
    pm.playbackOptions(e=1,animationStartTime=pre_animMin_time)

    pm.playbackOptions(e=1,maxTime=pre_max_time)
    pm.playbackOptions(e=1,animationEndTime=pre_animMax_time)

def get_parent_and_world(selection_set):
    if not selection_set.elements():
        pm.error('This set is blank: '+selection_set.name())
    
    found_element = selection_set.elements()[0]

    base_node = found_element
    for parent_node in pm.pickWalk(found_element,direction='up',recurse=1):
        if pm.PyNode(parent_node).isReferenced():
            base_node = pm.PyNode(parent_node)
    
    base_node_parent = base_node.getParent() or 'world'
    return base_node_parent,base_node


def write_json_log(kwargs):
    from datetime import datetime
    export_timestamp = datetime.now()

    json_log_filepath = _get_json_log()
    current_log = _read_json(json_log_filepath)
    nkwargs = kwargs.copy()
    for this_key,this_value in nkwargs.items():
        if 'pymel' in str(type(this_value)):
            nkwargs[this_key] = this_value.name()
            
    current_log.setdefault(str(export_timestamp),nkwargs)
    
    pprint(kwargs)
    
    _write_json(json_log_filepath,current_log)

def get_exporter_node():
    pm.mel.eval('gameFbxExporter')
    return pm.PyNode(pm.mel.eval('$temp=$gGameFbxExporterCurrentNode;'))

def search_for_string(this_string):
    this_path = '/Applications/Autodesk/maya2019/Maya.app/Contents/scripts/others/'
    all_game_files = [f for f in os.listdir(this_path) if f.startswith('game')]
    for game_file in all_game_files:
        with open(os.path.join(this_path,game_file),'r') as this_file:
            for num,this_line in enumerate(this_file.readlines()):
                if this_string in this_line:
                    print game_file,num,this_line

def get_renderCam(select=True,shot_name_filter = True,*args,**kwargs):
    found_cameras = pm.ls(CAMERA_NAME_LIST)

    if shot_name_filter:
        shot_path,shot_name = get_shot_folder()
        found_cameras = [f for f in found_cameras if shot_name in f.name()]

    if select:
        pm.select(found_cameras)
    return found_cameras

def create_camera_set(force_camera_update = False,add_selected = False):
    selected_items = pm.ls(sl=1)
    
    camera_set_name = CAMERA_SET_NAME

    if not pm.objExists(camera_set_name):
        camera_namespace = pm.Namespace('camera',create=1)
        camera_namespace.setCurrent()
        camera_set = pm.sets(name=camera_set_name,empty=True)
        pm.Namespace(':').setCurrent()
        force_camera_update = True

    camera_set = pm.PyNode(camera_set_name)
    if force_camera_update:
        found_export_cameras = get_renderCam(select=False)

        if add_selected:
            found_export_cameras = selected_items
        
        if not found_export_cameras:
            pm.error('No Cameras were selected. Select a Camera and try again.')
        
        if camera_set.members(): camera_set.removeMembers(camera_set.members())

        found_export_camera = found_export_cameras[0]
        if found_export_camera.type() == 'camera':
            found_export_camera = found_export_camera.getTransform()
            
        camera_set.addMembers([found_export_camera])
    
    return camera_set


def get_all_sets(*args,**kwargs):
    return pm.ls("export_anim",recursive=1,typ='objectSet')
    
########################

############ UI Code
class StoredUI:
    def __init__(self,*args,**kwargs):
        self.check_boxes = None
        self.frameRange_layout = None
        self.start_frame_field = None
        self.end_frame_field = None
        self.set_range_button = None
        self.this_path = None
        self.destination_field = None
        self.options_ui = None
        self.check_duplicate_checkbox = None
        self.run_test_checkbox = None
        self.world_reparent_checkbox = None
        self.prefix_textfield = None
        self.diagnostic_button = None
        self.export_button = None
        self.refresh_button = None
        self.sets_list_layout = None
        self.up_axis = 2
        self.up_axis_radio_collection = None
        self.camera_prePost_roll_field = None


    def refresh_sets_list(self,*args,**kwargs):
        found_sets = get_all_sets()
        
        if self.check_boxes:
            pm.deleteUI(self.check_boxes)
        self.check_boxes = []
        with self.sets_list_layout:
            for found_set in found_sets:
                pm.separator(width=5,style='none')
                self.check_boxes.append(pm.checkBox(found_set,
                                                        changeCommand=self.checkbox_toggles))
        self.checkbox_toggles()
        

    def make_ui(self,*args,**kwargs):
        
        def separator_with_text(add_text,
                                style='shelf',
                                height=10,
                                text_location=25,
                                width = 250):
            separator_options = {'height':height,'style':style}
            pm.separator(height=5,style='none')
            with pm.rowLayout(numberOfColumns=3):
                text_location = text_location or 25
                total_width = width - text_location
                pm.separator(width = text_location,**separator_options)
                this_text = pm.text(add_text,font='fixedWidthFont')
                sep_length = len(add_text.zfill(total_width)) - len(add_text)*7
                pm.separator(width=sep_length,**separator_options)
        
        found_sets = get_all_sets()

        try:
            self.this_path = get_ue_shot_folder()[-1]
        except:
            debug_get_shot_folder()
        self.check_boxes = []

        this_title = 'ExportTheseSets'
        if pm.window(this_title,exists=1,q=1):
            pm.deleteUI(this_title)
        
        with pm.window(this_title,title='Export These Sets',width=275):
            with pm.columnLayout(columnAlign='center',columnAttach=['left',2]) as main_column:
                pm.separator(height=15)
                with pm.columnLayout():            
                    pm.text('Luka FBX Exporter!\nv'+TOOL_VERSION, font='fixedWidthFont', align='center', width=275)
                pm.separator(height=15)

                self.refresh_button = pm.button('Refresh',width=275,command=self.refresh_sets_list)

                with pm.frameLayout("Select Sets to Export",width=275):
                    
                    with pm.scrollLayout(backgroundColor=[.6]*3) as self.sets_list_layout:
                        pass
                    
                pm.separator(height=5)
                
                with pm.rowColumnLayout(numberOfColumns=7,width=275) as self.frameRange_layout:
                    pm.separator(width=5,style='none')
                    pm.text("Frame Range: ")
                    self.start_frame_field = pm.textField(width=50, changeCommand=self.set_range)
                    pm.text(" - ")                    
                    self.end_frame_field = pm.textField(width=50, changeCommand=self.set_range)
                    pm.text(" ")
                    self.set_range_button = pm.button('Set Range',
                                                          command = self.set_frame_range,
                                                          annotation='If RED, Frame Range is not set to Full.',
                                                          width=65)
                
                pm.separator(height=5)
                with pm.frameLayout("Destination Folder",width=275,borderVisible=0):
                    with pm.rowColumnLayout(numberOfColumns=3):#,backgroundColor=[0.7]*3):
                        pm.separator(width=5,style='none')
                        self.destination_field = pm.textField('Final Path',
                                                                  text=self.this_path,
                                                                  enable=True,
                                                                  width=200)
                        pm.button('Browse',command=self.set_new_path)
                        pm.separator(width=2,style='none')
                        pm.button('Reset Path',command=self.reset_path,width=100)
                
                pm.separator(height=5)
                with pm.frameLayout("More Options", collapsable=1, borderVisible=0,width=275) as self.options_ui:
                    
                    with pm.rowColumnLayout(numberOfColumns=2,backgroundColor=[0.7]*3):
                        pm.separator(width=5,style='none')
                        
                        with pm.columnLayout():
                            
                            self.check_duplicate_checkbox = pm.checkBox('Check Duplicates',value=True)
                            self.world_reparent_checkbox = pm.checkBox('Parent to World (default is On)',
                                                                     annotation= 'Parent the top-most node of the Export to World during Export,\n'
                                                                     'then return to its original location.\n'
                                                                     'WARNING: This should ONLY be done by request of the UE department!',
                                                                     value=True)
                            self.run_test_checkbox = pm.checkBox('Run Test',
                                                                 annotation= 'Exports 10 frames, adds "_TEST_" string',
                                                                 changeCommand=self.set_frame_range)
                            with pm.rowColumnLayout(numberOfColumns=6):
                                pm.text('Up-Axis:')
                                pm.separator(width=5,style='none')
                                self.up_axis_radio_collection = pm.radioCollection()
                                y_radio_button = pm.radioButton('Y-Up',changeCommand=self.set_world_up,annotation='Default value is "Z-Up')
                                z_radio_button = pm.radioButton('Z-Up',changeCommand=self.set_world_up,annotation='Default value is "Z-Up')
                                pm.separator(width=5,style='none')
                                pm.text('(default is Z-Up)')
                                self.up_axis_radio_collection.setSelect('Z_Up')
                            separator_with_text('Prefix')
                            
                            with pm.rowColumnLayout(numberOfColumns=3):
                                pm.text("Use Prefix: ")
                                self.prefix_textfield = pm.textField('Prefix')
                                pm.text(" _assetName")
                            separator_with_text('Camera')
                            
                            with pm.rowColumnLayout(numberOfColumns=2):
                                pm.text("Pre/Post Camera Roll Frames: ")
                                self.camera_prePost_roll_field = pm.textField(width=50,text=10, changeCommand=self.set_range)
                                # button to create the set
                                self.create_camera_set_button = pm.button('Make Camera Set',
                                                               command = self.make_cam_set,
                                                               annotation = 'Create a Camera Set, add "RenderCam" if it exists')
                                # pm.button('Select RenderCams', command = pm.Callback(get_renderCam), annotation = 'Select all RenderCams in the scene.')
                                # pm.button('Add Selected to Set',
                                # command = pm.Callback(create_camera_set,force_camera_update = True,add_selected = True),
                                # annotation = 'Add selected Camera to the Set.')
                                # Create a popup menu
                                cam_popup = pm.popupMenu()
                                # menu item to select existing "RenderCams"
                                pm.menuItem("Select RenderCams",
                                            parent=cam_popup,
                                            command = pm.Callback(get_renderCam),
                                            annotation='Select all RenderCams in the scene.')
                                pm.menuItem("Add Selected Cam to Set",
                                            parent=cam_popup,
                                            command = pm.Callback(create_camera_set,force_camera_update = True,add_selected = True),
                                            annotation='Override selected Node into the Camera Selection Set.')
                                            
                            separator_with_text('Debugging')

                            with pm.rowColumnLayout(numberOfColumns=3):
                                pm.button('Debug',
                                           command=debug_get_shot_folder,
                                           annotation = '(not mandatory) Print out of Directory Detection.')
                                self.diagnostic_button = pm.button('Print Diagnostics',
                                                                       command=self.print_kwargs_only,
                                                                       annotation = '(not mandatory) Show printout of\n'
                                                                        'the settings that will be used during Export.')
                                write_to_csv_button = pm.button('Write CSV',
                                                               command=pm.Callback(convert_json_to_csv,get_path=True),
                                                               annotation = '(not mandatory) Write out the current exports to CSV')
                                # Create a popup menu
                                csv_popup = pm.popupMenu()
                                # Renaming both the Warp node and its set
                                pm.menuItem('Combine duplicate JSON',parent=csv_popup,
                                            command = _combine_excess_json_files,
                                            annotation='Find and combine excess JSON files.')

                                 
                pm.separator(height=10)

                self.export_button = pm.button('Export Checked',
                                                   command = self.run_export_from_ui,
                                                   width=275)
                pm.separator(height=10)

        self.refresh_sets_list()
        new_height = len(self.check_boxes)*30
        if new_height > 500:
            new_height = 500
        self.sets_list_layout.setHeight(new_height)
        
        self.set_frame_range()
        self.options_ui.setCollapse(True)

    def make_cam_set(self,*args,**kwargs):
        create_camera_set()
        self.refresh_sets_list()
        

    def set_world_up(self,*args,**kwargs):
        self.up_axis = ['Y_Up','Z_Up'].index(self.up_axis_radio_collection.getSelect())+1


    def checkbox_toggles(self,*args,**kwargs):
        current_state = len(self.get_enabled_checkboxes())

        this_annotation = 'Check Sets ON to enable this button.'
        if current_state:
            this_annotation = 'Assets ready to export!'
            
        self.export_button.setEnable(current_state)
        self.export_button.setBackgroundColor([0.3]*3)
        
        layout_detected = False
        for check_box in self.check_boxes:
            asset_name = check_box.name().split('|')[-1]
            if 'layout' in asset_name.lower():
                check_box.setBackgroundColor([0.6,0.6,0])
                check_box.setAnnotation('Layout assets NOT necessary to Export. Double-check with Adrian.')
                if check_box.getValue():
                    layout_detected = True
        
        if layout_detected:
            this_annotation += ' Layout assets detected.'
            self.export_button.setBackgroundColor([0.9,0.9,0])

            
        self.export_button.setAnnotation(this_annotation)
        self.export_button.setEnableBackground( layout_detected)
        
        self.diagnostic_button.setEnable(current_state)


    def set_range(self,*args,**kwargs):
        pm.playbackOptions(e=1,minTime=float(self.start_frame_field.getText()))
        pm.playbackOptions(e=1,maxTime=float(self.end_frame_field.getText()))
        self.set_frame_range()
    

    def set_frame_range(self,*args,**kwargs):
        self.start_frame = pm.playbackOptions(q=1,minTime=1)
        self.end_frame = pm.playbackOptions(q=1,maxTime=1)
        
        self.camera_prePost_roll = float(self.camera_prePost_roll_field.getText())
        
        animStart_time = pm.playbackOptions(q=1,animationStartTime=1)
        animEnd_time = pm.playbackOptions(q=1,animationEndTime=1)

        if self.run_test_checkbox.getValue():
            self.start_frame = animStart_time
            self.end_frame = animStart_time + 10.0
            self.frameRange_layout.setEnable(False)
        else:
            self.frameRange_layout.setEnable(True)
        
        self.start_frame_field.setText(str(self.start_frame))
        self.end_frame_field.setText(str(self.end_frame))
        
        self.camera_prePost_roll_field.setText(str(self.camera_prePost_roll))

        # print 'UI Color',self.options_ui.getBackgroundColor()
        if self.start_frame != animStart_time or self.end_frame != animEnd_time:
            self.set_range_button.noBackground(1) # Disabled Grey
            self.set_range_button.setBackgroundColor([1,0,0]) # Red

            # self.options_ui.setEnableBackground(1)
            # self.options_ui.setBackgroundColor([1,0,0])
        else:
            # print 'time set'
            
            # self.options_ui.setBackgroundColor([0.4]*3)
            # self.options_ui.setEnableBackground(0)
            
            self.set_range_button.setBackgroundColor([0,0,0])
            self.set_range_button.noBackground(0) # Disabled Grey
        

    def reset_path(self,*args,**kwargs):
        self.this_path = get_ue_shot_folder()[-1]
        self.destination_field.setText(self.this_path)    

    def set_new_path(self,*args,**kwargs):
        new_path = browse_custom_path(starting_directory=self.this_path)
        if new_path:
            self.this_path = new_path[0]
            self.destination_field.setText(self.this_path)

    def browse_custom_path(self,starting_directory=None):
        return pm.fileDialog2(fileMode=2,startingDirectory=starting_directory) or False

    def get_enabled_checkboxes(self,*args,**kwargs):
        selected_sets = []
        for check_box in self.check_boxes:
            if check_box.getValue():
                selected_sets.append(pm.PyNode(check_box.name().split('|')[-1]))
        return selected_sets

    def run_export_from_ui(self,print_kwargs = False,*args,**kwargs):
        original_selection = pm.selected()

        selected_sets = self.get_enabled_checkboxes()
        
        custom_path = self.this_path

        
        export_assets_now(selection_sets = selected_sets,
                        check_duplicates = self.check_duplicate_checkbox.getValue(),
                        test_range = self.run_test_checkbox.getValue(),
                        prefix = self.prefix_textfield.getText(),
                        force_set_flag = True,
                        custom_path = custom_path,
                        frame_range = [self.start_frame , self.end_frame],
                        from_ui = True,
                        print_kwargs_only = print_kwargs,
                        up_axis = ['Y_Up','Z_Up'].index(self.up_axis_radio_collection.getSelect())+1,
                        world_reparent = self.world_reparent_checkbox.getValue() or 'Disabled',
                        camera_prePost_roll = [self.camera_prePost_roll , self.camera_prePost_roll]
                        )

        pm.select(original_selection)

    def print_kwargs_only(self,*args,**kwargs):
        
        self.run_export_from_ui(print_kwargs = True)

    
def make_export_ui():
    StoredUI().make_ui()


THIS_MEL_COMMAND ='''
global proc NEW_gameExp_DoExport()
{    
    global string $gGameFbxExporterCurrentNode;
    
    // In order to trigger the changeCommand callback of a textField
    // the text field needs to be out of focus but by clicking on a button
    // the focus it not changed so I'm forcing it here to be sure that
    // the callback is called and my values are all set.
    
    string $gameExporterPresetList = gameExp_GetPrefixedName("gameExporterPresetList"); 
    setFocus $gameExporterPresetList;      
           
    string $dir = `getAttr($gGameFbxExporterCurrentNode + ".exportPath")`;
    string $file = `getAttr($gGameFbxExporterCurrentNode + ".exportFilename")`;
       
    int $exportType = `getAttr($gGameFbxExporterCurrentNode + ".exportTypeIndex")`; 
    int $splitType = `getAttr ($gGameFbxExporterCurrentNode + ".fileSplitType")`;   
    int $singleFileOut = ($splitType == 1) ? true : false;
    int $modelFileMode = 1;
    int $moveToOrigin = 0;

    if ($exportType == 1)
    {
        $modelFileMode = `getAttr ($gGameFbxExporterCurrentNode + ".modelFileMode")`;
        $singleFileOut = ($modelFileMode==1) ? true : false;    
    }
    $moveToOrigin = `getAttr($gGameFbxExporterCurrentNode + ".moveToOrigin")`;

      
    // add extension if not added
    if(fileExtension(basename($file,"")) == "")
    {
        $file = ($file + ".fbx");
    }
    
    string $exportFilePath = ($dir + "/" + $file);
             
    string $presetPath = (gameExp_GetFbxExportPresetDirectory() + "/" + gameExp_GetFbxPresetForExportType());
        
    FBXPushSettings;   
    FBXLoadExportPresetFile -f $presetPath;

    gameExp_SetFbxPropertiesWithAttributes(); 
    
    string $exportSelectionFlag = "";
    string $oldSelection[];
    
    // 1- Export All, 2- Export Selected, 3- Export Selection Set
    int $exportSetIndex = `getAttr($gGameFbxExporterCurrentNode + ".exportSetIndex")`;
    if($exportSetIndex > 1)
    {
        $exportSelectionFlag = "-s"; 
        
        $oldSelection = `ls -selection`;   


    
        if($exportSetIndex == 3)
        {
            string $selectionSetName = `getAttr($gGameFbxExporterCurrentNode + ".selectionSetName")`;
            if(size($selectionSetName))
            {                
                select -replace $selectionSetName;
            }
        }
    }
    
    $exportType = `getAttr($gGameFbxExporterCurrentNode + ".exportTypeIndex")`;    
    if ($exportType == 2 || $exportType == 3)
    {
        print "Exporting Type";
        // Export animations or clips.
        FBXExportSplitAnimationIntoTakes -clear;         
        int $nbAnimClips = `getAttr -size ($gGameFbxExporterCurrentNode + ".animClips")`;
        
        
        if(!gameExp_SetBakeAnimStartEnd())
        {
            return;
        }       
        
        float $originalT[];
        float $originalR[];
        string $roots[];
        if ($moveToOrigin)
        {
            gameExp_GetRoots($roots);
            gameExp_MoveToOrigin($originalT, $originalR, $roots);
        }
        
        string $name[];
        float  $start[], $end[];
        string $fileNameTmp =  `substitute "\.fbx$" $exportFilePath ""`;
        string $fileNameList[] = gameExp_GenerateClipFilenameList($nbAnimClips, $fileNameTmp, $name, $start, $end);
        
        for($i=0; $i < size($fileNameList); $i++ )
        {
            FBXExportSplitAnimationIntoTakes -v $name[$i] $start[$i] $end[$i];  
            
            if($splitType == 2)
            {     
                // Animation Clips Export, Multiple Clip Files               
				if(catch(`gameExp_FBXExport $exportSelectionFlag $fileNameList[$i]`))       
				{
					// An error occured, move back from origin is required then return.
					if ($moveToOrigin)
                    {
                        gameExp_MoveBackFromOrigin($originalT, $originalR, $roots);
                    }
					return;
				}                
                // Keep the last one exported to view in the FBX Review
                $exportFilePath = $fileNameList[$i];
            }
        }
        
        if($splitType == 1)
        {              
            // Animation Clips Export, Multiple Clips to Single File            
			if(catch(`gameExp_FBXExport $exportSelectionFlag $exportFilePath`))
			{
				// An error occured, move back from origin is required then return.
				if ($moveToOrigin)
                {
                    gameExp_MoveBackFromOrigin($originalT, $originalR, $roots);
                }
				return;
			}                                       
        }    

	    if ($moveToOrigin)
        {
            gameExp_MoveBackFromOrigin($originalT, $originalR, $roots);
        }

	}
    
       
    if(size($oldSelection))
    {
        select -replace $oldSelection;
    }
    else
    {
        select -clear;
    }
    
    FBXPopSettings;     
    
}'''


