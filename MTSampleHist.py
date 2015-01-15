
import cv2
import numpy as np
import sys

import backgroundExtractor as be
import motionTrackerHIST as mt
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


    if camShift:
        i=0
        camShiftTracker = cst.CamShiftTracker()
        
    if capture.isOpened :
        motionTracker = mt.MotionTrackerHist(capture, histogramFile='./sample/captures/capture_116.jpg_', showTrackerImage= showTracker)

        while capture.isOpened :
            
            f,frame = capture.read()
            
            frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            motionTracker.update(frame)
            
            #mo = motionTracker.getMovingObjects()
            #frameGray = motionTracker.drawRectangles()
            
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
                #ddi = motionTracker.getDilatedDiffImage(frame)
                #if i == 0:
                    #camShiftTracker.updateRectangles(frame, motionTracker.getMovingRectangles())
                    #camShiftTracker.updateContours(frame, mo)
                #    camShiftTracker.updateBiggestObjectContour(frame, motionTracker.getBiggestMovingObject())
                #if i%90 == 0:
                #    camShiftTracker.updateContours(ddi, mo)
                    
                camShiftTracker.trackBiggestObject(frame)
                #i+=1

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
                    key = cv2.waitKey(27)
                    if key == 1048608: # space key
                        #camShiftTracker.updateRectangles(frame, motionTracker.getMovingRectangles())
                        #camShiftTracker.updateContours(frame, mo)
                        camShiftTracker.updateBiggestObjectContour(frame, motionTracker.getBiggestMovingObjectContour())
                    elif(key!=-1):
                        print key
                        capture.release()
                        cv2.destroyAllWindows()
                        break

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
