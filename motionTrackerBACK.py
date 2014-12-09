import cv2
import numpy as np
import sys
import locationEstimator as le
import motionTracker as mt
import backgroundExtractor2 as be


class MotionTrackerBACK(mt.MotionTracker):
    
    def __init__(self, calibrationFile, capture, perfection = 90, backImage = None, ):
        super(self.__class__, self).__init__(calibrationFile, capture)
        self.perfection = perfection
        self.backExtr = be.BackgroundExtractor(self.perfection)
        self.THRESHOLD = 20
        if not backImage == None :
            self.backImage = backImage
        else :
            self.backImage = None
    
    def getMovingObjects(self, frame):
        #imgGray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.frame = frame.copy()
        #self.frame = cv2.bilateralFilter(self.frame,9,75,75)
        self.frame = cv2.blur(self.frame, (5,5))
        self.backImage = self.backExtr.feed(self.frame)
        cv2.imshow('backImage', self.backImage)
        
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

    def updateBackgroundImage(self, capture, perfection, frameCountLimit):
        self.backExtr = be.BackgroundExtractor(perfection)
        if self.capture.isOpened :
            self.backImage = self.backExtr.extract(capture, frameCountLimit)
            if not self.backImage == None:
                cv2.imshow('backImage', self.backImage)
            return self.backImage
        
        return self.backImage
