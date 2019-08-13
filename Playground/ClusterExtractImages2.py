#Matches multiple images
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from datetime import datetime

#TemplateDir = "E:\\R2D2\\images\\ToTest\\ToMatch"
TemplateDir = "E:\\R2D2\\images\\Crop\\ImagesToCrop"
SubpartsDir = "E:\\R2D2\\images\\Crop\\Subparts"

imgScale = 1

templates = []
for file in os.listdir(TemplateDir):
    filename = TemplateDir + "\\" + os.fsdecode(file)
    original = cv2.imread(filename)

    cropped_image = original[200:,:]
    ch,w, h = cropped_image.shape[::-1]
    current_h = 0
    size = 240
    delta = 20
    boxno=0
    while current_h+delta+size <= h:
        current_w = 0
        while current_w+delta+size <= w:
            boxno = boxno +1
            cropped_image = original[current_h+200:current_h+200+size, current_w:current_w+200]
            cropped_filename = SubpartsDir + "\\" + os.fsdecode(file).split('.')[0] + "_" + str(boxno) + ".png"
            cv2.imwrite(cropped_filename, cropped_image)
            current_w = current_w + delta
        current_h = current_h + delta

print("Done")