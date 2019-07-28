import RPi.GPIO as gpio
import time
from threading import Timer

gpio.setmode(gpio.BCM)

class UltraSoundHandler:
    UltraDistance=100
    ECHO_PIN=-1
    TRIG_PIN=-1
    def StartMeasuring(self):
        t = Timer(0.001, self.LoopUltraSound)
        t.start()
        return

    def LoopUltraSound(self):
        while True:
            #print("Will call getUltaSoundDistance")
            self.UltraDistance = self.getUltaSoundDistance()
            #print("UltraDistance = " + str(self.UltraDistance))
            time.sleep(0.09)
    def getUltaSoundDistance(self):
        gpio.output(self.TRIG_PIN, True)
        time.sleep(0.00001)
        gpio.output(self.TRIG_PIN, False)
        while gpio.input(self.ECHO_PIN) == 0:
            pass
        start = time.time()
        while gpio.input(self.ECHO_PIN) == 1:
            pass
        stop = time.time()
        distance = (stop-start)*170
        return  distance;