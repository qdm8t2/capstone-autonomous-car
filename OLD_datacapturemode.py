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
cam.resolution = (1280, 720)
cam.framerate=80

cam.hflip = True
cam.vflip=True

tty.setraw(sys.stdin)

x = 0

while x != chr(27):
	x = sys.stdin.read(1)[0]
	if x == "w":
		now=time.time()
		file_string ="data/forward/img_" + time.strftime("%y%m%d_%H-%M-%S") + ".jpg"
		cam.capture(file_string,use_video_port=True)
		then=time.time()
		print("%s function took %f ms" % (file_string, (then-now)*1000.0))
	elif x == "d":
		file_string ="data/right/img_" + time.strftime("%y%m%d_%H-%M-%S") + ".jpg"
		cam.capture(file_string)
