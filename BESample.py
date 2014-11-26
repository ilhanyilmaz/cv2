import cv2
import numpy as np
import sys

import backgroundExtractor as be

capture = None
inputFile = None

if len(sys.argv) > 1 :
    inputFile = sys.argv[1]
    print "Opening file: {}".format(inputFile)
    capture=cv2.VideoCapture(inputFile)
else :
    print "Opening camera."
    capture=cv2.VideoCapture(0)

backExtr = be.BackgroundExtractor()

if capture.isOpened :
    print capture
    backImage =backExtr.extract(capture, 30)
    cv2.imshow('track', backImage)

    if(cv2.waitKey()!=-1):
        capture.release()
        cv2.destroyAllWindows()
        cv2.imwrite("BESample.jpg", backImage)
