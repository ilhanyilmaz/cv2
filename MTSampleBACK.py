
import cv2
import numpy as np
import sys

import backgroundExtractor as be
import motionTrackerBACK as mt
import videoPlayer as vp

perfection = 50
blur = 5
threshold = 20
back_threshold = 6
m_open = 1
m_close = 10
motionTracker = None

def createTrackbars():
    global perfection, blur, threshold, back_threshold, m_open, m_close
    cv2.namedWindow('settings')
    
    cv2.createTrackbar('blur','settings',blur, 10, np.uint)
    cv2.createTrackbar('perfection','settings',perfection, 250, np.uint)
    cv2.createTrackbar('back_threshold','settings',back_threshold, 30, np.uint)
    cv2.createTrackbar('m_open','settings',m_open, 5, np.uint)
    cv2.createTrackbar('m_close','settings',m_close, 20, np.uint)
    cv2.createTrackbar('threshold','settings',threshold, 30, np.uint)
    
    

def checkSettings():
    global perfection, blur, threshold, back_threshold, m_open, m_close
    global motionTracker
    if motionTracker == None:
        return
    value = cv2.getTrackbarPos('perfection','settings')
    if value != perfection :
        perfection = value
        motionTracker.setParameter('perfection', value)
        
    value = cv2.getTrackbarPos('blur','settings')
    if value == 0:
        value = 1
    if value != blur :
        blur = value
        motionTracker.setParameter('blur', value)
                                   
    value = cv2.getTrackbarPos('threshold','settings')
    if value != threshold :
        threshold = value
        motionTracker.setParameter('threshold', value)

    value = cv2.getTrackbarPos('back_threshold','settings')
    if value != back_threshold :
        back_threshold = value
        motionTracker.setParameter('back_threshold', value)

    value = cv2.getTrackbarPos('m_open','settings')
    if value == 0:
        value = 1
    if value != m_open :
        m_open = value
        motionTracker.setParameter('m_open', value)

    value = cv2.getTrackbarPos('m_close','settings')
    if value == 0:
        value = 1
    if value != m_close :
        m_close = value
        motionTracker.setParameter('m_close', value)

def main(argv):
    global motionTracker
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


    createTrackbars()
    if capture.isOpened :
        motionTracker = mt.MotionTrackerBACK('./sample/calibration/calibration.npz', capture)

        while capture.isOpened :
            checkSettings()
            #print capture.get(cv2.cv.CV_CAP_PROP_)
            f,frame = capture.read()
            frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mo = motionTracker.getMovingObjects(frameGray)
            #print len(mo)
            #if len(mo) > 50 :
            #    motionTracker = mt.MotionTrackerBACK('./sample/calibration/calibration.npz', capture)
            #    continue
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
