from picamera import PiCamera
from time import sleep
from datetime import datetime


class CameraHandler:
    todo=1

    def takePicture(self):
        pi_camera = PiCamera()
        try:
            pi_camera.resolution = (1640,1232)
            now_Str = datetime.today().strftime('%Y%m%d-%H%M%S')
            sleep(2)
            pi_camera.capture('./DataRecording/Images/%s.png' % now_Str)
        finally:
            pi_camera.close()
    
    
