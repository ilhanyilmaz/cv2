
import cv2
import numpy as np
import sys

import backgroundExtractor as be
import motionTrackerBACK as mt
import videoPlayer as vp
import brightestobject as bo
import objectRecognizer as objr
import camShiftTracker as cst

import arduinocomm as ac

motionTracker = None

show2DPositions = False
showBackground = False
showTracker = False
showDiff = False

    
def main(argv):
    global motionTracker
    global showTracker
    
    capture = None
    inputFile = None
    player = None
    if len(sys.argv) > 1 :
        inputFile = sys.argv[1]
        print "Opening file: {}".format(inputFile)
        capture=cv2.VideoCapture(inputFile)
        player = vp.VideoPlayer(capture)
    else :
        print "Opening camera."
        capture=cv2.VideoCapture(0)


    i=0
    if capture.isOpened :
        motionTracker = mt.MotionTrackerBACK(capture)

        while capture.isOpened :
            f,frame = capture.read()
            frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            motionTracker.update(frameGray)
            biggestObjPos = motionTracker.getBiggestMovingObject()
            height, width = frameGray.shape
            if not biggestObjPos == None:
                x = int(biggestObjPos[0] *100 / float(width))
                y = int(biggestObjPos[1] *100 / float(height))
                ac.lookAt((x,y))

            cv2.imshow("image",frameGray)
            
            if(cv2.waitKey(27)!=-1):
                capture.release()
                cv2.destroyAllWindows()
                break

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
