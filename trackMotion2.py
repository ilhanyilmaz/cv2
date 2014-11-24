import cv2
import numpy as np
import sys

capture = None
inputFile = None

if len(sys.argv) > 1 :
    inputFile = sys.argv[1]
    print "Opening file: {}".format(inputFile)
    capture=cv2.VideoCapture(inputFile)
else :
    print "Opening camera."
    capture=cv2.VideoCapture(0)

backImage = cv2.imread("backgroundImage.jpg")

while(capture.isOpened): 
    f,img=capture.read()

    if f==True:
        diffImage = cv2.absdiff(backImage,img)
        ret, thresholdRGB = cv2.threshold(diffImage, 30, 255, cv2.THRESH_BINARY)

        cv2.imshow('track', thresholdRGB)

    if(cv2.waitKey(27)!=-1):
        capture.release()
        cv2.destroyAllWindows()
        break 

capture.release()
cv2.destroyAllWindows()
