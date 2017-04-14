#!/usr/bin/python

import picamera
import time
import pygame
import tty
import sys
import os
from PIL import Image

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
		now=time.time()
		file_string ="data/forward/img_" + time.strftime("%y%m%d_%H-%M-%S") + ".jpg"
		cam.capture(file_string)
		file_string ="data/forward/img_" + time.strftime("%y%m%d_%H-%M-%S") + ".jpg"
		cam.capture(file_string)
		then=time.time()
		print("%s function took %f ms" % (file_string, (then-now)*1000.0))
	elif x == "d":
		file_string ="data/right/img_" + time.strftime("%y%m%d_%H-%M-%S") + ".jpg"
		cam.capture(file_string)
                
# cam.stop_preview()
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
