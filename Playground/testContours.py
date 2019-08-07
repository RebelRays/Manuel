#Doesn't do what I want it todo which is to group the object totgather
#Result similar to lines

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

ContoursDir = "E:\\R2D2\\images\\ToTest\\Contours"
StrumpaDir = "E:\\R2D2\\images\\ToTest\\Strumpa"

dir_name = ContoursDir
directory = os.fsencode(dir_name)
x=[]
y = []
for file in os.listdir(directory):
    filename = dir_name + "\\" + os.fsdecode(file)
    image = cv2.imread(filename)

    im = cv2.imread(filename)
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print("No of shapes = " + str(len(contours)))
    cv2.drawContours(im, contours, -1, (0,255,0), 3)
    plt.imshow(im)
    plt.show()

    for cnt in contours:
        rect2 = cv2.boundingRect(cnt)
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        img2 = cv2.drawContours(imgray, [box], 0, (0,255,0), 30)
        plt.imshow(img2)
        plt.show()
    

print("Done")