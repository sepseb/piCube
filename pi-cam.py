from picamera import PiCamera
from datetime import datetime
from time import sleep
from cmd import Cmd
import subprocess
import os

default_path = '/home/pi/Documents/'
camera = PiCamera()

class PiShell(Cmd):
    prompt = 'PiCube $ '
    intro = "\n--------------------------------------"\
            "\n PiCube Camera Interface Software"\
            "\n Enter help for a list of commands"\
            "\n Enter exit to leave the program"

    def do_exit(self,inp):
        # Add code to stop any running tasks with camera
        return True

    def help_exit(self):
        print(f'Exit the program')

    def do_create_dir(self,inp):
        path =  default_path + inp
        if (os.path.isfile(path) == False):
            os.mkdir(path)
            print(f'Created directory : {path}')
        else:
            print(f'Directory Already Exists')

    def help_create_dir(self):
        print(f'Syntax : create_dir [folder name]')
        print(f'Create directory for pictures')

    def do_capture(self,inp):
        if (inp == 'ts'):
            now = datetime.now()
            dt_string = now.strftime("%d%m%Y_%H%M%S")
            # Use Timestamp as image name
            image_path = default_path + dt_string + '.jpg'
        elif (inp == 'gps'):    
            # Use GPS location as image name - Future addition
            image_path = default_path + 'gps.jpg'
        camera.capture(image_path)

    def help_capture(self):
        print(f'Syntax : capture [x]')
        print(f'Captures one picture ')
        print(f'If x = ts, filename is current data_time.jpg')
        print(f'If x = gps, filename is current lat_lon.jpg')

    def do_burst_mode(self, inp):
        arg = parse(inp)
        for i in range(arg[0]):
            sleep(arg[1])
            image_path = default_path + 'image%s.jpg'
            camera.capture(image_path % i)

    def help_burst_mode(self):
        print(f'Syntax : burst_mode [x] [y]')
        print(f'Captures total of x pictures; one picture every y seconds')

    def do_transfer(self, inp):
        #to add later
        subprocess.run(["scp", 'FILE', "USER@SERVER:PATH"])

    def help_transfer(self):
        print(f'Transfers images to the computer')    

    do_EOF = do_exit
    help_EOF = help_exit

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

if __name__ == '__main__':

    PiShell().cmdloop()
