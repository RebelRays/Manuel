#Matches multiple images
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from datetime import datetime

def getLines(cannymask):
    treshold = 30
    lines=cv2.HoughLinesP(cannymask, 3, np.pi/180, treshold, np.array([]), minLineLength=6, maxLineGap=15)
    return lines

def lineDistance(line1, line2):
    l1_x1, l1_y1, l1_x2, l1_y2 = line1.reshape(4)
    l2_x1, l2_y1, l2_x2, l2_y2 = line2.reshape(4)

    l1_middle_x = (l1_x1+l1_x2)/2.0
    l1_middle_y= (l1_y1+l1_y2)/2-0

    l2_middle_x = (l2_x1+l2_x2)/2.0
    l2_middle_y= (l2_y1+l2_y2)/2-0
    return math.sqrt((l2_middle_x - l1_middle_x)**2 +(l1_middle_y - l2_middle_y)**2 )

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

def GetCannyMask(working_image):
    height = working_image.shape[0]
    down_regions = np.array([[(0, height), (0,230), (640,245), (640,height)]])
    
    grayImage=cv2.cvtColor(working_image, cv2.COLOR_RGB2GRAY)
    blurImage = cv2.GaussianBlur(grayImage, (5,5), 0)
    cannyImage=cv2.Canny(blurImage, 20, 60)

    cropped_image = cannyImage[200:,:]

    #region_of_floor = np.zeros_like(cannyImage)
    #cv2.fillPoly(region_of_floor, down_regions, 255)
    #masked_image = cannyImage #cv2.bitwise_and(cannyImage, region_of_floor)
    return cropped_image

def distanceFromCenter(line, combined_x, combined_y):
    x1, y1, x2, y2 = line.reshape(4)
    middle_x = (x1+x2)/2.0
    middle_y= (y1+y2)/2-0
    average = math.sqrt((combined_x - middle_x)**2 +(combined_y - middle_y)**2 )
    linelength = math.sqrt((x1 - x2)**2 +(y1 - y2)**2 )
    return average, linelength

#TemplateDir = "E:\\R2D2\\images\\ToTest\\ToMatch"
TemplateDir = "E:\\R2D2\\images\\Crop\\ImagesToCrop"
SubpartsDir = "E:\\R2D2\\images\\Crop\\Subparts"

imgScale = 1

templates = []
for file in os.listdir(TemplateDir):
    filename = TemplateDir + "\\" + os.fsdecode(file)
    original = cv2.imread(filename)
    #plt.text("Original")
    #plt.imshow(original)
    #plt.show()
    #newX,newY = original.shape[1]*imgScale, original.shape[0]*imgScale
    #newimg = cv2.resize(original,(int(newX),int(newY)))
    cannymask = GetCannyMask(original)
    #height, width = template.shape
    #newX,newY = template.shape[1]*imgScale, template.shape[0]*imgScale
    #newimg = cv2.resize(template,(int(newX),int(newY)))
    #plt.imshow(cannymask)
    #plt.show()
    #resized_template = cv2.resize(template, (width/,64), interpolation = cv2.INTER_AREA)

    w, h = cannymask.shape[::-1]
    templates.append([cannymask, w, h, file, original])

for template,w, h, filename, original in templates:
    lines = getLines(template)

    img = np.copy(template)
    #cv2.imshow("original", original)
    #cv2.waitKey(0)
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        cv2.line(img, (x1,y1), (x2,y2), (126,126,255), 8)
    #cv2.imshow("lines", img)
    #cv2.waitKey(0)
    no_of_lines = len(lines)
    print("no_of_lines = " + str(no_of_lines))
    #Calc distance to other lines to determin how many are within reac
    LinesThatCanBePared = list(range(no_of_lines))

    MinlinesToConstruct = 25
    MaxDistance = 75
    Clusters = []
    while(len(LinesThatCanBePared) > MinlinesToConstruct):
        currentLineNo = LinesThatCanBePared[0]
        #Calc distance between all lines and pic out the one that reaches the most -> take out

        centerpoint=-1
        currentBiggestCluster = []
        for l1 in LinesThatCanBePared:
            potentialCluster = []
            for l2 in LinesThatCanBePared:
                if(l1 != l2):
                    line1 = lines[l1]
                    line2 = lines[l2]
                    
                    distance = lineDistance(line1, line2)
                    if(distance < MaxDistance):
                        #print(str(l1) + " -> " + str(l2) + " = " + str(distance))
                        potentialCluster.append(l2)

                        #img = np.copy(template)
                        #x1, y1, x2, y2 = line1.reshape(4)
                        #cv2.line(img, (x1,y1), (x2,y2), (80,126,126), 4)
                        #cv2.imshow("p1: lines " + str(l1) + " -> " + str(l2) + " = " + str(distance), img)
                        #cv2.waitKey(0)

                        #x1, y1, x2, y2 = line2.reshape(4)
                        #cv2.line(img, (x1,y1), (x2,y2), (126,126,255), 4)
                        #cv2.imshow("lines " + str(l1) + " -> " + str(l2) + " = " + str(distance), img)
                        #cv2.waitKey(0)

            if(len(potentialCluster)> len(currentBiggestCluster)):
                print("Found Clustrt size " + str(len(potentialCluster)) + " centerpoint = " + str(l1))
                currentBiggestCluster=potentialCluster
                currentBiggestCluster.append(l1)
                centerpoint=l1
        if (len(currentBiggestCluster)<MinlinesToConstruct):
            print("Reached min")
            break
        else:
            print("Adding Cluster with size " + str(len(currentBiggestCluster)))
            #img = np.copy(template)
            Clusters.append(currentBiggestCluster)
            for lineno in currentBiggestCluster:
                #l1 = lines[lineno]
                #x1, y1, x2, y2 = l1.reshape(4)
                #cv2.line(img, (x1,y1), (x2,y2), (126,126,255), 8)
                LinesThatCanBePared.remove(lineno)
            print("No of LinesThatCanBePared left = " + str(len(LinesThatCanBePared)))
            #plt.imshow(img)
            #plt.show()

    print(filename + " No of clusters found = " + str(len(Clusters)))
    img = np.copy(template)
    #plt.imshow(img)
    #plt.show()

    colorshift = 0
    now_Str = datetime.today().strftime('%Y%m%d-%H%M%S')
    clusterno = 0
    for Cluster in Clusters:
        clusterno = clusterno +1
        img = np.copy(template)
        colorshift = 120 #colorshift + 120 #250/len(Clusters)

        min_x = 10000
        min_y=100000
        max_x = 0
        max_y=0

        #cv2.line(img, (0,220), (640,220), (210, 180, 222), 4)
        for lineno in Cluster:
            
            l1 = lines[lineno]
            x1, y1, x2, y2 = l1.reshape(4)
            #print("drawing lineno " + str(lineno) + " x1 = " + str(x1) + " y1= " + str(y1) + " x2 = " + str(x2)  + " y2 = " + str(y2))
            cv2.line(img, (x1,y1), (x2,y2), (colorshift,126,255), 4)
            min_x = min(min_x, x1, x2)
            min_y = min(min_y, y1, y2)
            max_x = max(max_x, x1, x2)
            max_y = max(max_y, y1, y2)

            cv2.rectangle(img, (min_x, min_y), (max_x, max_y), (255, 255, 00), 2)
            #cv2.line(img, (min_x,min_y), (max_x,min_y), (148,126,122), 1)

            #max length of box?
            

        #plt.imshow(img)
        #plt.show()

        min_y = min_y +200 #Crop compesation
        max_y = max_y +200 
        pic_width, pic_height = cannymask.shape[::-1]
        pic_height=pic_height+200
        min_x = max(0, min_x-5)
        min_y = max(0, min_y-5)
        max_x = min(pic_width, max_x+5)
        max_y = min(pic_height, max_y+5)
        cropped_image = original[min_y:max_y, min_x:max_x]
        #plt.imshow(cropped_image)
        #plt.show()
        cropped_filename = SubpartsDir + "\\" + filename.split('.')[0] + "_" + str(clusterno) + ".png"
        print(cropped_filename)
        cv2.imwrite(cropped_filename, cropped_image)
    #print(filename + " totAverageDistance " + str(totAverageDistance) + " totAverageRatio " + str(totAverageRatio) + " totAverageLineLenght " + str(totAverageLineLenght)+ " no_of_lines " + str(no_of_lines))

print("Done")