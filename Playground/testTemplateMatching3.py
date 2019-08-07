#Matches multiple images
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

ContoursDir = "E:\\R2D2\\images\\ToTest\\Contours"
StrumpaDir = "E:\\R2D2\\images\\ToTest\\Strumpa"

NoStrumpaDirCanny = "E:\\R2D2\\images\\ToTest\\IngenStrumpaCanny"
StrumpaDirCanny = "E:\\R2D2\\images\\ToTest\\StrumpaCanny"

TemplateDir = "E:\\R2D2\\images\\ToTest\\ToMatch"

imgScale = 0.5

dir_name = ContoursDir
directory = os.fsencode(dir_name)
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

def match(directory, templates):
    ImageGenMatches = {}
    for template,w, h, filename in templates:
        ImageGenMatches[filename] = 0
    
    NoMatch = 0
    totNo = 0
    for file in os.listdir(directory):
        totNo = totNo + 1
        filename = directory + "\\" + os.fsdecode(file)
        image = cv2.imread(filename)
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        newX,newY = img_gray.shape[1]*imgScale, img_gray.shape[0]*imgScale
        newimg = cv2.resize(img_gray,(int(newX),int(newY)))
        img_gray = newimg
        for template,w, h, filename in templates:
            #template = cv2.imread("E:\\R2D2\\images\\ToTest\\ma.png",0)
            #w, h = template.shape[::-1]
            res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
            threshold = 0.48
            loc = np.where( res >= threshold)
            found = False
            for pt in zip(*loc[::-1]):
                found= True
                NoMatch = NoMatch + 1
                ImageGenMatches[filename] = ImageGenMatches[filename] + 1
                break
            if(found):
                break
    return NoMatch, totNo, ImageGenMatches
    
NoCorrectlyMatched, totThatShouldHaveBeenMatched, ImageGenMatches = match(StrumpaDirCanny, templates)
print("NoCorrectlyMatched = " + str(NoCorrectlyMatched) + " / " + str(totThatShouldHaveBeenMatched))
IncorrectlyMatched, totThatShouldNotHaveBeenMatched, ImageGenMatches2 = match(NoStrumpaDirCanny, templates)
print("IncorrectlyMatched = " + str(IncorrectlyMatched) + " / " + str(totThatShouldNotHaveBeenMatched))

print("Done")