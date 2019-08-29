import tensorflow as tf
import numpy as np
from tensorflow import keras
import os
import cv2
import matplotlib.pyplot as plt

model = None
modelInputDim = (120,120)
def load_model():
    global model
    global modelInputDim
    model2 = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(60, (3, 3), activation='relu', input_shape=(120, 120,3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(15, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    #tf.keras.layers.Conv2D(12, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dropout(0.4),
    #tf.keras.layers.Dense(2, activation='sigmoid')
    tf.keras.layers.Dense(2, activation='softmax')
    ])

    modelfile= "tensormodel/cp-05-0025.ckpt"
    model2.load_weights(modelfile)
    model = model2
    modelInputDim = (120,120)

def load_model2():
    global model
    global modelInputDim
    model2 = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(40, (3, 3), activation='relu', input_shape=(60,60, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Dropout(0.05),
    tf.keras.layers.Conv2D(20, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    #tf.keras.layers.Conv2D(12, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    #tf.keras.layers.Dense(2, activation='sigmoid')
    tf.keras.layers.Dense(2, activation='softmax')
    ])

    modelfile= "tensormodel/cp_60-60_40-d-20-001_0050.ckpt"
    model2.load_weights(modelfile)
    model = model2
    modelInputDim = (60,60)

def load_model5():
    global model
    global modelInputDim

    #model2 =tf.keras.models.load_model("tensormodel/best")
    model2 = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(44, (3, 3), activation='relu', input_shape=(60,60, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Dropout(0.04),
    tf.keras.layers.Conv2D(26, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    #tf.keras.layers.Conv2D(12, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    #tf.keras.layers.Dense(2, activation='sigmoid')
    tf.keras.layers.Dense(2, activation='softmax')
    ])
    
    
    modelfile= "tensormodel/cp_60-60_44-d-26-003_0061.ckpt"
    model2.load_weights(modelfile)
    model = model2
    modelInputDim = (60,60)

def load_model4():
    global model
    global modelInputDim

    #model2 =tf.keras.models.load_model("tensormodel/best")
    model2 = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(42, (3, 3), activation='relu', input_shape=(60,60, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Dropout(0.04),
    tf.keras.layers.Conv2D(24, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    #tf.keras.layers.Conv2D(12, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    #tf.keras.layers.Dense(2, activation='sigmoid')
    tf.keras.layers.Dense(2, activation='softmax')
    ])
    
    
    modelfile= "tensormodel/cp_60-60_40-d-20-004_0072.ckpt"
    model2.load_weights(modelfile)
    model = model2
    modelInputDim = (60,60)

def load_model3():
    global model
    global modelInputDim
    model2 = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(42, (3, 3), activation='relu', input_shape=(60,60, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Dropout(0.04),
    tf.keras.layers.Conv2D(24, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    #tf.keras.layers.Conv2D(12, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    #tf.keras.layers.Dense(2, activation='sigmoid')
    tf.keras.layers.Dense(2, activation='softmax')
    ])

    modelfile= "tensormodel/cp_exp_60-60_40-d-20-002_0070.ckpt"
    model2.load_weights(modelfile)
    model = model2
    modelInputDim = (60,60)

def getNotSockOrSock(image):
    if(model is None):
        load_model()
    resized = cv2.resize(image, modelInputDim)
    resized = resized/255
    prediction = model.predict(np.array([resized]))
    result = np.argmax(prediction[0])
    return result

ImageSubfolder = "./DataRecording/Images"
SubpartsDir = "E:\\R2D2\\images\\Crop\\Subparts"
def generateboxes(ImageFileName):
    boxesContainingSock = []
    original = cv2.imread(ImageFileName)
    justthefilename = ImageFileName.split('/')[-1]
    justthefilename  = justthefilename.split('.')[0]
    print("justthefilename " + justthefilename)
    cropped_from = 50
    cropped_image = original[cropped_from:,:]
    ch,w, h = cropped_image.shape[::-1]
    current_h = 0
    size = 240
    delta = 60
    boxno=0
    #justthefilename = "foo"
    while current_h+delta+size <= h:
        current_w = 0
        while current_w+delta+size <= w:
            boxno = boxno +1
            cropped_image = original[current_h+cropped_from:current_h+cropped_from+size, current_w:current_w+size]
            #plt.imshow(cropped_image)
            #plt.show()

            result = getNotSockOrSock(cropped_image)
            newfilename = ImageSubfolder + "/" + "NotSock" + "/" + justthefilename + "_" + str(current_h) + "_" + str(current_w) + ".png"
            if(result == 1):
                newfilename = ImageSubfolder + "/" + "Sock" + "/" + justthefilename + "_" + str(current_h) + "_" + str(current_w) + ".png"
                boxesContainingSock.append((current_h, current_w))
            
            print(newfilename)
            cv2.imwrite(newfilename, cropped_image)
            current_w = current_w + delta
        current_h = current_h + delta
    return boxesContainingSock
    
def generateboxes2(ImageFileName):
    boxesContainingSock = []
    original = cv2.imread(ImageFileName)
    imageswithboxes = original.copy()
    justthefilename = ImageFileName.split('/')[-1]
    justthefilename  = justthefilename.split('.')[0]
    print("justthefilename " + justthefilename)
    
    current_h = 0
    size = 240
    delta = 60
    boxno=0
    
    imageboxes = [(0,0), (120,0), (240,0),(360,0),(0,160), (120,160), (240,160),(360,160),(0,320), (120,320), (240,320),(360,320),(0,480), (120,480), (240,480),(360,480)]

    size_w = 160
    size_h = 120
    for current_h, current_w in imageboxes:
        cropped_image = original[current_h:current_h+size_h, current_w:current_w+size_w]
        result = getNotSockOrSock(cropped_image)
        newfilename = ImageSubfolder + "/" + "NotSock" + "/" + justthefilename + "_" + str(current_h) + "_" + str(current_w) + ".png"
        if(result == 1):
            newfilename = ImageSubfolder + "/" + "Sock" + "/" + justthefilename + "_" + str(current_h) + "_" + str(current_w) + ".png"
            boxesContainingSock.append((current_h, current_w))
            cv2.rectangle(imageswithboxes, (current_w, current_h), (current_w+size_w, current_h+size_h), (255,0,0), thickness=1, lineType=8, shift=0)
        print(newfilename)
        cv2.imwrite(newfilename, cropped_image)
        newfilenameforimageswithboxes = ImageSubfolder + "/" + "box_" + justthefilename + ".png"
        cv2.imwrite(newfilenameforimageswithboxes, imageswithboxes)

    return boxesContainingSock

def isSock(image, x1, y1, x2, y2):
    cropped_image = image[y1:y2, x1:x2]
    result = getNotSockOrSock(cropped_image)
    return result==1

#Generated boxes
def generateboxes3(ImageFileName):
    ImprovedBoxes = []    
    boxes = generateboxes2(ImageFileName)
    original = cv2.imread(ImageFileName)
    imageswithboxes = original.copy()

    justthefilename = ImageFileName.split('/')[-1]
    justthefilename  = justthefilename.split('.')[0]

    alreadyTaken = {}
    delta_move = 5
    box_y_size = 120
    box_x_size = 160
    i = 0
    for box in boxes:
        i = i +1
        if box in alreadyTaken:
            continue
        else:
            alreadyTaken[box]=True # .append(box)
            y, x = box
            min_x = x
            max_x = x + box_x_size
            max_y= y+ box_y_size
            min_y=y
            while x - delta_move >= 0:
                x = x - delta_move
                if (isSock(original, x,y,x+box_x_size, y+ box_y_size) == False):
                    min_x=x+box_x_size
                    break

            y, x = box
            while x + box_x_size < 640:
                x = x + delta_move
                if (isSock(original, x,y,x+box_x_size, y+ box_y_size) == False):
                    max_x=x #+ box_x_size
                    break

            y, x = box            
            while y + box_y_size < 480:
                y = y + delta_move
                if (isSock(original, x,y,x+box_x_size, y+ box_y_size) == False):
                    max_y=y
                    break
            
            y, x = box
            while y - delta_move >= 0:
                y = y - delta_move
                if (isSock(original, x,y,x+box_x_size, y+ box_y_size) == False):
                    min_y=y+box_y_size
                    break
            
            ImprovedBoxes.append((min_x, min_y, max_x, max_y))
            cv2.rectangle(imageswithboxes, (min_x, min_y), (max_x, max_y), (255,i*20,i*10), thickness=1, lineType=8, shift=0)
    
    newfilenameforimageswithboxes = ImageSubfolder + "/" + "box2_" + justthefilename + ".png"
    cv2.imwrite(newfilenameforimageswithboxes, imageswithboxes)

    return ImprovedBoxes

