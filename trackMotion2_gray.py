import cv2
import numpy as np
import sys

THRESHOLD = 20

capture = None
inputFile = None

if len(sys.argv) > 1 :
    inputFile = sys.argv[1]
    print "Opening file: {}".format(inputFile)
    capture=cv2.VideoCapture(inputFile)
else :
    print "Opening camera."
    capture=cv2.VideoCapture(0)

backImage = cv2.imread("backgroundImageGray.jpg", cv2.COLOR_BGR2GRAY)



while(capture.isOpened): 
    f,img=capture.read()

    if f==True:
        imgGray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        diffImage = cv2.absdiff(backImage,imgGray)
        ret, threshold = cv2.threshold(diffImage, THRESHOLD, 255, cv2.THRESH_BINARY)
        kernel = np.ones((2,2),np.uint8)
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
        #threshold = cv2.erode(threshold,kernel,iterations = 1)
        kernel = np.ones((10,10),np.uint8)
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
        #threshold = cv2.dilate(threshold,kernel,iterations = 1)
        #kernel = np.ones((8,8),np.uint8)
        #threshold = cv2.erode(threshold,kernel,iterations = 1)
        contours, hierachy = cv2.findContours(threshold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img,contours,-1,(0,255,0),3)

        cv2.imshow('track', img)

    if(cv2.waitKey(27)!=-1):
        capture.release()
        cv2.destroyAllWindows()
        break 

capture.release()
cv2.destroyAllWindows()
