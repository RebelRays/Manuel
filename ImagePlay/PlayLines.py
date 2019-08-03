#Playing around with images taken

#pip install matplotlib
#pip install numpy

#pip install opencv-python


import cv2
import numpy as np
import matplotlib.pyplot as plt
image = cv2.imread("E:\\R2D2\\images\\Sock9.png")

cv2.imshow("ok", image)
cv2.waitKey(0)
#imageCopy = np.copy(image)
grayImage=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
blurImage = cv2.GaussianBlur(grayImage, (5,5), 0)
cannyImage=cv2.Canny(blurImage, 50, 100)

#The region of interest
height = image.shape[0]
#down_regions = np.array([[(0, height), (0,340), (640,171), (640,360),(360,448),(360,height)]])
#region_of_floor = np.zeros_like(cannyImage)
#cv2.fillPoly(region_of_floor, down_regions, 255)
#down_regions = np.array([[(0, height), (0,210), (620,225), (620,402),(335,402),(335,height)]])
down_regions = np.array([[(0, height), (0,210), (620,225), (620,height)]])

region_of_floor = np.zeros_like(cannyImage)
cv2.fillPoly(region_of_floor, down_regions, 255)

cv2.imshow("ok", region_of_floor)
cv2.waitKey(0)

#Filter the rest
masked_image = cv2.bitwise_and(cannyImage, region_of_floor)
cv2.imshow("masked_image", masked_image)
cv2.waitKey(0)


#Get Lines
#treshold = 100
treshold = 2
#lines=cv2.HoughLinesP(masked_image, 2, np.pi/180, treshold, np.array([]), minLineLength=40, maxLineGap=5)
lines=cv2.HoughLinesP(masked_image, 2, np.pi/180, treshold, np.array([]), minLineLength=4, maxLineGap=5)

#Plot them
line_image = np.zeros_like(image)
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


print(combined_x)
print(combined_y)

plt.imshow(image)
plt.show()




#cv2.imshow("ok", image)
#cv2.waitKey(0)
print("Done")