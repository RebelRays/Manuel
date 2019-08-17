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
import AITensorflow

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

engines.SetOnTime = 0.01
engines.SetOffTime = 0.06 
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

RecordInverseMoves = []
PlayingRecorded = []
def ExecCommand(user_command):


    ########################
    # Enviroment Commands
    if(user_command.upper() == 'W'):
        time.sleep(0.5)
        RecordInverseMoves.append('W')
    elif(user_command.upper() == 'GOBACK'):
        PlayingRecorded = RecordInverseMoves[:]

        for command in PlayingRecorded:
            ExecCommand(command)
        ExecCommand("S")
        RecordInverseMoves.clear()
    elif(user_command.upper() == 'SLOWEST'):
        engines.setSpeed(0.01, 2)
        print("Set to SLOWEST")
    elif(user_command.upper() == 'SLOW'):
        engines.SetOnTime = 0.02
        engines.SetOffTime = 0.01
        print("Set to Slow")
    elif(user_command.upper() == 'NORMAL'):
        engines.SetOnTime = 0.05
        engines.SetOffTime = 0.01
        print("Set to Normal")
    elif(user_command.upper() == 'BRIGHTER'):
        camera.makeBrighter()
        print("makeBrighter")
    elif(user_command.upper() == 'BRIGHTER2'):
        camera.makeBrighter2()
        print("makeBrighter")
    elif(user_command.upper() == 'BRIGHTERRESET'):
        camera.resetExposure()
        print("resetExposure")
    ########################
    # Engine Commands
    if(user_command.upper() == 'F'):
        engines.RobotMoveForward()
        RecordInverseMoves.append('B')
    elif(user_command.upper() == 'B'):
        engines.RobotMoveBack()
        RecordInverseMoves.append('F')
    elif(user_command.upper() == 'L'):
        engines.RobotMoveLeft()
        RecordInverseMoves.append('R')
        #engines.RobotMoveRightWheels()
    elif(user_command.upper() == 'R'):
        engines.RobotMoveRight()
        RecordInverseMoves.append('L')
    elif(user_command.upper() == 'S'):
        print("Stopping")
        engines.RobotStop()
        RecordInverseMoves.append('S')
    #########################
    #SENSORS
    elif(user_command.upper() == 'U'):
        print("Ultrasound Distance = " +str(usDistance.UltraDistance))
    elif(user_command.upper() == 'PIC'):
        camera.fastPic()
    elif(user_command.upper() == 'STOPPIC'):
        camera.closeCamera()
    elif(user_command.upper() == 'WIFI'):
        Wifi.Record()
    #########################
    #ROBOT CLAWS
    elif(user_command.upper() == 'G'):
        ardy.printServoLocations()
    elif(user_command.upper() == "READ"):
        ardy.printAll()
    elif(user_command.upper() == 'P'):
        ardy.pingArdy()
    elif(user_command[0:3].upper() == 'SET'):
        ardy.MoveServo(user_command[3], int(user_command[4:]))
    elif(user_command.upper() == 'UPP'):
        ardy.MoveServo('4', 175)
        time.sleep(0.8)
        ardy.MoveServo('1', 90)
        time.sleep(0.8)
        ardy.MoveServo('3', 70)
        time.sleep(0.8)
        ardy.MoveServo('2', 177)
        time.sleep(0.8)
    elif(user_command.upper() == 'DOWN'):
        ardy.MoveServo('4', 95)
        time.sleep(0.8)
        ardy.MoveServo('1', 90)
        time.sleep(0.8)
        ardy.MoveServo('2', 5)
        time.sleep(0.8)
        ardy.MoveServo('3', 40)
        time.sleep(0.8)
    elif(user_command.upper() == 'HOLD'):
        ardy.MoveServo('4', 175)
        time.sleep(0.8)
        ardy.MoveServo('1', 90)
        time.sleep(0.8)
        ardy.MoveServo('2', 20)
        time.sleep(0.8)
        ardy.MoveServo('3', 110)
        time.sleep(0.8)
    #########################
    #AI
    #generateboxes
    elif(user_command.upper() == 'SOCK'):
        print("Boxes")
        imagename = camera.fastPic()
        boxes = AITensorflow.generateboxes(imagename)
        print(boxes)
    elif(user_command.upper() == 'RANDOME'):
        ExecCommand("PIC")
        NoOfRownds = 200
        while NoOfRownds>0:
            NoOfRownds = NoOfRownds - 1
            x = random.randint(1,4)
            print("x = " + str(x))
            if(x == 1):
                if(usDistance.UltraDistance < 0.18):
                    print("Bump stop")
                    continue
                ExecCommand("B")
                ExecCommand("W")
                ExecCommand("S")
                ExecCommand("PIC")
            elif(x == 2):
                ExecCommand("F")
                ExecCommand("W")
                ExecCommand("S")
                ExecCommand("PIC")
            elif(x == 3):
                ExecCommand("L")
                ExecCommand("W")
                ExecCommand("S")
                ExecCommand("PIC")
            elif(x == 4):
                ExecCommand("R")
                ExecCommand("W")
                ExecCommand("S")
                ExecCommand("PIC")
    elif(user_command.upper() == 'HUNT2' or user_command.upper() == 'HUNTER2'):

        NO_OF_SEARCHTURNS_ALLOWED = 5
        while(NO_OF_SEARCHTURNS_ALLOWED > 0):
            imagename = camera.fastPic()
            #res = HunterAI.Descision(imagename)
            boxes = AITensorflow.generateboxes(imagename)

            #AimingFor = (60,300)
            closestbox = None
            mindiffy = 10000
            for box in boxes:
                diffy = box[0]-60
                if(diffy < mindiffy):
                    mindiffy = diffy
                    closestbox = box
            if(closestbox is not None):
                if(closestbox[0] < 60):
                    if(usDistance.UltraDistance < 0.18):
                        print("Bump stop")
                        NO_OF_SEARCHTURNS_ALLOWED = NO_OF_SEARCHTURNS_ALLOWED - 1
                        continue
                    print("Ultrasound Distance = " +str(usDistance.UltraDistance))
                    print("forward adjust")
                    ExecCommand("F")
                    ExecCommand("W")
                    ExecCommand("S")
                elif(closestbox[1] < 300):
                    print("left adjust")
                    ExecCommand("R")
                    ExecCommand("W")
                    ExecCommand("S")
                else:
                    print("Perfect spot")
                    break
            else:
                print("left searching")
                ExecCommand("L")
                ExecCommand("W")
                ExecCommand("S")
                NO_OF_SEARCHTURNS_ALLOWED = NO_OF_SEARCHTURNS_ALLOWED - 1
    elif(user_command.upper() == 'HUNT' or user_command.upper() == 'HUNTER'):
        NO_OF_SEARCHTURNS_ALLOWED = 5
        while(NO_OF_SEARCHTURNS_ALLOWED > 0):
            imagename = camera.takePicture()
            res = HunterAI.Descision(imagename)
            if(res == "grab"):
                print("grabbing")
                ardy.MoveServo('4', 170)
                break
            elif (res == "left"):
                print("left")
                ExecCommand("L")
                ExecCommand("W")
                ExecCommand("S")
            elif (res == "forward"):
                print("forward")
                ExecCommand("F")
                ExecCommand("W")
                ExecCommand("S")
            elif (res == "Did not find anything"):
                print("left searching")
                ExecCommand("L")
                ExecCommand("W")
                ExecCommand("S")
                NO_OF_SEARCHTURNS_ALLOWED = NO_OF_SEARCHTURNS_ALLOWED - 1
    elif(user_command.upper() == 'THUNT' or user_command.upper() == 'THUNTER'):
        imagename = camera.takePicture()
        res = HunterAI.Descision(imagename)
        print(res)
    elif(user_command.upper() == 'CANNY'):
        imagename = camera.takePicture()
        HunterAI.SaveCannyMask(imagename)

LoopNo = 40
try:
    while(LoopNo>0):
        print(LoopNo)
        LoopNo=LoopNo-1

        use_command_line = input("Your command:")
        user_commands = use_command_line.split(' ')
        #print(user_commands)

        for user_command in user_commands:
            print("user_command : " + user_command)
            if(user_command.upper() == 'Q'):
                LoopNo=0
                break
            ExecCommand(user_command)
        ExecCommand("S") #because I forget
finally:
    usDistance.StopMeasuring()
    engines.cleanup()
    ardy.cleanup()
    time.sleep(0.8)
    gpio.cleanup() # this ensures a clean exit