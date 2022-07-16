from distutils.command.config import config
from picamera import PiCamera
from datetime import datetime
from adafruit_servokit import ServoKit
from time import sleep
from cmd import Cmd
import subprocess
import os
import configparser
import re
import requests

installed_release = '0.2.0'
response = requests.get("https://api.github.com/repos/sepseb/piCube/releases")
latest_release = response.json()[0]['tag_name']

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.

config = configparser.ConfigParser()
config.read('config.ini')
filter_name_1 = config['servo_config_file']['filter_name_1']
filter_name_2 = config['servo_config_file']['filter_name_2']
filter_name_3 = config['servo_config_file']['filter_name_3']
servo_cmd_1 = config['servo_config_file']['servo_cmd_1']
servo_cmd_2 = config['servo_config_file']['servo_cmd_2']
servo_cmd_3 = config['servo_config_file']['servo_cmd_3']

servo_installed = 0
if (servo_installed == 1):
    kit = ServoKit(channels=16)

default_path = '/home/pi/Documents/'

class PiShell(Cmd):

    prompt = 'PiCube $ '
    intro = "\n--------------------------------------"\
            "\n PiCube Interface Program v{current_version}"\
            "\n Type help for a list of commands"\
            "\n Type exit to leave the program"\

    def do_exit(self,inp):
        # Add code to stop any running tasks with camera
        return True

    def help_exit(self):
        print(f'Exit the program')

    def do_new_session(self,inp):
        global session_path
        session_path =  default_path + inp + '/'
        if (os.path.isdir(session_path) == False):
            os.mkdir(session_path)
            print(f'Created directory : {session_path}')
        else:
            user_input = input ("Session already exists - Continue with old session? (y/n)?")
            if (user_input == 'n'):
                print(f'Please create a new session with a new name')
            else:
                print(f'Using {session_path} as current session')

    def help_new_session(self):
        print(f'Syntax : new_session [folder name]')
        print(f'Creates a new folder in Documents')

    def do_auto(self,inp):
        global session_path
        if not inp:
            now = datetime.now()
            dt_string = now.strftime("%m-%d-%Y_%H-%M-%S")
            # Use Timestamp as image name
            image_path = session_path + dt_string + '.jpg'
        else:
            # Use input as image name - Future addition
            image_path = session_path + inp + '.jpg'    
        camera.capture(image_path)
        print(f'Image Captured : {image_path}')

    def help_auto(self):
        print(f'Syntax : auto x')
        print(f'Captures one picture ')
        print(f'If x = ts, filename is current data_time.jpg')
        print(f'If x = gps, filename is current lat_lon.jpg')

    def do_manual(self,inp):
        global session_path
        inp += ' '
        iso_value = re.search('--iso (.+?) ', inp)
        ss_value = re.search('--shutter (.+?) ', inp)

        camera.iso = int(iso_value.group(1))
        camera.shutter_speed = int(ss_value.group(1))

        camera.exposure_mode = 'off'
        now = datetime.now()
        dt_string = now.strftime("%m-%d-%Y_%H-%M-%S")
        # Use Timestamp as image name
        image_path = session_path + dt_string + '.jpg'
        camera.capture(image_path)
        print(f'Image Captured : {image_path}')

    def help_manual(self):
        print(f'Syntax : manual x')
        print(f'Where x is iso')

    def do_set_resolution(self, inp):
        arg = tuple(map(int, inp.split()))
        camera.resolution = (arg[0],arg[1])
       
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
    
    def do_transfer(inp):
        global session_path
        inp += ' '
        ip_value = re.search('--ip (.+?) ', inp)
        user_value = re.search('--user (.+?) ', inp)
        scp_cmd = 'scp -r %s %s@%s:/C:/Users/%s/Desktop/' % \
            (session_path, user_value.group(1), ip_value.group(1), user_value.group(1))
        subprocess.run(scp_cmd)

    def help_transfer(self):
        print(f'Transfers images to the computer')

def version_check(old_ver, new_ver):

    old_ver_t = tuple(map(int, old_ver.split('.')))
    new_ver_t = tuple(map(int, new_ver.split('.')))
    for i in range(3):
        diff =  new_ver_t[i] - old_ver_t[i]
        if diff is 0:
            continue
        if diff > 0:
            update = 'Released version %s is now available' % (new_ver)
        else:
            update = 'Developlment version installed'
        return '%s' % (update)
    return 'Latest released version installed'

def detect_camera():

    if (picam_version == 'ov5647'):
        return ' Detected Camera Module v1'
    elif (picam_version == 'imx219'):
        return ' Detected Camera Module v2'
    elif (picam_version == 'imx477'):
        return ' Detected HQ Camera'
    else:
        return ' Camera Model Unknown or no camera detected'

def setup_camera():
    camera = PiCamera(framerate=30)
    picam_version = camera.revision
    camera.resolution = camera.MAX_RESOLUTION
    return ' Camera resolution set to maximum : %s' % (camera.resolution)

if __name__ == '__main__':

    print(f'Starting Application...')
    print(detect_camera())
    print(setup_camera())
    print(version_check(installed_release, latest_release))
    PiShell().cmdloop()