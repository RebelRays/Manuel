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
        time.sleep(.5)
        #Line = ser.readlines()
        #print(Line)

    def MoveServo(self, ServoNo, Angle):
        ser.write(b's')
        #print("Sending ServoNo")
        #print(ServoNo)
        ser.write(bytes([int(ServoNo)]))
        #print("Sending Angle")
        #print(Angle)
        #print("encoded to")
        bangle = bytes([Angle])
        #print(bangle)
        ser.write(bangle)
        time.sleep(0.5)
        #return ser.readline()
    def printAll(self):
        while ser.in_waiting > 0:
            print(ser.readline())
    def pingArdy(self):
        print("Ping Ardy")
        ser.write(b'p')
        time.sleep(1)
        #print(ser.readlines())
    def printLastCommand(self):
        print("getLastCommand")
        ser.write(b'r')
        time.sleep(0.5)
        #print(ser.readlines())
    def cleanup(self):
        print("ArduinoCommunication -> Cleanup")
        ser.close()