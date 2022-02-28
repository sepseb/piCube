from picamera import PiCamera
from time import sleep
from cmd import Cmd
import os

class PiShell(Cmd):
    prompt = 'PiCube $ '
    intro = "\n--------------------------------------"\
            "\nPiCube Camera Interface Software"\
            "\n Enter help for a list of commands"\
            "\n Enter exit to leave the program"

    def do_exit(self,inp):
        # Add code to stop any running tasks with camera
        return True

    def help_exit(self):
        print('Exit the program')

    def do_take_pic(self):
        camera.capture('/home/pi/Desktop/image.jpg')

    def help_take_pic

    def do_burst_mode(self):
        for i in range(5):
            sleep(5)
            camera.capture('/home/pi/Desktop/image%s.jpg' % i)

    do_exit = do_EOF
    help_exit = help_EOF


if __name__ = '__main__':

    camera = PiCamera()
    # Turn the camera's LED off
    camera.led = False
    PiShell().cmdloop()
