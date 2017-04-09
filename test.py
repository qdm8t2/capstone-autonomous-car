# Imports
from Driver import Driver, Direction
import pygame
import picamera
import tty

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

tty.setraw(sys.stdin)

# Run loop
while True:
	for event in pygame.event.get():
		# Joypad button presses
		if event.type == pygame.JOYBUTTONDOWN:
			# Up
			if event.button == 4:
				file_string ="data/forward/img_" + time.strftime("%y%m%d_%H-%M-%S") + ".jpg"
				cam.capture(file_string)
				driver.drive(Direction.FORWARD, 150)
			# Down
			if event.button == 6:
				file_string ="data/backward/img_" + time.strftime("%y%m%d_%H-%M-%S") + ".jpg"
				cam.capture(file_string)
				driver.drive(Direction.BACKWARD, 150)
			# Right
			if event.button == 5:
				file_string ="data/right/img_" + time.strftime("%y%m%d_%H-%M-%S") + ".jpg"
				cam.capture(file_string)
				driver.turn(Direction.RIGHT, 255)
			# Left
			if event.button == 7:
				file_string ="data/left/img_" + time.strftime("%y%m%d_%H-%M-%S") + ".jpg"
				cam.capture(file_string)
				driver.turn(Direction.LEFT, 255)

		# Turn off motors if leaving game or done pressing button
		if event.type == pygame.QUIT or event.type == pygame.KEYUP or event.type == pygame.JOYBUTTONUP:
			driver.turnOffMotors()

		# Handle exit
		if event.type == pygame.QUIT:
			pygame.quit()

		# Keyboard press
		if event.type == pygame.KEYDOWN:
			# W (forward)			
			if event.key == pygame.K_w:
				file_string ="data/forward/img_" + time.strftime("%y%m%d_%H-%M-%S") + ".jpg"
				cam.capture(file_string)
				driver.drive(Direction.FORWARD, 150)
			# S (backwards)
			if event.key == pygame.K_s:
				file_string ="data/backward/img_" + time.strftime("%y%m%d_%H-%M-%S") + ".jpg"
				cam.capture(file_string)
				driver.drive(Direction.BACKWARD, 150)
			# A (left)
			if event.key == pygame.K_a:
				file_string ="data/left/img_" + time.strftime("%y%m%d_%H-%M-%S") + ".jpg"
				cam.capture(file_string)
				driver.turn(Direction.LEFT, 255)
			# D (right)
			if event.key == pygame.K_d:
				file_string ="data/right/img_" + time.strftime("%y%m%d_%H-%M-%S") + ".jpg"
				cam.capture(file_string)
				driver.turn(Direction.RIGHT, 255)
	
	# Configure joystick if not already set
	if not joystick_set:
		for i in range(pygame.joystick.get_count()):
			joystick = pygame.joystick.Joystick(i)
			joystick.init()
			joystick_set = True
			print("Joystick enabled")