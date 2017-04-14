#!/usr/bin/python

import os
import picamera
import time

class PictureFactory:
    action="idle"
    shutdown=False

    def beginCapture:
        cam = picamera.PiCamera()
        cam.resolution = (1024, 768)
        cam.framerate=30

        cam.hflip = True
        cam.vflip=True

        cam.start_preview()
        time.sleep(5)
        now=time.time()
        for filename in cam.capture_continuous('data/'+self.action+'/img{timestamp:%Y-%m-%d-%H-%M}.jpg'):
            print('Captured %s' % (action+"/"+filename))
            if shutdown:
                break
        then=time.time()
        cam.stop_preview()

    def changeAction(action):
        self.action=action

    def shutdown:
        self.shutdown=True