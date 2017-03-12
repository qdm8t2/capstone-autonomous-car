from Driver import Driver

import atexit

driver=Driver();

driver.driveForward(200,2)


#THIS NEEDS TO RUN WHEN A DRIVER IS CREATED
#What this does is makes sure that if the program is killed,
#the motors will stop and not run forever
atexit.register(driver.turnOffMotors)