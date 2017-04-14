#!/usr/bin/python

import picamera
#import time
import pygame
import tty
import sys
#import termios
import os
#from PIL import *
from PIL import Image
#from numpy import *

from PIL import ImageOps

cam = picamera.PiCamera()

cam.hflip = True
cam.vflip=True

#cam.start_preview()
#orig_settings = termios.tcgetattr(sys.stdin)
tty.setraw(sys.stdin)

x = 0
i=0

while x != chr(27):
	x = sys.stdin.read(1)[0]
	if x == "w":
            y = "forwardimage%s.jpg"%(i)
            cam.capture(y)
            print(y)
            i=i+1
            img = Image.open(y)
            img.save('forward/' + y)
                
cam.stop_preview()
#var = raw_input("Command:")
#i=0
#while var != 'q':
#    if var == 'w':
#        y = "testimage%s.jpg"%(i)
#        cam.capture(y)
#        print(y)
#        i=i+1
#    else:
#        print('invalid')
            
#    var = raw_input("Command:")
