# Imports
from Driver import Driver, Direction
import NeuralNetworkThree
import DataHandler
import pygame
import picamera
import tty
import sys
import time
import math
import threading
import datetime
import io

# Pygame set up
pygame.init()
pygame.joystick.init()
pygame.display.set_mode()

# Initialize variables
joystick_set = False
driver = Driver()
cam = picamera.PiCamera()
cam.hflip = True
cam.vflip=True
cam.resolution = (1280, 720)
cam.framerate=80
camInterval=.5

# Idle will let the program know when an action is being taken, and trigger a picture. 
# Action will specefy the action being taken, so the filepath can be resolved
idle=True
action=""

tty.setraw(sys.stdin)
# Set current time in seconds
secondTracker=camInterval*round(time.time()/camInterval)

# Run loop
while True:
	for event in pygame.event.get():
		# Joypad button presses
		if event.type == pygame.JOYBUTTONDOWN:
			# Up
			if event.button == 4:
				driver.drive(Direction.FORWARD, 150)
				idle=False
				action="forward"
			# Down
			if event.button == 6:
				driver.drive(Direction.BACKWARD, 150)
				idle=False
				action="backward"
			# Right
			if event.button == 5:
				action="right"
				# Need to take picture before to prevent blur
				file_string ="data/"+action+"/img_" + datetime.datetime.now().strftime("%H-%M-%S-%f") + ".jpg"
				cam.capture(file_string,use_video_port=True)
				# cam.capture(file_string)
				driver.turn(Direction.RIGHT, 255)
			# Left
			if event.button == 7:
				action="left"
				# Need to take picture before to prevent blur
				file_string ="data/"+action+"/img_" + datetime.datetime.now().strftime("%H-%M-%S-%f") + ".jpg"
				cam.capture(file_string,use_video_port=True)
				# cam.capture(file_string)
				driver.turn(Direction.LEFT, 255)

			# UP
			if event.button == 12:
				driver.drive(Direction.FORWARD, 150)
			# Down
			if event.button == 14:
				driver.drive(Direction.BACKWARD, 150)
			# Right
			if event.button == 13:
				driver.turn(Direction.RIGHT, 255)
			# Left
			if event.button == 15:
				driver.turn(Direction.LEFT, 255)

			# Initiate Auto Mode
			if event.button == 3:
				AutoMode()

				
				

		# Check if picture should be taken
		currSeconds=camInterval*round(time.time()/camInterval)
		# print(currSeconds)
		if not idle and currSeconds!=secondTracker:
			file_string ="data/"+action+"/img_" + datetime.datetime.now().strftime("%H-%M-%S-%f") + ".jpg"
			cam.capture(file_string,use_video_port=True)
			# cam.capture(file_string)
			secondTracker=currSeconds

		# Turn off motors if leaving game or done pressing button
		if event.type == pygame.QUIT or event.type == pygame.KEYUP or event.type == pygame.JOYBUTTONUP:
			driver.turnOffMotors()
			idle=True

		# Handle exit
		if event.type == pygame.QUIT:
			pygame.quit()

		# Keyboard press
		if event.type == pygame.KEYDOWN:
			# W (forward)			
			if event.key == pygame.K_w:
				file_string ="data/forward/img_" + datetime.datetime.now().strftime("%H-%M-%S-%f") + ".jpg"
				cam.capture(file_string)
				driver.drive(Direction.FORWARD, 150)
			# S (backwards)
			if event.key == pygame.K_s:
				file_string ="data/backward/img_" + datetime.datetime.now().strftime("%H-%M-%S-%f") + ".jpg"
				cam.capture(file_string)
				driver.drive(Direction.BACKWARD, 150)
			# A (left)
			if event.key == pygame.K_a:
				file_string ="data/left/img_" + datetime.datetime.now().strftime("%H-%M-%S-%f") + ".jpg"
				cam.capture(file_string)
				driver.turn(Direction.LEFT, 255)
			# D (right)
			if event.key == pygame.K_d:
				file_string ="data/right/img_" + datetime.datetime.now().strftime("%H-%M-%S-%f") + ".jpg"
				cam.capture(file_string)
				driver.turn(Direction.RIGHT, 255)
	
	# Configure joystick if not already set
	if not joystick_set:
		for i in range(pygame.joystick.get_count()):
			joystick = pygame.joystick.Joystick(i)
			joystick.init()
			joystick_set = True
			print("Joystick enabled")

	def AutoMode():
		# Initializing variables
		running=True
		stream=io.BytesIO() #where we store the pictures  
		# cam.hflip = True
		# cam.vflip=True
		# cam.resolution = (1280, 720)
		# cam.framerate=80

		print("Auto mode started")


		# Loop me til you kill me
		while running:
			# take a picture
			cam.capture(stream,'rgb',use_video_port=True)

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
				if prediction_index==1:
					driver.turn(Direction.RIGHT, 255)
				# Left
				if prediction_index==2:
					driver.turn(Direction.LEFT, 255)
				

			finally:
				# Reset the stream and event
				stream.seek(0)
				stream.truncate()


			# checks if the player hits the start key, indicating that they want to stop autonomous mode
			for event in pygame.event.get():
				if event.type == pygame.JOYBUTTONDOWN and event.button==3:
					running=False