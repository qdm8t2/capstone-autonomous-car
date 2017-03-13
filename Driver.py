from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from enum import Enum
 
import time
import atexit

class Direction(Enum):
    FORWARD=1
    BACKWARD=2
    LEFT=3
    RIGHT=4


class Driver:

    def __init__(self):
        self.mh=Adafruit_MotorHAT(addr=0x60)
        self.rMotors=[]
        self.lMotors=[]
        self.rMotors.insert(1,self.mh.getMotor(1))
        self.rMotors.insert(2,self.mh.getMotor(2))
        self.lMotors.insert(3,self.mh.getMotor(3))
        self.lMotors.insert(4,self.mh.getMotor(4))

    def drive(self,direction,speed,runtime):
        print("StartMotor")
        for motor in self.lMotors:
            motor.run(Adafruit_MotorHAT.FORWARD)
            motor.setSpeed(speed)
        for motor in self.rMotors:
            motor.run(Adafruit_MotorHAT.BACKWARD)
            motor.setSpeed(speed)
        print("Waiting")
        time.sleep(runtime)
        for motor in self.lMotors:
            motor.setSpeed(0)
            motor.run(Adafruit_MotorHAT.RELEASE)
        for motor in self.rMotors:
            motor.setSpeed(0)
            motor.run(Adafruit_MotorHAT.RELEASE)
        print("Done")

    def turn(self,direction):
        if direction == Direction.LEFT:
            mDirection=Adafruit_MotorHAT.FORWARD
            mDirection=Adafruit_MotorHAT.BACKWARD
        else:
            mDirection=Adafruit_MotorHAT.BACKWARD
            mDirection=Adafruit_MotorHAT.FORWARD

        print("StartMotor")
        for motor in self.lMotors:
            motor.run(mDirection)
            motor.setSpeed(100)
        for motor in self.rMotors:
            motor.run(mDirection)
            motor.setSpeed(100)
        time.sleep(2)
        for motor in self.lMotors:
            motor.setSpeed(0)
            motor.run(Adafruit_MotorHAT.RELEASE)
        for motor in self.rMotors:
            motor.setSpeed(0)
            motor.run(Adafruit_MotorHAT.RELEASE)
        



    def turnOffMotors(self):
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)