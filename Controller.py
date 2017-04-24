# Imports
from Driver import Driver, Direction
from NeuralNetworkThree import NeuralNetwork
from NeuralNetworkThree import ImageProcessor
from DataHandler import DataHandler
from scipy.misc import imread,imshow
import pygame
import picamera
import tty
import sys
import time
import math
import threading
import datetime
import io
from PIL import Image

# Pygame set up
pygame.init()
pygame.joystick.init()
screen=pygame.display.set_mode((1280, 720))

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

# tty.setraw(sys.stdin)
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
			driver.stop()
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

		# cam.start_preview(fullscreen=False, window = (100, 20, 640, 480))
		dh = DataHandler(initialize_files=False)
		nn = NeuralNetwork()
		nn.load()

		# Loop me til you kill me
		while running:
			y=time.time()
			# take a picture
			# SS
			cam.capture('curr.jpg',format='jpeg',use_video_port=True)
			
			# cam.capture('curr.jpg',use_video_port=True)

			# Read In Photo
			#TODO BREAK THIS, its not needed
			if True:
				# SS
				# stream.seek(0)

				#SS
				# im = imread(stream, flatten=True)
				# stream.seek(0)


				im = imread('curr.jpg', flatten=True)
				# print('Time to take and read:',round(time.time() - y, 5))
				y=time.time()
				
				# curr=Image.open(stream)
				# raw_str = curr.tostring("raw", 'RGBA')
				# frame = pygame.image.fromstring(raw_str,len(raw_str),"RGB")
				frame=pygame.image.load('curr.jpg')
				screen.blit(frame,(0,0))
				pygame.display.flip()
				# print('Time to display:',round(time.time() - y, 5))

				x = time.time()
				a, prediction = nn.predict([im], True)
				print('Prediction time:', round(time.time() - x, 5), 'seconds')
				print('Forward Match  :', round(prediction[0][0]*100, 3), '%')
				print('Right Match    :', round(prediction[0][1]*100, 3), '%')
				print('Left Match     :', round(prediction[0][2]*100, 3), '%')
				prediction_index = dh.determine_index(prediction)
				print("Prediction     :", dh.index_to_description(prediction_index))
				print('----------------')
				# print("Prediction:", dh.index_to_description(prediction_index))
				#SS
				# stream.flush()
				# Forward
				if prediction_index==0:
					driver.drive(Direction.FORWARD, 150)
					time.sleep(.25)
					driver.stop()
				# Right
				if prediction_index==1:
					driver.turn(Direction.RIGHT, 255)
					time.sleep(.1)
					driver.stop()
				# Left
				if prediction_index==2:
					driver.turn(Direction.LEFT, 255)
					time.sleep(.1)
					driver.stop()


				

			# finally:
			# # 	print("")
			# 	# Reset the stream and event
			# 	# SS
			# 	stream.seek(0)
			# 	stream.truncate()


			# checks if the player hits the start key, indicating that they want to stop autonomous mode
			for event in pygame.event.get():
				if event.type == pygame.JOYBUTTONDOWN and event.button==3:
					running=False