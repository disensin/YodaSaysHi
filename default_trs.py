from pymel import all as pm

def set_default_trs(option_str=None,query=False):
  '''
  For the selected objects, use this tool to set their default Transform Tool.
  When set, use the hotkey "T" to show an individual manipulator for each object.
  
  :option_str str:
    Valid values are: 'None', 'Translate', 'Rotate', 'Scale', and 'Transform'.
  :query bool:
    If True, it'll return a list of valid String values.
  '''
    trs_options = {
                'None': 0,
                'Translate': 1,
                'Rotate': 2,
                'Scale': 3,
                'Transform': 4,
                    }
    if query:
        print("Available Options:\n",trs_options.keys())
        return trs_options.keys()
    items = pm.selected()
    for i in items:
        i.showManipDefault.set(trs_options[option_str])
    pm.warning('Default Transform set to:',option_str)



# set_default_trs('None')
# set_default_trs('Translate')
# set_default_trs('Rotate')
# set_default_trs('Scale')
# set_default_trs('Transform')
# set_default_trs(query=1)
