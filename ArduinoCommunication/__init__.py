import serial
import time

serialport = "/dev/ttyACM0" #"COM3"
ser = serial.Serial(serialport, 9800, timeout=1)

##ser.close()


class ArduinoCommunication:
    def printServoLocations(self):
        ser.write(b'g')
        time.sleep(0.5)
        Line = ser.readline()
        print(Line)

    def MoveServo(self, ServoNo, Angle):
        ser.write(b's')
        ser.write(ServoNo)
        ser.write(bytes([Angle])[0])
        time.sleep(0.5)
        return ser.readline()
    def cleanup(self):
        ser.close()