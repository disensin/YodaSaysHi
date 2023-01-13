"""
Created by: Isai Calderon
October 25, 2019
Version 1.0.0

function wacom_ratio() {
 python /folder/containg/python/file/wacom_set_ratio.py "$@";
}


"""
import os
import sys
import subprocess

# Collect Terminal Arguments
arguments = sys.argv

if '-h' in arguments or '--help' in arguments:
    print("Description:")
    " This tool will change the Aspect Ratio of your current Wacom Tablet to match the screen's layout!"
    " Once run, if you draw a circle on the tablet, it'll draw a circle on the screen."
    " "
    " Options:"
    '  -h,  --help       This info.'
    '  -reset            Reset the area to Default.'
    '  -debug            0 : No output'
    '                    1 : New ratio'
    '                    2 : Will return the exact code running'
    '                        to set the desired Ratio, will NOT run the code.'
    sys.exit()

if '-debug' in arguments and '-reset' in arguments:
    print( "ERROR: '-debug' and '-reset' must be used independently.")
    sys.exit()

def get_from_shell(run_string):
    """
    With a given Linux Terminal command, return the output.
    """
    dimension_output = subprocess.Popen(run_string,
           shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    delivered_values = dimension_output.communicate()[0]
    return delivered_values

def get_ratio_from_string(length,height):
    """
    Using the given integer strings, return their ratio.
    """
    return float(length)/float(height)

def get_screens_ratio():
    """
    Return the combined ratio of all attached Displays.
    """
    screen_ratio_list = get_from_shell("xdpyinfo | grep 'dimensions:'").split()[1].split('x')
    # print screen_ratio_list
    return get_ratio_from_string(screen_ratio_list[0],screen_ratio_list[1])

def get_wacom_device():
    """
    Retreive the attached Wacom Stylus, Eraser, and Touch device names
    """
    wacom_output = get_from_shell("xsetwacom --list")
    returning_these = []
    for w in wacom_output.split('\n'):
        if 'stylus' in w:
            returning_these += [w.split('stylus')[0]+'stylus']
        if 'eraser' in w:
            returning_these += [w.split('eraser')[0]+'eraser']
        if 'touch' in w:
            returning_these += [w.split('touch')[0]+'touch']
    return returning_these

def set_wacom_ratio(debug=False,reset=False):
    """
    This will provide the user with a 1:1 Wacom-to-screen motion.
    Checks the screen's ratio, and apply it to the current Wacom device.

    If the ratio of the screen layout is greater than that
        of the Tablet, it'll adjust the height of the tablet.
    If the ratio of the screen layout is smaller than that
        of the Tablet, it'll adjust the length of the tablet.
    :param debug:
            0 will run the script with zero output;
            1 will run the script with some output;
            2 will not run the script and will output Debugging information.
    """
    screen_ratio = get_screens_ratio()
    run_code = ''
    changed_ratio = None
    all_reset_code = None
    for p in get_wacom_device():
        ###################### ATTEMPTED MATHLESS SOLUTION USING MapToOutput
        # total_screen_dimensions = get_from_shell("xdpyinfo | grep 'dimensions:'").split()[1]+"+0+0"
        # run_code = ''
        # for p in get_wacom_device():
        #     if 'touch' in p:
        #         run_code = 'xsetwacom set "{0}" Touch off;\n'.format(p) + run_code
        #     if 'eraser' in p or 'stylus' in p:
        #         os.system('xsetwacom set "{0}" ResetArea'.format(p))
        #         run_code = 'xsetwacom set "{0}" maptooutput {1};\n'.format(p,total_screen_dimensions) + run_code
        ######################### USING MATH TO GET FINAL VALUES
        if 'touch' in p:
            run_code = 'xsetwacom set "{0}" Touch off;\n'.format(p) + run_code
        if 'eraser' in p or 'stylus' in p:
            reset_code = 'xsetwacom set "{0}" ResetArea'.format(p)
            if debug < 2:
                os.system(reset_code)
            if reset:
                # all_reset_code = reset_code + ";\n" + all_reset_code
                continue
            wacom_dimensions = get_from_shell('xsetwacom get "{0}" Area'.format(p)).split()
            wac_length = int(wacom_dimensions[2]) - int(wacom_dimensions[0])
            wac_height = int(wacom_dimensions[3]) - int(wacom_dimensions[1])
            current_tablet_ratio = get_ratio_from_string(wac_length,wac_height)
            # print 'wac_length',int(wacom_dimensions[3]),int(wac_length/screen_ratio)

            final_wac_height = wac_height
            final_wac_length = wac_length
            # If the ratio of the tablet (1.6) is greater than the screens (3.5555):
            if current_tablet_ratio < screen_ratio:
            #     height = length / screen ratio
                final_wac_height = int(wac_length/screen_ratio)
                changed_ratio = 'Height'
                # if debug >= 1:
                #     print 'Changing Height by {0} / {1} = {2}'.format(wac_length,screen_ratio,final_wac_height)
            # elif the ratio of the tablet (1.6) is smaller than the screens (1.5625):
            elif current_tablet_ratio > screen_ratio:
            #     length = height * ratio   
                final_wac_length = int(wac_height * screen_ratio)
                changed_ratio = 'Length'
                # if debug >= 1:
                #     print 'Changing Length by {0} x {1} = {2}'.format(wac_height,screen_ratio,final_wac_length)

            run_code = 'xsetwacom set "{0}" Area {1} {2} {3} {4};\n'.format(p,
                wacom_dimensions[0],
                wacom_dimensions[1],
                int(wacom_dimensions[0]) + final_wac_length,
                int(wacom_dimensions[1]) + final_wac_height,
                ) + run_code
            # else:
            #     run_code = 
    if debug >= 2:
        print ("SCREEN RATIO:::")
        print( get_screens_ratio())
        print( "WACOM DEVICES:::")
        print( get_wacom_device())
        print( "CODE TO RUN:::")
        print( run_code)
        return
    if debug >= 1 and not reset:
        print( "Wacom {0} Ratio: Changed to {1}".format(changed_ratio,screen_ratio))
    # os.system(run_code)
    get_from_shell(run_code)
# If there are Arguments
# print arguments

for num,arg in enumerate(arguments):
    if arg == '-debug':
        try: current_value = int(arguments[num+1])
        except: current_value = 1
        
        set_wacom_ratio(debug=current_value) # No output.
        sys.exit()
    if arg == '-reset':
        try:
            current_value = int(arguments[num+1])
        except:
            set_wacom_ratio(debug=0,reset=1)
        print( 'Wacom Ratio: Reset!')
        sys.exit()



set_wacom_ratio(debug=0,reset=0) # No output.

# print 'attempting',arguments[-1]
# set_wacom_ratio(debug=0) # No output.
# set_wacom_ratio(debug=1) # Script will run, some output.
# set_wacom_ratio(debug=2) # Script will not run, just output information.
