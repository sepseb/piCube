#!/usr/bin/python

from distutils.command.config import config
from time import sleep
from picamera import PiCamera
from datetime import datetime
from adafruit_servokit import ServoKit
from cmd import Cmd
import subprocess
import os
import configparser
import re
import requests
import sys

installed_release = '0.2.0'
response = requests.get("https://api.github.com/repos/sepseb/piCube/releases")
latest_release = response.json()[0]['tag_name']

config = configparser.ConfigParser()
config.read('config.ini')
filter_name_1 = config['servo_config_file']['filter_name_1']
filter_name_2 = config['servo_config_file']['filter_name_2']
filter_name_3 = config['servo_config_file']['filter_name_3']
servo_cmd_1 = config['servo_config_file']['servo_cmd_1']
servo_cmd_2 = config['servo_config_file']['servo_cmd_2']
servo_cmd_3 = config['servo_config_file']['servo_cmd_3']

default_path = '/home/pi/Documents/'

class PiShell(Cmd):

    prompt = 'piCube $ '
    intro = '-----------------------------------------'\
            f'\n piCube Interface Program v{installed_release}'\
            f'\n Type help for a list of commands'\
            f'\n Type exit to leave the program'\

    def do_exit(self,inp):
        # Add code to stop any running tasks with camera
        camera.close()
        return True

    def help_exit(self):
        print(f'Exit the program')

    def do_new_session(self,inp):
        global session_path
        if not inp:
            print("Syntax Error: No session name provided")
            return
        session_path =  default_path + inp + '/'
        try:
            os.mkdir(session_path)
            print(f'Created directory : {session_path}')
        except:
            while True:
                user_input = input ("Session already exists - Continue with old session? (y/n)?")
                if (user_input == 'n'):
                    print(f'Please create a new session with a new name')
                    break
                elif (user_input == 'y'):
                    print(f'Using {session_path} as current session')
                    break
                else:
                    print(f'User input error')
            return

    def help_new_session(self):
        print(f'Syntax : new_session [folder name]')
        print(f'Creates a new folder in Documents')

    def do_auto(self,inp):
        try:
            session_path
        except:
            print(f'Error: No new session was created')
            return
        if not inp:
            now = datetime.now()
            dt_string = now.strftime("%m-%d-%Y_%H-%M-%S")
            # Use Timestamp as image name
            image_path = session_path + 'auto_' + dt_string + '.jpg'
        else:
            # Use input as image name - Future addition
            image_path = session_path + inp + '.jpg'    
        camera.capture(image_path)
        print(f'Image captured to : {image_path}')

    def help_auto(self):
        print(f'Syntax : auto x')
        print(f'Captures one picture with automatic settings')
        print(f'If x is not defined, filename is current data_time.jpg')
        print(f'If x is give a string, filename will be the string.jpg')

    def do_manual(self,inp):
        try:
            session_path
        except:
            print(f'Error: No new session was created')
            return
        # Parse the arguments
        inp += ' '
        iso_value = re.search('--iso (.+?) ', inp)
        ss_value = re.search('--shutter (.+?) ', inp)
        exp_comp_value = re.search('--exp (.+?) ', inp)

        # This section checks for which arguments have been input and if they are valid
        if iso_value is None:
            camera.iso = 0
            print('Warning: No user input for iso - using auto')
        else:
            try:
                camera.iso = int(iso_value.group(1))
            except:
                print(f'Invalid iso value: {int(iso_value.group(1))} (valid range 0..800)  - try a lower number')
                return
        if ss_value is None:
            camera.shutter_speed = 0
            print('Warning: No user input for shutter speed - auto')
        else:
            camera.shutter_speed = int(ss_value.group(1))
        if exp_comp_value is None:
            camera.exposure_compensation = 0
            print('Warning: No user input for exposure compensation - using default value')
        else:
            try:
                camera.exposure_compensation = int(exp_comp_value.group(1))
            except:
                print(f'Invalid exposure compensation value: {int(exp_comp_value.group(1))} (valid range -25..25) -  truncating...')
                camera.exposure_compensation =(max(min(25, int(exp_comp_value.group(1))), -25))
                
        now = datetime.now()
        dt_string = now.strftime("_%M-%S")
        # Use Timestamp as image name
        properties = f'iso-{camera.iso}' + f'_shutter-{camera.shutter_speed}'
        image_path = session_path + properties + dt_string + '.jpg'
        if camera.iso == 0:
            print(f'\nISO : auto')
        else:
            print(f'\nISO : {camera.iso}')
        if camera.shutter_speed == 0:
            print(f'Exposure time : 1/{int(1000000/camera.exposure_speed)} ({camera.exposure_speed}) microseconds')
        else:
            print(f'Shutter speed : 1/{int(1000000/camera.shutter_speed)} ({camera.shutter_speed}) microseconds')
        if camera.exposure_compensation != 0:
            print(f'exposure compensation : {camera.exposure_compensation}')
        camera.capture(image_path)
        print(f'Image captured to : {image_path}\n')

    def help_manual(self):
        print(f'Syntax : manual --iso value --shutter value --exp value')
        print(f'Captures one picture with manual settings')
        print(f'If each of the three arguments is not entered, the camera will automatically adjust')

    def do_set_resolution(self, inp):
        if not inp:
            print("Syntax Error: No resolution provided")
            return
        try:
            arg = tuple(map(int, inp.split()))
            camera.resolution = (arg[0],arg[1])
        except:
            print('Error : incorrect resolution values')
       
    def help_set_resolution(self):
        print(f'Syntax : set_resolution x y')
        print(f'Sets the camera resolution to x by y')
        print(f'Camera Module v1 Max Resolution is (2592x1944)')
        print(f'Camera Module v2 Max Resolution is (32802464)')
        print(f'HQ Camera Max Resolution is (4056x3040)') 

    def do_filter(self, inp):
        if (inp == filter_name_1):
            #kit.servo[0].angle = servo_cmd_1
            print(f'commanding servo to move to {servo_cmd_1}')
        elif (inp == filter_name_2):
            #kit.servo[0].angle = servo_cmd_2
            print(f'commanding servo to move to {servo_cmd_2}')
        elif (inp == filter_name_3):
            #kit.servo[0].angle = servo_cmd_3
            print(f'commanding servo to move to {servo_cmd_3}')
    
    def help_filter(self):
        print(f'Syntax : filter x')
        print(f'Rotate the filter wheel to the selected filter x')
        print(f'Filter names : {filter_name_1}, {filter_name_2}, {filter_name_3}')
    
    def do_transfer(self, inp):
        if not inp:
            print("Syntax Error: No input provided")
            return
        try: 
            inp += ' '
            ip_value = re.search('--ip (.+?) ', inp)
            user_value = re.search('--user (.+?) ', inp)
            scp_cmd = 'scp -r %s %s@%s:/C:/Users/%s/Desktop/' % \
                (session_path, user_value.group(1), ip_value.group(1), user_value.group(1))
            subprocess.run(scp_cmd)
        except:
            print("Oops... Something went wrong")

    def help_transfer(self):
        print(f'transfer --ip <PC ip ad> --user <PC username>')
        print(f'Transfers images to the computer')

def version_check(old_ver, new_ver):

    old_ver_t = tuple(map(int, old_ver.split('.')))
    new_ver_t = tuple(map(int, new_ver.split('.')))
    for i in range(3):
        diff =  new_ver_t[i] - old_ver_t[i]
        if diff == 0:
            continue
        if diff > 0:
            update = ' Released version %s is now available' % (new_ver)
        else:
            update = ' Development version installed'
        return '%s' % (update)
    return ' Latest released version installed'

def detect_camera(picam_version):
     
    if (picam_version == 'ov5647'):
        return ' Detected Camera Module v1'
    elif (picam_version == 'imx219'):
        return ' Detected Camera Module v2'
    elif (picam_version == 'imx477'):
        return ' Detected HQ Camera'
    else:
        return ' Camera Model Unknown or no camera detected'
    
def camera_init(inp):
    if not inp:
        # Initiate camera with default sensor mode
        camera = PiCamera()
    else:
        camera = PiCamera(sensor_mode = int(inp[0]))
        print(f' Camera sensor mode set to : {int(inp[0])}')

    camera.framerate_range = (1, 30)
    cam_model = camera.revision
    print(detect_camera(cam_model))
    camera.resolution = camera.MAX_RESOLUTION
    print(f' Camera resolution set to : {camera.resolution}')
    return camera
    
def servo_init():
    # Set channels to the number of servo channels on your kit.
    # 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
    kit = ServoKit(channels=16)

def parse_argv(argv,type):
    output = []
    for i in range(0,len(argv)): 
        for j in range(0,len(type)):
            if argv[i] == type[j]:
                output.append(argv[i+1])
    return output

if __name__ == '__main__':
    print(f'Starting Application...')
    arg_types = ['--mode','--firmware']
    cmd_args = parse_argv(sys.argv[1:],arg_types)
    camera = camera_init(cmd_args)
    print(version_check(installed_release, latest_release[1:]))
    #servo_init()
    PiShell().cmdloop()