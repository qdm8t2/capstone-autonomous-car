from Driver import Driver
from Driver import Direction

import atexit

driver=Driver();

var=raw_input("Command:")

while var!='q':
	if var=='w':
		driver.drive(Direction.FORWARD,100,2)
	if var=='d':
		driver.turn(Direction.RIGHT)
	if var=='a':
		driver.turn(Direction.LEFT)
	if var=='s':
		driver.drive(Direction.BACKWARD,100,2)

	var = raw_input("Command:")





#THIS NEEDS TO RUN WHEN A DRIVER IS CREATED
#What this does is makes sure that if the program is killed,
#the motors will stop and not run forever
atexit.register(driver.turnOffMotors)