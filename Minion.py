from enum import Enum
import time
import random
import RPi.GPIO as gpio
import UltraSound
import Movement
import logging
import ArduinoCommunication
import Camera
import WifiSignals
import HunterAI

logging.basicConfig(filename='example.log',level=logging.DEBUG, format="%(asctime)-15s %(levelname)s:\t %(message)s")
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

#### Pins On the Raspy

try:
    gpio.cleanup()
finally:
    print("no cleanup")

gpio.setmode(gpio.BCM)

#UltraSound
TRIG_PIN=20
ECHO_PIN=21
gpio.setup(TRIG_PIN, gpio.OUT)
gpio.setup(ECHO_PIN, gpio.IN)

#Engines
#Engine Left
EnableLeftEngines = 4
IN1=17
IN2=18
gpio.setup(EnableLeftEngines, gpio.OUT)
gpio.setup(IN1, gpio.OUT)
gpio.setup(IN2, gpio.OUT)
#Engine Right
EnableRightEngines = 23
IN3=27
IN4=22
gpio.setup(EnableRightEngines, gpio.OUT)
gpio.setup(IN3, gpio.OUT)
gpio.setup(IN4, gpio.OUT)
####


usDistance = UltraSound.UltraSoundHandler()
usDistance.TRIG_PIN=TRIG_PIN
usDistance.ECHO_PIN=ECHO_PIN
usDistance.StartMeasuring()

engines = Movement.HandleEngines()
engines.EnableLeftEngines = EnableLeftEngines
engines.IN1 = IN1
engines.IN2 = IN2
engines.EnableRightEngines = EnableRightEngines
engines.IN3 = IN3
engines.IN4 = IN4
engines.RobotStop()

engines.SetOnTime = 0.005 
engines.SetOffTime = 0.01 
engines.RegulateSpeed()

engines.RobotStop()
#input("Press to Start")

# Fix Python 2.x.
try: 
    input = raw_input
except NameError: 
    pass

ardy = ArduinoCommunication.ArduinoCommunication()
camera = Camera.CameraHandler()
Wifi = WifiSignals.WifiSignals()
LoopNo = 20
try:
    while(LoopNo>0):
        print(LoopNo)

        use_command_line = input("Your command:")
        user_commands = use_command_line.split(' ')
        #print(user_commands)

        for user_command in user_commands:
            print("user_command : " + user_command)
            if(user_command.upper() == 'F'):
                engines.RobotMoveForward()
            elif(user_command.upper() == 'B'):
                engines.RobotMoveBack()
            elif(user_command.upper() == 'L'):
                engines.RobotMoveLeft()
                #engines.RobotMoveRightWheels()
            elif(user_command.upper() == 'R'):
                engines.RobotMoveRight()
            elif(user_command.upper() == 'S'):
                print("Stopping")
                engines.RobotStop()
            elif(user_command.upper() == 'G'):
                ardy.printServoLocations()
            elif(user_command.upper() == 'U'):
               print("Ultrasound Distance = " +str(usDistance.UltraDistance))
            elif(user_command.upper() == 'SIDE'):
                #ardy.MoveServo('1', 10)
                #ardy.MoveServo('2', 10)
                #ardy.MoveServo('3', 80)
                #ardy.MoveServo('4', 160)
                ardy.MoveServo('1', 5)

                ardy.MoveServo('2', 5)
                ardy.MoveServo('3', 70)
                ardy.MoveServo('4', 160)
            elif(user_command.upper() == 'START'):
                #ardy.MoveServo('1', 87)
                #ardy.MoveServo('2', 160)
                #ardy.MoveServo('3', 60)
                #ardy.MoveServo('4', 166)
                ardy.MoveServo('4', 175)
                time.sleep(0.8)
                ardy.MoveServo('1', 90)
                time.sleep(0.8)
                ardy.MoveServo('3', 70)
                time.sleep(0.8)
                ardy.MoveServo('2', 177)
                time.sleep(0.8)
            elif(user_command.upper() == 'DOWN'):
                ardy.MoveServo('4', 100)
                time.sleep(0.8)
                ardy.MoveServo('1', 90)
                time.sleep(0.8)
                ardy.MoveServo('2', 5)
                time.sleep(0.8)
                ardy.MoveServo('3', 40)
                time.sleep(0.8)
            elif(user_command.upper() == 'HUNT'):
                NO_OF_SEARCHTURNS_ALLOWED = 5
                while(NO_OF_SEARCHTURNS_ALLOWED > 0):
                    imagename = camera.takePicture()
                    res = HunterAI.Descision(imagename)
                    if(res == "grab"):
                        print("grabbing")
                        ardy.MoveServo('4', 170)
                        break
                    elif (res == "left"):
                        print("Moving left")
                        engines.RobotMoveLeft()
                        time.sleep(0.5)
                        engines.RobotStop()
                    elif (res == "forward"):
                        print("Forward")
                        engines.RobotMoveForward()
                        time.sleep(0.5)
                        engines.RobotStop()
                    elif (res == "Did not find anything"):
                        print("left searching")
                        engines.RobotMoveLeft()
                        time.sleep(1)
                        engines.RobotStop()
                        NO_OF_SEARCHTURNS_ALLOWED = NO_OF_SEARCHTURNS_ALLOWED - 1
                    
            elif(user_command.upper() == 'PIC'):
                camera.takePicture()
            elif(user_command.upper() == 'WIFI'):
                Wifi.Record()
            elif(user_command.upper() == "READ"):
                #print("Checking Serial reply")
                ardy.printAll()
            elif(user_command[0:3].upper() == 'SET'):
                ardy.MoveServo(user_command[3], int(user_command[4:]))
            elif(user_command.upper() == 'P'):
                ardy.pingArdy()
            elif(user_command.upper() == 'H'):
                ardy.printLastCommand()
            
            elif(user_command.upper() == 'Q'):
                LoopNo=0
                break
            elif(user_command.upper() == 'W'):
                time.sleep(0.5)
            
            LoopNo=LoopNo-1
        #UltraSoundHandler
        #distance = UltraSound.getUltaSoundDistance()
        
        #print("Distance to Base the decsions On = " +str(usDistance.UltraDistance))
        #if(usDistance.UltraDistance > 0.25):
        #    print("Forward")
        #    engines.RobotMoveForward()
            #engines.RobotMoveBack()
            #engines.RobotMoveLeft()
        #else:
        #    engines.RobotStop()

        #print(distance)
        #time.sleep(0.2)
        #LoopNo=LoopNo-1
finally:
    ardy.cleanup()  
    gpio.cleanup() # this ensures a clean exit