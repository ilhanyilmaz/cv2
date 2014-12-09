
import cv2
import numpy as np
import sys

import backgroundExtractor as be
import motionTrackerDIFF as mt
import videoPlayer as vp

def main(argv):
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


    if capture.isOpened :
        motionTracker = mt.MotionTrackerDIFF('./sample/calibration/calibration.npz', capture)

        while capture.isOpened :
            f,frame = capture.read()
            frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mo = motionTracker.getMovingObjects(frameGray)
            motionTracker.getObjectPositions()
            frame = motionTracker.drawContours()
            if frame == None :
                continue
            cv2.imshow('tracker', frame)

            if not player == None :
                player.loop()
            else :
                if(cv2.waitKey(27)!=-1):
                    capture.release()
                    cv2.destroyAllWindows()
                    break

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
