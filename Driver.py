from Adafruit_MotorHAT import Adafruit_MotorHAT
from enum import Enum
 
import time
import atexit

class Direction(Enum):
    FORWARD=1
    BACKWARD=2
    LEFT=3
    RIGHT=4

_DefaultForwardSpeed=150
_DefaultTurnSpeed=255


class Driver:

    # Driver creation and setup
    def __init__(self):
        self.mh=Adafruit_MotorHAT(addr=0x60)
        self.rMotors=[]
        self.lMotors=[]
        self.rMotors.insert(1,self.mh.getMotor(1))
        self.rMotors.insert(2,self.mh.getMotor(2))
        self.lMotors.insert(3,self.mh.getMotor(3))
        self.lMotors.insert(4,self.mh.getMotor(4))
        self.forwardSpeed=_DefaultForwardSpeed
        self.turnSpeed=_DefaultTurnSpeed

    # Execute a forward or backward action
    def drive(self,direction,speed):
        # check the direction
        if direction == Direction.FORWARD:
            lDirection=Adafruit_MotorHAT.BACKWARD
            rDirection=Adafruit_MotorHAT.FORWARD
        elif direction== Direction.BACKWARD:
            lDirection=Adafruit_MotorHAT.FORWARD
            rDirection=Adafruit_MotorHAT.BACKWARD
        else:
            return

        for motor in self.lMotors:
            motor.run(lDirection)
            motor.setSpeed(speed)
        for motor in self.rMotors:
            motor.run(rDirection)
            motor.setSpeed(speed)
        return

    # Execute a turn
    def turn(self,direction,speed):
        # check the direction
        if direction == Direction.LEFT:
            mDirection = Adafruit_MotorHAT.BACKWARD
            motor = self.lMotors[0]
            motor.run(mDirection)
            motor.setSpeed(speed)
		
            motor = self.lMotors[1]
            motor.run(mDirection)
            motor.setSpeed(speed)

            motor = self.rMotors[0]
            motor.run(mDirection)
            motor.setSpeed(speed)

            motor = self.rMotors[1]
            motor.run(mDirection)
            motor.setSpeed(speed)

        else:
            mDirection = Adafruit_MotorHAT.FORWARD
            motor = self.lMotors[0]
            motor.run(mDirection)
            motor.setSpeed(speed)
		
            motor = self.lMotors[1]
            motor.run(mDirection)
            motor.setSpeed(speed)

            motor = self.rMotors[0]
            motor.run(mDirection)
            motor.setSpeed(speed)

            motor = self.rMotors[1]
            motor.run(mDirection)
            motor.setSpeed(speed)	
        return

    # Number between 0 and 255
    def setForwardSpeed(self,forwardSpeed):
        self.forwardSpeed=forwardSpeed
        
    # Number between 0 and 255
    def setForwardSpeed(self,forwardSpeed):
        self.forwardSpeed=forwardSpeed


    def stop(self):
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
