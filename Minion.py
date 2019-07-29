from enum import Enum
import time
import random
import RPi.GPIO as gpio
import UltraSound
import Movement
import logging
import ArduinoCommunication

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

ardy = new ArduinoCommunication.ArduinoCommunication()

LoopNo = 20
try:
    while(LoopNo>0):
        print(LoopNo)

        use_command_line = input("Your command:")
        user_commands = use_command_line.split(' ')

        for user_command in user_commands:
            if(user_command.upper() == 'F'):
                engines.RobotMoveForward()
            elif(user_command.upper() == 'B'):
                engines.RobotMoveBack()
            elif(user_command.upper() == 'L'):
                engines.RobotMoveLeft()
            elif(user_command.upper() == 'R'):
                engines.RobotMoveRight()
            elif(user_command.upper() == 'G'):
                ardy.printServoLocations()
            elif(user_command[0] == 's'):
                ardy.MoveServo(user_command[0], int(user_command[2:]))
            
            time.sleep(0.2)
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