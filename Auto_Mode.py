# Imports
from Driver import Driver, Direction
import ImageProcess
import pygame
import picamera
import tty
import sys
import NeuralNetworkThree

# Initializing variables
continue=True
stream=io.BytesIO() #where we store the pictures
processer = ImageProcess.ImageProcess()   
driver = Driver()
cam = picamera.PiCamera()
cam.hflip = True
cam.vflip=True
cam.resolution = (1280, 720)
cam.framerate=80

print("Auto mode started")


# Loop me til you kill me
while continue:
	# take a picture
	cam.capture(stream,use_video_port=True)

	# Read In Photo
	try:
		stream.seek(0)
		
		dh = DataHandler(initialize_files=False)
		nn = NeuralNetwork()
		nn.load()
		im = imread(stream, flatten=True)
		prediction = nn.predict([im], True)
		prediction_index = dh.determine_index(prediction)
		print("Prediction:", dh.index_to_description(prediction_index))

		# Forward
		if prediction_index==0:
			driver.drive(Direction.FORWARD, 150)
		# Right
		else if prediction_index==1:
			driver.turn(Direction.RIGHT, 255)
		# Left
		else if prediction_index==2:
			driver.turn(Direction.LEFT, 255)
		

	finally:
		# Reset the stream and event
		self.stream.seek(0)
		self.stream.truncate()


	# checks if the player hits the start key, indicating that they want to stop autonomous mode
	for event in pygame.event.get():
		if event.type == pygame.JOYBUTTONDOWN and event.button==3:
			continue=False