from maya import cmds as mc
import sys
# This script will set the Scripts path in the Project into
# Maya's working direcry.
all_rules = mc.workspace(q=1,fileRule=1)
scripts_path = all_rules[all_rules.index('scripts')+1]
add_this_path = os.path.join(projectDirectory, scripts_path)
if add_this_path not in sys.path:
    sys.path.append(add_this_path)

