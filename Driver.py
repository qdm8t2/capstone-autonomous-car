from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
 
import time
import atexit

class Driver:

    def __init__(self):
        self.mh=Adafruit_MotorHAT(addr=0x60)
        self.rMotors=[]
        self.lMotors=[]
        self.rMotors.insert(1,self.mh.getMotor(1))
        self.rMotors.insert(2,self.mh.getMotor(2))
        self.lMotors.insert(3,self.mh.getMotor(3))
        self.lMotors.insert(4,self.mh.getMotor(4))

    def driveForward(self,speed,runtime):
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



    def turnOffMotors(self):
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)