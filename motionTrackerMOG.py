import cv2
import numpy as np
import sys
import locationEstimator as le
import motionTracker as mt
import backgroundExtractor2 as be

class MotionTrackerMOG(mt.MotionTracker):

    def __init__(self, calibration, capture, backImage = None):
        super(self.__class__,self).__init__(calibration, capture)
        if not backImage == None :
            self.backImage = backImage
        else :
            self.backImage = self.updateBackgroundImage(capture, 100, 200)
            
        self.fgbg = cv2.BackgroundSubtractorMOG()

        if self.backImage == None :
            self.fgbg.apply(self.backImage)
        

    def getMovingObjects(self, frame):
        self.frame = frame.copy()
        fgmask = self.fgbg.apply(self.frame)

        threshold = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.KERNEL_OPEN)
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, self.KERNEL_CLOSE)

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
