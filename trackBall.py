import cv2
import numpy as np
import sys

THRESHOLD = 20
THRESHOLD_WHITE = 230
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
        ret, threshold1 = cv2.threshold(diffImage, THRESHOLD, 255, cv2.THRESH_BINARY)
        ret, threshold2 = cv2.threshold(imgGray, THRESHOLD_WHITE, 255, cv2.THRESH_BINARY)
        
        #threshold = cv2.bitwise_and(threshold1, threshold2)

        threshold = cv2.bitwise_and(threshold1, threshold2)
        #kernel = np.ones((2,2),np.uint8)
        #threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
        #kernel = np.ones((10,10),np.uint8)
        #threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
        """contours, hierachy = cv2.findContours(threshold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:   
            area = cv2.contourArea(contour)
           #print area
            if area < 10:
                continue
            x,y,w,h = cv2.boundingRect(contour)
            #print "{0}-{1}/{2}-{3}".format(x,y,w,h)
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0))
        #cv2.drawContours(img,contours,-1,(0,255,0),3)
        """
        cv2.imshow('track1', threshold1)
        cv2.imshow('track2', threshold2)
        cv2.imshow('track3', threshold)

    if(cv2.waitKey(27)!=-1):
        capture.release()
        cv2.destroyAllWindows()
        break 

capture.release()
cv2.destroyAllWindows()
