
import cv2
import numpy as np
import sys

import backgroundExtractor as be
import motionTrackerBACK as mt
import videoPlayer as vp
import brightestobject as bo
import objectRecognizer as objr
import camShiftTracker as cst
import locationEstimator as le

import arduinocomm as ac

motionTracker = None
show2DPositions = False
showBackground = False
showTracker = False
showDiff = False
showMain = True
controlArduino = False
camShift = False
colorSearch = False
ballSearch = False


def init():
    global controlArduino, colorSearch
    if controlArduino:
        ac.init()
    if colorSearch:
        objr.createJerseyWindow()
        
def createTrackbars():
    global showMain, show2DPositions, showBackground, showTracker, showDiff
    if not showMain:
        return
    cv2.namedWindow('video player')
    cv2.createTrackbar('show 2D positions', 'video player',show2DPositions, 1, np.uint)
    cv2.createTrackbar('show background', 'video player', showBackground, 1, np.uint)
    cv2.createTrackbar('show tracker', 'video player', showTracker, 1, np.uint)
    cv2.createTrackbar('show diff image', 'video player', showDiff, 1, np.uint)
    
def checkSettings():
    
    global showMain, motionTracker
    
    if not showMain:
        return
        
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
            
    value = cv2.getTrackbarPos('show tracker', 'video player')
    if value != motionTracker.showTracker:
        motionTracker.setParameter('show_tracker', value)
        if value == 0:
            cv2.destroyWindow('tracker')
            
    value = cv2.getTrackbarPos('show diff image', 'video player')
    if value == False and motionTracker.showDiffImage:
        cv2.destroyWindow('diff image')
    elif value == True and not motionTracker.showDiffImage:
        motionTracker.createDiffImageWindow()
    motionTracker.setParameter('show_diff_image', value)

def main(argv):
    global motionTracker
    global showTracker, showMain, showBackground, showTracker
    global controlArduino, camShift, colorSearch, ballSearch, show2DPositions
    
    capture = None
    inputFile = None
    player = None
    if len(sys.argv) > 1 :
        inputFile = sys.argv[1]
        print "Opening file: {}".format(inputFile)
        capture=cv2.VideoCapture(inputFile)
        player = vp.VideoPlayer(capture, show=showMain)
    else :
        print "Opening camera."
        capture=cv2.VideoCapture(0)


    createTrackbars()
    if camShift:
        i=0
        camShiftTracker = cst.CamShiftTracker()
        
    if capture.isOpened :
        motionTracker = mt.MotionTrackerBACK(capture, calibrationFile='./sample/calibration/calibration.npz', showTrackerImage= showTracker, showBackImage = showBackground)

        while capture.isOpened :
            checkSettings()
            
            f,frame = capture.read()
            
            frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            motionTracker.update(frameGray)
            
            mo = motionTracker.getMovingObjects()
            frameGray = motionTracker.drawRectangles()
            
            if motionTracker.showPositions:
                motionTracker.update2dPoints()
            
            if controlArduino:
                biggestObjPos = motionTracker.getBiggestMovingObject()
                height, width = frameGray.shape
                if not biggestObjPos == None:
                    x = int(biggestObjPos[0] *100 / float(width))
                    y = int(biggestObjPos[1] *100 / float(height))
                    ac.lookAt((x,y))
                #cv2.circle(frameGray, (biggestObjPos), 10, 255,-1)
                #cv2.imshow('framegray', frameGray)

            if camShift:
                ddi = motionTracker.getDilatedDiffImage(frame)
                if i%90 == 0:
                    camShiftTracker.updateContours(ddi, mo)
                    
                camShiftTracker.track(ddi)
                i+=1

            if colorSearch:
                objr.playersWithGreenJersey(frame, mo)  
            
            if ballSearch:
                ballContour = bo.getBall(frame, motionTracker.diffImage) #brightest object should be a BALL
                if not ballContour == None:
                    x,y,w,h = cv2.boundingRect(ballContour)
                    cv2.rectangle(frameGray, (x,y), (x+w,y+h), (255,255,255))
           
            if not player == None :
                player.loop()
            else :
                if showMain:
                    cv2.imshow('video player', frame)
                    if(cv2.waitKey(27)!=-1):
                        capture.release()
                        cv2.destroyAllWindows()
                        break

if __name__ == "__main__":
    init()
    sys.exit(main(sys.argv[1:]))
