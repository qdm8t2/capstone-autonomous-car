from Driver import Driver
from Driver import Direction

import atexit

driver=Driver();

#Driving Tests

#Test drive forward. Observe to determine pass or fail.
print("Forward Test")
driver.drive(Direction.FORWARD,100,2)

#Test drive Backward. Observe to determine pass or fail.
print("Backward Test")
driver.drive(Direction.BACKWARD,100,2)

#Test left. Observe to determine pass or fail.
print("Left Test")
driver.turn(Direction.LEFT,150)

#Test right. Observe to determine pass or fail.
print("Right Test")
driver.turn(Direction.RIGHT,150)









#THIS NEEDS TO RUN WHEN A DRIVER IS CREATED
#What this does is makes sure that if the program is killed,
#the motors will stop and not run forever
atexit.register(driver.turnOffMotors)