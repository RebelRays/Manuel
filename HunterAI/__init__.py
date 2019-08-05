import cv2
import numpy as np
import matplotlib.pyplot as plt

import os

def GetCannyMask(working_image):
    height = working_image.shape[0]
    down_regions = np.array([[(0, height), (0,210), (620,225), (620,height)]])
    
    grayImage=cv2.cvtColor(working_image, cv2.COLOR_RGB2GRAY)
    blurImage = cv2.GaussianBlur(grayImage, (5,5), 0)
    cannyImage=cv2.Canny(blurImage, 50, 100)

    region_of_floor = np.zeros_like(cannyImage)
    cv2.fillPoly(region_of_floor, down_regions, 255)
    masked_image = cv2.bitwise_and(cannyImage, region_of_floor)
    return masked_image

def Coordinates(filename):
    image = cv2.imread(filename)
    cannymask = GetCannyMask(image)
        
    treshold = 2
    lines=cv2.HoughLinesP(cannymask, 2, np.pi/180, treshold, np.array([]), minLineLength=4, maxLineGap=5)
    combined_x=0
    combined_y= 0
    if lines is not None:
        no_of_lines = len(lines)
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            #for x1, y1, x2, y2 in lines:
            cv2.line(image, (x1,y1), (x2,y2), (255,0,0), 10)
            middle_x = (x1+x2)/2.0
            middle_y= (y1+y2)/2-0
            combined_x = combined_x + middle_x/no_of_lines
            combined_y = combined_y + middle_y/no_of_lines
    return combined_x, combined_y

def Descision(filename):
    combined_x, combined_y = Coordinates(filename)
    print("combined_x = " + str(combined_x) + " combined_y " + str(combined_y))
    if(combined_x == 0 or combined_y == 0):
        #Did not find anything
        return "Did not find anything"
    if(combined_x < 290):
        return "left"
    if(combined_y <325):
        return "forward"
    return "grab"