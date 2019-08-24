import tensorflow as tf
import numpy as np
from tensorflow import keras
import os
import cv2
import matplotlib.pyplot as plt

model = None
TemplateDir = "E:\\R2D2\\images\\AllImages"
SubpartsDir = "E:\\R2D2\\images\\Crop\\Subparts"

def load_model():
    global model
    model2 = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(40, (3, 3), activation='relu', input_shape=(60,60, 3)),
  tf.keras.layers.MaxPooling2D((2, 2)),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Conv2D(20, (3, 3), activation='relu'),
  tf.keras.layers.MaxPooling2D((2, 2)),
  #tf.keras.layers.Conv2D(12, (3, 3), activation='relu'),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(8, activation='relu'),
  tf.keras.layers.Dropout(0.3),
  #tf.keras.layers.Dense(2, activation='sigmoid')
  tf.keras.layers.Dense(2, activation='softmax')
    ])

    
    modelfile= "E:\\AIPlay\\tensor\\training_16\\cp_60-60_40-d-20_0015.ckpt"
    model2.load_weights(modelfile)
    model = model2

def getNotSockOrSock(image):
    if(model is None):
        load_model()
    resized = cv2.resize(image, (60,60))
    resized=resized/255
    prediction = model.predict(np.array([resized]))
    if(prediction[0][1]>0.8):
        return 1
    return 0

    #result = np.argmax(prediction[0])
    #return result

ImageSubfolder = SubpartsDir
#SubpartsDir = "E:\\R2D2\\images\\Crop\\Subparts"
def generateboxes(ImageFileName):
    boxesContainingSock = []
    original = cv2.imread(ImageFileName)
    justthefilename = ImageFileName.split('\\')[-1]
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
            newfilename = ImageSubfolder + "\\" + "NotSock" + "\\" + justthefilename + "_" + str(current_h) + "_" + str(current_w) + ".png"
            if(result == 1):
                newfilename = ImageSubfolder + "\\" + "Sock" + "\\" + justthefilename + "_" + str(current_h) + "_" + str(current_w) + ".png"
                boxesContainingSock.append((current_h, current_w))
            
            print(newfilename)
            cv2.imwrite(newfilename, cropped_image)
            current_w = current_w + delta
        current_h = current_h + delta
    return boxesContainingSock
    

for file in os.listdir(TemplateDir):
    filename = TemplateDir + "\\" + os.fsdecode(file)
    generateboxes(filename)