# Imports
import pygame
import picamera
import tty
import sys


# Pygame set up
pygame.init()
pygame.joystick.init()
pygame.display.set_mode()



tty.setraw(sys.stdin)

# Run loop
while True:
	for event in pygame.event.get():
		print("event")
		if event.type == pygame.JOYBUTTONDOWN:
			print("Down Event")
			print(event.button)
		