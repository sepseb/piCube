from distutils.command.config import config
from email.policy import default
from importlib.resources import path
from ssl import SSLSession
from matplotlib import use
from picamera import PiCamera
from datetime import datetime
from adafruit_servokit import ServoKit
from time import sleep
from cmd import Cmd
import subprocess
import os
import configparser

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

class PiShell(Cmd):

    prompt = 'PiCube $ '
    intro = "\n--------------------------------------"\
            "\n PiCube Interface Program"\
            "\n Type help for a list of commands"\
            "\n Type exit to leave the program"

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

    def do_capture(self,inp):

        global session_path
        if not inp:
            now = datetime.now()
            dt_string = now.strftime("%m-%d-%Y_%H:%M:%S")
            # Use Timestamp as image name
            image_path = session_path + dt_string + '.jpg'
        else:
            # Use input as image name - Future addition
            image_path = session_path + inp + '.jpg'
        camera.capture(image_path)

    def help_capture(self):
        print(f'Syntax : capture x')
        print(f'Captures one picture ')
        print(f'If x = ts, filename is current data_time.jpg')
        print(f'If x = gps, filename is current lat_lon.jpg')

    def do_burst_mode(self, inp):
        global session_path
        arg = parse(inp)
        for i in range(arg[0]):
            sleep(arg[1])
            now = datetime.now()
            dt_string = now.strftime("%m-%d-%Y_%H:%M:%S")
            image_path = session_path + dt_string + '.jpg'
            camera.capture(image_path % i)

    def help_burst_mode(self):
        print(f'Syntax : burst_mode x y')
        print(f'Captures total of x pictures; one picture every y seconds')

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
