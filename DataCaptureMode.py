# Imports
from Driver import Driver, Direction
import pygame
import picamera
import tty
import sys
import time
import math
import threading
import datetime

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
				driver.turn(Direction.RIGHT, 255)
			# Left
			if event.button == 7:
				action="left"
				# Need to take picture before to prevent blur
				file_string ="data/"+action+"/img_" + datetime.datetime.now().strftime("%H-%M-%S-%f") + ".jpg"
				cam.capture(file_string,use_video_port=True)
				driver.turn(Direction.LEFT, 255)
				

		# Check if picture should be taken
		currSeconds=camInterval*round(time.time()/camInterval)
		print(currSeconds)
		if not idle and currSeconds!=secondTracker:
			file_string ="data/"+action+"/img_" + datetime.datetime.now().strftime("%H-%M-%S-%f") + ".jpg"
			cam.capture(file_string,use_video_port=True)
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