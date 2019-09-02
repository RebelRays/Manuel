import tensorflow as tf
import numpy as np
from tensorflow import keras
import os
import cv2
import matplotlib.pyplot as plt

model = None
TemplateDir = "E:\\R2D2\\images\\AllImagesTo_120_160"
SubpartsDir = "E:\\R2D2\\images\\120_160_Images"

ImageSubfolder = SubpartsDir
#SubpartsDir = "E:\\R2D2\\images\\Crop\\Subparts"
def generateboxes(ImageFileName):
    boxesContainingSock = []
    original = cv2.imread(ImageFileName)
    justthefilename = ImageFileName.split('\\')[-1]
    justthefilename  = justthefilename.split('.')[0]
    print("justthefilename " + justthefilename)

    cropped_image = original.copy() #[cropped_from:,:]
    ch,w, h = cropped_image.shape[::-1]

    size_x = 160
    size_y = 120
    delta = 20
    boxno=0
    current_y = 0
    current_x = 0
    #justthefilename = "foo"
    while current_y+delta+size_y <= h:
        current_x=0
        while current_x+delta+size_x <= w:
            boxno = boxno +1
            cropped_image = original[current_y:current_y+size_y, current_x:current_x+size_x]
            
            newfilename = ImageSubfolder + "\\" + justthefilename + "_" + str(current_y) + "_" + str(current_x) + ".png"
            
            cv2.imwrite(newfilename, cropped_image)
            current_x = current_x + delta
        current_y = current_y + delta
    

for file in os.listdir(TemplateDir):
    filename = TemplateDir + "\\" + os.fsdecode(file)
    generateboxes(filename)