from picamera import PiCamera
from time import sleep
from datetime import datetime

pi_camera = PiCamera()
class CameraHandler:
    todo=1

    def takePicture(self):
        pi_camera.resolution = (64, 64)
        now_Str = datetime.today().strftime('%Y%m%d-%H%M%S')
        pi_camera.capture('/DataRecording/Images/%s.png' % now_Str)
        pi_camera.close()
    
    
