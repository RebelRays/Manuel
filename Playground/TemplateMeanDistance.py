#Matches multiple images
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math




def getLines(cannymask):
    treshold = 2
    lines=cv2.HoughLinesP(cannymask, 2, np.pi/180, treshold, np.array([]), minLineLength=4, maxLineGap=5)
    return lines

def getCenter(lines):
    combined_x=0
    combined_y= 0
    no_of_lines= 0
    if lines is not None:
        no_of_lines = len(lines)
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            #for x1, y1, x2, y2 in lines:
            #cv2.line(image, (x1,y1), (x2,y2), (255,0,0), 2)
            middle_x = (x1+x2)/2.0
            middle_y= (y1+y2)/2-0
            combined_x = combined_x + middle_x/no_of_lines
            combined_y = combined_y + middle_y/no_of_lines
    #print("combined_x " + str(combined_x) + " combined_y " + str(combined_y) + " no_of_lines: " + str(no_of_lines))
    return combined_x, combined_y, no_of_lines

def distanceFromCenter(line, combined_x, combined_y):
    x1, y1, x2, y2 = line.reshape(4)
    middle_x = (x1+x2)/2.0
    middle_y= (y1+y2)/2-0
    average = math.sqrt((combined_x - middle_x)**2 +(combined_y - middle_y)**2 )
    linelength = math.sqrt((x1 - x2)**2 +(y1 - y2)**2 )
    return average, linelength

#TemplateDir = "E:\\R2D2\\images\\ToTest\\ToMatch"
TemplateDir = "E:\\R2D2\\images\\ToTest\\ClusterTest"

imgScale = 1

templates = []
for file in os.listdir(TemplateDir):
    filename = TemplateDir + "\\" + os.fsdecode(file)
    template = cv2.imread(filename,0)

    #height, width = template.shape
    newX,newY = template.shape[1]*imgScale, template.shape[0]*imgScale

    newimg = cv2.resize(template,(int(newX),int(newY)))
    #resized_template = cv2.resize(template, (width/,64), interpolation = cv2.INTER_AREA)
    w, h = newimg.shape[::-1]
    templates.append([newimg, w, h, file])

for template,w, h, filename in templates:
    lines = getLines(template)
    combined_x, combined_y, no_of_lines = getCenter(lines)
    
    totAverageRatio = 0
    totAverageDistance = 0
    totAverageLineLenght = 0
    no_of_lines = len(lines)
    for line in lines:

        distance, linelength = distanceFromCenter(line, combined_x, combined_y)
        totAverageLineLenght = totAverageLineLenght + linelength/no_of_lines
        totAverageDistance = totAverageDistance + distance/no_of_lines
        totAverageRatio = totAverageRatio + (distance/linelength)/no_of_lines
        #print(filename + " distance " + str(distance) + " ratio " + str(distance/linelength))
    print(filename + " totAverageDistance " + str(totAverageDistance) + " totAverageRatio " + str(totAverageRatio) + " totAverageLineLenght " + str(totAverageLineLenght)+ " no_of_lines " + str(no_of_lines))

print("Done")