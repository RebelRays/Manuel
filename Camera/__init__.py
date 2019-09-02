from picamera import PiCamera
from time import sleep
from datetime import datetime
from fractions import Fraction

makeBrighter= False

cam = None
class CameraHandler:

    def makeBrighter2(self):
        global cam
        cam.framerate=Fraction(1, 6)
        cam.shutter_speed=2000000
        cam.iso = 800
    def makeBrighter(self):
        global makeBrighter
        makeBrighter = True
        #cam.iso = 800
    def resetExposure(self):
        global cam
        cam.iso = 0
        cam.shutter_speed=0
    def initFastPic(self):
        global cam
        global makeBrighter
        if(cam is None):
            cam = PiCamera()
            cam.resolution = (640,480)
            cam.rotation = 180
            cam.start_preview()
            sleep(2)
            if(makeBrighter):
                print("Bright pic")
                #cam.iso=800
                cam.shutter_speed = 3000000
                print(str(cam.shutter_speed))
                cam.framerate=1/3.0
                cam.shutter_speed = 3000000
                print(str(cam.shutter_speed))
                #cam.exposure_mode = 'off'
                #cam.iso = 800
                #cam.awb_mode = 'off'


    def closeCamera(self):
        global cam
        if(cam is not None):
            cam.close()
            cam = None
        
    def fastPic(self):
        if(cam is None):
            self.initFastPic()
        
        now_Str = datetime.today().strftime('%Y%m%d-%H%M%S')
        imagename = './DataRecording/Images/' + now_Str + ".png"
        cam.capture(imagename)
        return imagename
    
    def takePicture(self):
        if(cam is not None):
            pi_camera = cam
        else:
            pi_camera = PiCamera()
            pi_camera.resolution = (640,480)
            pi_camera.rotation = 180
            pi_camera.start_preview()
            sleep(2)
        try:
            now_Str = datetime.today().strftime('%Y%m%d-%H%M%S')
            #pi_camera.capture('./DataRecording/Images/%s.png' % now_Str)
            imagename = './DataRecording/Images/' + now_Str + ".png"
            pi_camera.capture(imagename)
            return imagename
        finally:
            pi_camera.close()
    
    
