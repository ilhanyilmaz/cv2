
import cv2
import numpy as np
import sys

import backgroundExtractor as be
import motionTrackerBACK as mt
import arduinocomm as ac

motionTracker = None
controlArduino = False


def init():
    if controlArduino:
        ac.init()
        
def main(argv):
    global motionTracker
    global controlArduino
    
    capture = None
    inputFile = None
    if len(sys.argv) > 1 :
        capNo = int(sys.argv[1])
        capture=cv2.VideoCapture(capNo)
    else :
        print "Opening camera."
        capture=cv2.VideoCapture(0)

    if capture.isOpened :
        motionTracker = mt.MotionTrackerBACK(capture)

        while capture.isOpened :
            
            f,frame = capture.read()
            
            frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            motionTracker.update(frameGray)
            
            motionTracker.getMovingObjects()
            
            if controlArduino:
                biggestObjPos = motionTracker.getBiggestMovingObject()
                height, width = frameGray.shape
                if not biggestObjPos == None:
                    x = int(biggestObjPos[0] *64 / float(width))
                    y = int(biggestObjPos[1] *64 / float(height))
                    ac.lookAt((x,y))
                #cv2.circle(frameGray, (biggestObjPos), 10, 255,-1)
                #cv2.imshow('framegray', frameGray)
           
            if(cv2.waitKey(27)!=-1):
                capture.release()
                break

if __name__ == "__main__":
    init()
    sys.exit(main(sys.argv[1:]))
