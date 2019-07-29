import serial
import time

serialport = "/dev/ttyACM1" #"COM3"
ser = serial.Serial(serialport, 9800, timeout=1)

##ser.close()


class ArduinoCommunication:
    def printServoLocations(self):
        ser.write(b'g')
        time.sleep(1)
        Line = ser.readlines()
        print(Line)

    def MoveServo(self, ServoNo, Angle):
        ser.write(b's')
        print("Sending ServoNo")
        print(ServoNo)
        ser.write(ServoNo)
        print("Sending Angle")
        bangle = (bytes([Angle])[0])
        print(bangle)
        ser.write(bangle)
        time.sleep(1)
        return ser.readline()
    def printAll(self):
        if ser.in_waiting > 0:
            print(ser.readlines())
    def pingArdy(self):
        print("Ping Ardy")
        ser.write(b'p')
        time.sleep(1)
        print(ser.readlines())
    def printLastCommand(self):
        print("getLastCommand")
        ser.write(b'r')
        time.sleep(1)
        print(ser.readlines())
    def cleanup(self):
        print("ArduinoCommunication -> Cleanup")
        ser.close()