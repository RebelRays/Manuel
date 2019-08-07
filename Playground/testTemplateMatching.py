#Mathes an image with another
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
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template = cv2.imread("E:\\R2D2\\images\\ToTest\\ma.png",0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
            cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            cv2.imwrite('res.png',image)

    plt.imshow(image)
    plt.show()

print("Done")