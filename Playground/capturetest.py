from picamera import PiCamera
from time import sleep
from datetime import datetime
from fractions import Fraction
from PIL import Image
import numpy as np

cam = PiCamera()
try:
    
    cam.resolution = (640,480)
    cam.rotation = 180

    cam.framerate=Fraction(1, 2)
    cam.shutter_speed = 2000000

    print(str(cam.shutter_speed))
    cam.start_preview()
    sleep(2)
    print("Capturing")
    cam.capture("imagename.png")
    print("Done Capturing")
    im = Image.open("imagename.png")
    brightness = np.mean(im)
    print("brightness = " + str(brightness))
finally:
    cam.close()