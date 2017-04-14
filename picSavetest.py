#!/usr/bin/python

import os
from PIL import *
from PIL import Image
from numpy import *
#from pylab import *
from PIL import ImageOps
import picamera
import time
import os.path

cam = picamera.PiCamera()
cam.resolution = (640, 480)
cam.framerate = 120

cam.hflip = True
cam.vflip=True

#cam.exposure_compensation = 25
#cam.brightness = 55
#cam.exposure_mode = 'off'
#cam.awb_mode = 'off'

cam.start_preview()
# time.sleep(5)

time.sleep(5)
cam.stop_preview()
numPics=10
i=0
now=time.time()
for filename in cam.capture_continuous('Test/img{timestamp:%Y-%m-%d-%H-%M}.jpg'):
    print('Captured %s' % filename)
    i+=1
    if i>numPics: 
        break
then=time.time()
print("function took %.3f ms per picture" % ((((then-now)*1000.0))/numPics))