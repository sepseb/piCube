from distutils.command.config import config
from email.policy import default
from importlib.resources import path
from ssl import SSLSession
from matplotlib import use
from picamera import PiCamera
from picamera.array import PiBayerArray
from datetime import datetie
from adafruit_servokit import ServoKit
from time import sleep
from cmd import Cmd
import subprocess
import os
import configparser
import numpy as np

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

camera = PiCamera()
picam_version = camera.revision
camera.resolution = camera.MAX_RESOLUTION

if (picam_version == 'ov5647'):
    print(f'Detected Camera Module v1')
elif (picam_version == 'imx219'):
    print(f'Detected Camera Module v2')
elif (picam_version == 'imx477'):
    print(f'Detected HQ Camera')
else:
    print(f'Camera Model Unknown or no camera detected')

print(f'Camera resolution set to maximum {camera.resolution}')

class PiShell(Cmd):

    prompt = 'PiCube $ '
    intro = "\n--------------------------------------"\
            "\n PiCube Interface Program v0.1.0"\
            "\n Type help for a list of commands"\
            "\n Type exit to leave the program"\

    def do_exit(self,inp):
        # Add code to stop any running tasks with camera
        return True

    def help_exit(self):
        print(f'Exit the program')

    def do_cap_raw(self, inp):
        global session_path
        arg = parse(inp)
        now = datetime.now()
        dt_string = now.strftime("%m-%d-%Y_%H-%M-%S")
        # Use Timestamp as image name
        image_path = session_path + dt_string + '.raw'
        with PiBayerArray(camera) as stream:
            camera.capture(stream, 'jpeg', bayer=True)
            output = (stream.demosaic() >> 2).astype(np.uint8)
            with open(image_path, 'wb') as f:
                output.tofile(f)
       
    def help_cap_raw(self):
        print(f'Syntax : cap_raw')
        print(f'Takes a raw image')

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

    def do_capture(self,inp):
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

    def help_capture(self):
        print(f'Syntax : capture x')
        print(f'Captures one picture ')
        print(f'If x = ts, filename is current data_time.jpg')
        print(f'If x = gps, filename is current lat_lon.jpg')

    def do_exp(self,inp):
        camera.exposure_mode = inp

    def help_exp(self):
        print(f'Syntax : exp [exposure mode]')
        print(f'Exposure Modes: off, auto, night, backlight, ...')
        print(f'spotlight,sports, snow, beach, verylong, fireworks')

    def do_cap(self,inp):

        global session_path
        arg = parse(inp)
        camera.iso = arg[0]
        now = datetime.now()
        dt_string = now.strftime("%m-%d-%Y_%H-%M-%S")
        # Use Timestamp as image name
        image_path = session_path + dt_string + '.jpg'
        camera.capture(image_path)
        print(f'Image Captured : {image_path}')

    def help_cap(self):
        print(f'Syntax : cap x')
        print(f'Where x is iso')

    def do_burst_mode(self, inp):
        global session_path
        arg = parse(inp)
        for i in range(arg[0]):
            sleep(arg[1])
            now = datetime.now()
            dt_string = now.strftime("%m-%d-%Y_%H-%M-%S")
            image_path = session_path + dt_string + '.jpg'
            camera.capture(image_path % i)

    def help_burst_mode(self):
        print(f'Syntax : burst_mode x y')
        print(f'Captures total of x pictures; one picture every y seconds')

    def do_set_resolution(self, inp):
        arg = parse(inp)
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
    
    def do_transfer(self, inp):
        #to add later
        subprocess.run(["scp", 'FILE', "USER@SERVER:PATH"])

    def help_transfer(self):
        print(f'Transfers images to the computer')

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

if __name__ == '__main__':

    PiShell().cmdloop()