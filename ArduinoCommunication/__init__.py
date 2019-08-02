import serial
import time

serialport = "/dev/ttyACM0" #"COM3"


try: 
    ser = serial.Serial(serialport, 9800, timeout=1)
except: 
    ser = serial.Serial("/dev/ttyACM1", 9800, timeout=1)

##ser.close()


class ArduinoCommunication:
    def printServoLocations(self):
        ser.write(b'g')
        #time.sleep(.5)
        #Line = ser.readlines()
        #print(Line)

    #ardy.MoveServo('2',10)
    def MoveServo(self, ServoNo, Angle):
        ser.writelines
        ser.write(b's')
        servoStr = ServoNo.encode('ascii')
        print("Servo")
        print(servoStr)
        ser.write(servoStr)
        AngleString = str(Angle).encode('ascii')
        i = 0
        print("Sending Angle")
        if(Angle<100):
            print(b'0')
            ser.write(b'0')
        else:
            ser.write(b'1')
            print(b'1')
            i=i+1
        
        if(Angle<10):
            print(b'0')
            ser.write(b'0')
        else:
            angle2 = chr(AngleString[i]).encode('ascii')
            ser.write(angle2)
            print(angle2)
            i=i+1

        ser.write(chr(AngleString[i].encode('ascii')))
        print(chr(AngleString[i].encode('ascii')))
        #time.sleep(0.5)
        #return ser.readline()
    def MoveServo2(self, ServoNo, Angle):
        ser.writelines
        ser.write(b's')
        servoStr = ServoNo.encode('ascii')
        print("Servo")
        print(servoStr)
        ser.write(servoStr)
        AngleString = str(Angle).encode('ascii')
        i = 0
        print("Sending Angle")
        if(Angle<100):
            print(b'0')
            ser.write(b'0')
        else:
            ser.write(AngleString[i])
            print(AngleString[i])
            i=i+1
        
        if(Angle<10):
            print(b'0')
            ser.write(b'0')
        else:
            ser.write(AngleString[i])
            print(AngleString[i])
            i=i+1

        ser.write(AngleString[i])
        print(AngleString[i])
        #time.sleep(0.5)
        #return ser.readline()
    def printAll(self):
        while ser.in_waiting > 0:
            print(ser.readline())
    def pingArdy(self):
        print("Ping Ardy")
        ser.write(b'p')
        #time.sleep(1)
        #print(ser.readlines())
    def printLastCommand(self):
        print("getLastCommand")
        ser.write(b'r')
        #time.sleep(0.5)
        #print(ser.readlines())
    def cleanup(self):
        print("ArduinoCommunication -> Cleanup")
        ser.close()
    
ardy = ArduinoCommunication()
print("Ready")