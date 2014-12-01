
import cv2
import numpy as np
import sys

import motionTracker2 as mt

def main(argv):
    capture = None
    inputFile = None

    if len(sys.argv) > 1 :
        inputFile = sys.argv[1]
        print "Opening file: {}".format(inputFile)
        capture=cv2.VideoCapture(inputFile)
    else :
        print "Opening camera."
        capture=cv2.VideoCapture(0)


    if capture.isOpened :
        motionTracker = mt.MotionTracker2()

        while capture.isOpened :
            f,frame = capture.read()
            frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            motionTracker.getMovingObjects(frameGray)
            frame = motionTracker.drawContours()
            if not frame == None :
	        cv2.imshow('tracker', frame)
        
            if(cv2.waitKey(27)!=-1):
                capture.release()
                cv2.destroyAllWindows()
                break

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
