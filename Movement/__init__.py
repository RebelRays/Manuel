import RPi.GPIO as gpio
import time
from threading import Timer

class WheelCommand:
    Stop=0
    Forward=1
    Back=-1

LoopRegulateSpeedTimer = None
class HandleEngines:
    EnableRightEngines=-1
    EnableLeftEngines=-1
    IN1 = -1
    IN2 = -1
    IN3 = -1
    IN4 = -1

    #is set fromoutside?
    SetOnTime=0.05
    SetOffTime=0.005

    """description of class"""
    def MoveLeftWheels(self, command):
        if(command == WheelCommand.Stop):
            gpio.output(self.EnableLeftEngines, False)
            gpio.output(self.IN1, False)
            gpio.output(self.IN2, False)
        elif(command == WheelCommand.Forward):
            gpio.output(self.EnableLeftEngines, True)
            gpio.output(self.IN1, False)
            gpio.output(self.IN2, True)
        elif(command == WheelCommand.Back):
            gpio.output(self.EnableLeftEngines, True)
            gpio.output(self.IN1, True)
            gpio.output(self.IN2, False)
    def MoveRightWheels(self, command):
        if(command == WheelCommand.Stop):
            gpio.output(self.EnableRightEngines, False)
            gpio.output(self.IN3, False)
            gpio.output(self.IN4, False)
        elif(command == WheelCommand.Forward):
            gpio.output(self.EnableRightEngines, True)
            gpio.output(self.IN3, False)
            gpio.output(self.IN4, True)
        elif(command == WheelCommand.Back):
            gpio.output(self.EnableRightEngines, True)
            gpio.output(self.IN3, True)
            gpio.output(self.IN4, False)

    def RobotMoveForward(self):
        #print("MOvin")
        self.MoveLeftWheels(WheelCommand.Forward)
        self.MoveRightWheels(WheelCommand.Forward)
    def RobotMoveBack(self):
        #print("Moving BAck")
        self.MoveLeftWheels(WheelCommand.Back)
        self.MoveRightWheels(WheelCommand.Back)
    def RobotMoveRight(self):
        self.MoveLeftWheels(WheelCommand.Forward)
        self.MoveRightWheels(WheelCommand.Back)
    def RobotMoveLeft(self):
        self.MoveLeftWheels(WheelCommand.Back)
        self.MoveRightWheels(WheelCommand.Forward)
    def RobotMoveRightWheels(self):
        self.MoveRightWheels(WheelCommand.Forward)
        self.MoveLeftWheels(WheelCommand.Stop)
    def RobotStop(self):
        print("Stopping")
        self.MoveLeftWheels(WheelCommand.Stop)
        self.MoveRightWheels(WheelCommand.Stop)
    def RegulateSpeed(self):
        global LoopRegulateSpeedTimer
        t = Timer(0.001, self.LoopRegulateSpeed) #One time call
        LoopRegulateSpeedTimer = t
        t.start()
        return
    def cleanup(self):
        global LoopRegulateSpeedTimer
        LoopRegulateSpeedTimer = None
    def LoopRegulateSpeed(self):
        while LoopRegulateSpeedTimer is None:
            gpio.output(self.EnableRightEngines, True)
            gpio.output(self.EnableLeftEngines, True)
            time.sleep(self.SetOnTime)
            gpio.output(self.EnableRightEngines, False)
            gpio.output(self.EnableLeftEngines, False)
            time.sleep(self.SetOffTime)
            




