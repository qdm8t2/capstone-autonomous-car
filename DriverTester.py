from Driver import Driver
from Driver import Direction

driver = Driver()

import atexit

import tty
import sys
import termios

orig_settings = termios.tcgetattr(sys.stdin)
tty.setraw(sys.stdin)

x = 0

driver = Driver()

while x != chr(27):
	x = sys.stdin.read(1)[0]
	if x == "w":
		print("Forward")
		driver.drive(Direction.FORWARD, 150)
	elif x == "a":
		print("Left")
		driver.turn(Direction.LEFT, 200)
	elif x == "d":
		print("Right")
		driver.turn(Direction.RIGHT, 200)
	elif x == "s":
		print("Backward")
		driver.drive(Direction.BACKWARD, 150)
	else:
		print("Idle")
		driver.turnOffMotors()

atexit.register(driver.turnOffMotors)
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)

quit()
# driver=Driver();

# var=raw_input("Command:")

# while var!='q':
# 	if var=='w':
# 		driver.drive(Direction.FORWARD,150,1)
# 	if var=='d':
# 		driver.turn(Direction.RIGHT,200)
# 	if var=='a':
# 		driver.turn(Direction.LEFT,200)
# 	if var=='s':
# 		driver.drive(Direction.BACKWARD,150,1)
# 	if var=='z':
# 		driver.curveTurn(Direction.RIGHT,150)

# 	var = raw_input("Command:")







#THIS NEEDS TO RUN WHEN A DRIVER IS CREATED
#What this does is makes sure that if the program is killed,
#the motors will stop and not run forever
atexit.register(driver.turnOffMotors)