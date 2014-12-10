
import cv2
import numpy as np
import sys

import backgroundExtractor as be
import motionTrackerBACK as mt
import videoPlayer as vp
import brightestobject as bo

blur = 5
threshold = 20
m_open = 1
m_close = 12
motionTracker = None
showTracker = True
showBackImage = True
showPositions = True

def createTrackbars():
    
    cv2.namedWindow('video player')
    cv2.createTrackbar('show 2D positions', 'video player',1, 1, np.uint)
    cv2.createTrackbar('show background', 'video player', 1, 1, np.uint)
    cv2.createTrackbar('show tracker', 'video player', 1, 1, np.uint)
    createTrackerWindow()
    
def createTrackerWindow():

    global blur, threshold, m_open, m_close
    
    cv2.namedWindow('tracker')
    cv2.createTrackbar('blur','tracker',blur, 10, np.uint)
    cv2.createTrackbar('m_open','tracker',m_open, 5, np.uint)
    cv2.createTrackbar('m_close','tracker',m_close, 20, np.uint)
    cv2.createTrackbar('threshold','tracker',threshold, 30, np.uint)

def trackerWindowSettings():

    global blur, threshold, m_open, m_close
    
    value = cv2.getTrackbarPos('blur','tracker')
    if value == 0:
        value = 1
    if value != blur :
        blur = value
        motionTracker.setParameter('blur', value)
                                   
    value = cv2.getTrackbarPos('threshold','tracker')
    if value != threshold :
        threshold = value
        motionTracker.setParameter('threshold', value)

    value = cv2.getTrackbarPos('m_open','tracker')
    if value == 0:
        value = 1
    if value != m_open :
        m_open = value
        motionTracker.setParameter('m_open', value)

    value = cv2.getTrackbarPos('m_close','tracker')
    if value == 0:
        value = 1
    if value != m_close :
        m_close = value
        motionTracker.setParameter('m_close', value)
        
def checkSettings():
    
    global motionTracker
    global showTracker, showPositions, showBackImage
    
    if motionTracker == None:
        return
    
    if showTracker :
        trackerWindowSettings()

    value = cv2.getTrackbarPos('show 2D positions', 'video player')
    if value != showPositions:
        motionTracker.setParameter('show_positions', value)
        if value == False:
            cv2.destroyWindow('positions')
        showPositions = value

    value = cv2.getTrackbarPos('show background', 'video player')

    if value != showBackImage:
        motionTracker.setParameter('show_back_image', value)
        if value == 0:
            cv2.destroyWindow('backImage')
        showBackImage = value
        
    value = cv2.getTrackbarPos('show tracker', 'video player')
    
    if value == False and showTracker:
        cv2.destroyWindow('tracker')
        showTracker = False
    elif value == True and not showTracker:
        createTrackerWindow()
        showTracker = True

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


    createTrackbars()
    if capture.isOpened :
        motionTracker = mt.MotionTrackerBACK('./sample/calibration/calibration.npz', capture)

        while capture.isOpened :
            checkSettings()
            #print capture.get(cv2.cv.CV_CAP_PROP_)
            f,frame = capture.read()
            #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            #h,s,v = cv2.split(hsv)
            #cv2.imshow("h",h)
            #cv2.imshow("s",s)
            #cv2.imshow("v",v)
            frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            mo = motionTracker.getMovingObjects(frameGray)
            

            #print len(mo)
            #if len(mo) > 50 :
            #    motionTracker = mt.MotionTrackerBACK('./sample/calibration/calibration.npz', capture)
            #    continue
            motionTracker.getObjectPositions()
            frameGray = motionTracker.drawContours()

            boPos = bo.findBall(frame, mo) #brightest object should be a BALL
            if boPos < len(mo) and boPos > -1:
                x,y,w,h = cv2.boundingRect(mo[boPos])
                cv2.rectangle(frameGray, (x,y), (x+w,y+h), (255,255,255))

            if showTracker : 
                cv2.imshow('tracker', frameGray)
           
            if not player == None :
                player.loop()
            else :
                if(cv2.waitKey(27)!=-1):
                    capture.release()
                    cv2.destroyAllWindows()
                    break

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
