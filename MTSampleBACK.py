
import cv2
import numpy as np
import sys

import backgroundExtractor as be
import motionTrackerBACK as mt
import videoPlayer as vp
import brightestobject as bo
import objectRecognizer as objr

motionTracker = None

show2DPositions = False
showBackground = False
showTracker = False
showDiff = False

def createTrackbars():
    global show2DPositions, showBackground, showTracker, showDiff
    cv2.namedWindow('video player')
    cv2.createTrackbar('show 2D positions', 'video player',show2DPositions, 1, np.uint)
    cv2.createTrackbar('show background', 'video player', showBackground, 1, np.uint)
    cv2.createTrackbar('show tracker', 'video player', showTracker, 1, np.uint)
    cv2.createTrackbar('show diff image', 'video player', showDiff, 1, np.uint)
    objr.createJerseyWindow()
    
def checkSettings():
    
    global motionTracker
    
    if motionTracker == None:
		return
    
    motionTracker.checkSettings()
    
    value = cv2.getTrackbarPos('show 2D positions', 'video player')
    if value != motionTracker.showPositions:
        motionTracker.setParameter('show_positions', value)
        if value == False:
            cv2.destroyWindow('positions')

    value = cv2.getTrackbarPos('show background', 'video player')
    if value != motionTracker.backExtr.showBackImage:
        motionTracker.setParameter('show_back_image', value)
        if value == 0:
            cv2.destroyWindow('backImage')
            
    value = cv2.getTrackbarPos('show diff image', 'video player')
    if value != motionTracker.showDiffImage:
        motionTracker.setParameter('show_diff_image', value)
        if value == 0:
            cv2.destroyWindow('diff image')
            
    value = cv2.getTrackbarPos('show tracker', 'video player')
    if value == False and motionTracker.showTracker:
        cv2.destroyWindow('tracker')
    elif value == True and not motionTracker.showTracker:
        motionTracker.createTrackerWindow()
    motionTracker.setParameter('show_tracker', value)

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
        motionTracker = mt.MotionTrackerBACK(capture, './sample/calibration/calibration.npz')

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
            motionTracker.update(frameGray)
            
            mo = motionTracker.getMovingObjects()
            motionTracker.getObjectPositions()
            frameGray = motionTracker.drawContours()

            objr.playersWithGreenJersey(frame, mo)           
            #ballContour = bo.getBall(frame, motionTracker.diffImage) #brightest object should be a BALL
            #if not ballContour == None:
            #    x,y,w,h = cv2.boundingRect(ballContour)
            #    cv2.rectangle(frameGray, (x,y), (x+w,y+h), (255,255,255))
           
            if not player == None :
                player.loop()
            else :
                if(cv2.waitKey(27)!=-1):
                    capture.release()
                    cv2.destroyAllWindows()
                    break

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
