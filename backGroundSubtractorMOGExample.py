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

fgbg = cv2.BackgroundSubtractorMOG()

while(capture.isOpened): 
    f,img=capture.read()
    if f==True:
        #img=cv2.flip(img,1)
        #img=cv2.medianBlur(img,3)
        fgmask = fgbg.apply(img)
        cv2.imshow('track',fgmask)
    if(cv2.waitKey(27)!=-1):
        capture.release()
        cv2.destroyAllWindows()
        break 
