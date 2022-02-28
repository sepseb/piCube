from picamera import PiCamera
from time import sleep
from cmd import Cmd
import os

path = '/home/pi/Documents'
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
        path = '/home/pi/Documents/' + inp
        os.mkdir(path)
        print(f'Created directory : {path}')

    def help_create_dir(self):
        print('Create directory for pictures')

    def do_take_pic(self,inp):
        camera.capture('/home/pi/Desktop/image.jpg')

    def help_take_pic(self):
        print('Takes one picture')

    def do_burst_mode(self, inp):
        arg = parse(inp)
        for i in range(arg[0]):
            sleep(arg[1])
            image_path = path + 'image%s.jpg'
            camera.capture(image_path % i)

    def help_burst_mode(self):
        print('Synatx : burst_mode [X] [Y]')
        print('Captures total of X pictures; one picture every Y seconds')

    do_EOF = do_exit
    help_EOF = help_exit

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

if __name__ == '__main__':

    PiShell().cmdloop()
