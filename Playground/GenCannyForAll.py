
import os
import numpy as np
import cv2
def GetCannyMask(working_image):
    height = working_image.shape[0]
    down_regions = np.array([[(0, height), (0,210), (620,225), (620,height)]])
    
    grayImage=cv2.cvtColor(working_image, cv2.COLOR_RGB2GRAY)
    blurImage = cv2.GaussianBlur(grayImage, (5,5), 0)
    cannyImage=cv2.Canny(blurImage, 20, 60)

    region_of_floor = np.zeros_like(cannyImage)
    cv2.fillPoly(region_of_floor, down_regions, 255)
    masked_image = cannyImage #cv2.bitwise_and(cannyImage, region_of_floor)
    return masked_image

def SaveCannyMask(filename, savefilename):
    
    image = cv2.imread(filename)
    cannymask = GetCannyMask(image)
        
    treshold = 2
    lines=cv2.HoughLinesP(cannymask, 2, np.pi/180, treshold, np.array([]), minLineLength=9, maxLineGap=5)
    combined_x=0
    combined_y= 0
    no_of_lines= 0
    if lines is not None:
        no_of_lines = len(lines)
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            #for x1, y1, x2, y2 in lines:
            cv2.line(image, (x1,y1), (x2,y2), (255,0,0), 2)
            middle_x = (x1+x2)/2.0
            middle_y= (y1+y2)/2-0
            combined_x = combined_x + middle_x/no_of_lines
            combined_y = combined_y + middle_y/no_of_lines
    cv2.imwrite(savefilename, cannymask)

NoStrumpaDir = "E:\\R2D2\\images\\ToTest\\IngenStrumpa"
StrumpaDir = "E:\\R2D2\\images\\ToTest\\Strumpa"
StrumpaDir = "E:\\R2D2\\images\\ToTest\\NewTest"

NoStrumpaDirCanny = "E:\\R2D2\\images\\ToTest\\IngenStrumpaCanny"
StrumpaDirCanny = "E:\\R2D2\\images\\ToTest\\StrumpaCanny"

dir_name = NoStrumpaDir
save_dir_name = NoStrumpaDirCanny
directory = os.fsencode(dir_name)
for file in os.listdir(directory):
    filename = dir_name + "\\" + os.fsdecode(file)
    savefilename = save_dir_name + "\\" + os.fsdecode(file)
    SaveCannyMask(filename, savefilename)

dir_name = StrumpaDir
save_dir_name = StrumpaDirCanny
directory = os.fsencode(dir_name)
for file in os.listdir(directory):
    filename = dir_name + "\\" + os.fsdecode(file)
    savefilename = save_dir_name + "\\" + os.fsdecode(file)
    SaveCannyMask(filename, savefilename)