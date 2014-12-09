import cv2
import numpy as np
import sys
import locationEstimator as le
import backgroundExtractor2 as be

class MotionTracker(object):

    def __init__(self, calibrationFile, capture, backImage = None):
        self.KERNEL_OPEN = np.ones((1,1),np.uint8)
        self.KERNEL_CLOSE = np.ones((10,10),np.uint8)
        self.contours = None
        self.frame = None
        self.capture = capture
        self.backExtr = None
        if not backImage == None :
            self.backImage = backImage
        else :
            self.backImage = None
        if not calibrationFile == None :
            self.estimator = le.LocationEstimator(calibrationFile)

    def updateBackgroundImage(self, capture, perfection):
        self.backExtr = be.BackgroundExtractor(perfection)
        if self.capture.isOpened :
            self.backImage = self.backExtr.extract(capture, 90)
            if not self.backImage == None:
                cv2.imshow('backImage', self.backImage)
            return self.backImage
        
        return self.backImage
    
    def getMovingObjects(self, frame):
        self.frame = frame.copy()
        #self.frame = cv2.blur(self.frame, (5,5))
        #self.frame = cv2.bilateralFilter(self.frame,9,75,75)
        diffImage = cv2.absdiff(self.backImage,self.frame)
        ret, threshold = cv2.threshold(diffImage, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
        #ret, threshold = cv2.threshold(diffImage, self.THRESHOLD, 255, cv2.THRESH_BINARY)
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, self.KERNEL_OPEN)
        #threshold = cv2.erode(threshold,kernel,iterations = 1)
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, self.KERNEL_CLOSE)
        #threshold = cv2.dilate(threshold,kernel,iterations = 1)
        #kernel = np.ones((8,8),np.uint8)
        #threshold = cv2.erode(threshold,kernel,iterations = 1)
        self.contours, hierachy = cv2.findContours(threshold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        return self.contours

    def getObjectPositions(self):
        if self.contours == None :
            return
        posImage = np.zeros((500,500,3), np.uint8)
        #i=1
        for contour in self.contours:
            area = cv2.contourArea(contour)
            #print area
            if area < 10:
                continue
            x,y,w,h = cv2.boundingRect(contour)
            objPos = self.estimator.get3dCoordinates(x+w/2, y+h)
            cv2.circle(posImage, (int(objPos[0]),int(objPos[1])), 10, (0,255,0),-1)
            #if i==1 :
                #print 'obj{0}= {1}-{2}'.format(i, str(x+w/2), str(y+h))
                #print self.estimator.get3dCoordinates(x+w/2, y+h)
            #i+=1
        cv2.imshow("pos", posImage)
    def drawContours(self):
        if self.contours == None:
            return self.frame
        for contour in self.contours:
            area = cv2.contourArea(contour)
            #print area
            if area < 10:
                continue
            x,y,w,h = cv2.boundingRect(contour)
            cv2.rectangle(self.frame, (x,y), (x+w,y+h), (0,255,0))
            #cv2.drawContours(img,contours,-1,(0,255,0),3)
        return self.frame
