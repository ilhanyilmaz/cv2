
import cv2
import numpy as np
import sys

import backgroundExtractor as be
import motionTrackerMOG as mt
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
        motionTracker = mt.MotionTrackerMOG(capture, './sample/calibration/calibration.npz')

        while capture.isOpened :
            #print capture.get(cv2.cv.CV_CAP_PROP_)
            f,frame = capture.read()
            frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            motionTracker.update(frameGray)
            mo = motionTracker.getMovingObjects()
            #print len(mo)
            if len(mo) > 30 :
                motionTracker = mt.MotionTrackerMOG(capture, './sample/calibration/calibration.npz')
                continue
            
            motionTracker.getObjectPositions()
            frame = motionTracker.drawContours()
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
