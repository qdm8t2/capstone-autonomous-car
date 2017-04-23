# Imports
from Driver import Driver, Direction
import ImageProcess
import pygame
import picamera
import tty
import sys

# Initializing variables
continue=True
stream=io.BytesIO() #where we store the pictures
processer = ImageProcess.ImageProcess()   
cam = picamera.PiCamera()
cam.hflip = True
cam.vflip=True
cam.resolution = (1280, 720)
cam.framerate=80


# Loop me til you kill me
while continue:
	# take a picture
	cam.capture(stream,use_video_port=True)

	# Read In Photo
	try:
		stream.seek(0)
		# Unneeded - Done in image processor
		# im=Image.open(stream)
		processer.imageProcesser(stream)
		

	finally:
		# Reset the stream and event
		self.stream.seek(0)
		self.stream.truncate()


	# checks if the player hits the start key, indicating that they want to stop autonomous mode
	for event in pygame.event.get():
		if event.type == pygame.JOYBUTTONDOWN and event.button==3:
			continue=False