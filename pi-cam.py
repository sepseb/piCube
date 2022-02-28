from picamera import PiCamera
from time import sleep
from cmd import Cmd
import os

camera = PiCamera()
# Turn the camera's LED off
camera.led = False

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
        print('Exit the program')

    def do_create_dir(self,inp):
        print("Default: {}".format(inp))

    def help_create_dir(self):
        print('Create directory for pictures')

    def do_take_pic(self,inp):
        camera.capture('/home/pi/Desktop/image.jpg')

    def help_take_pic(self):
        print('Takes one picture')

    def do_burst_mode(self,inp):
        for i in range(5):
            sleep(5)
            camera.capture('/home/pi/Desktop/image%s.jpg' % i)
    def help_burst_mode(self):
        print('Takes 5 pictures')

    do_EOF = do_exit
    help_EOF = help_exit

if __name__ == '__main__':

    PiShell().cmdloop()
