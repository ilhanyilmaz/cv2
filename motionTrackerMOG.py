import cv2
import numpy as np
import sys
import locationEstimator as le
import motionTracker as mt
import backgroundExtractor2 as be

class MotionTrackerMOG(mt.MotionTracker):

    def __init__(self, capture, calibrationFile = None, backImage = None, blur = 5):
		
        super(self.__class__, self).__init__(capture, calibrationFile = calibrationFile, blur=blur)
        if not backImage == None :
            self.backImage = backImage
        else :
            self.backImage = self.updateBackgroundImage(capture, 100, 200)
            
        self.fgbg = cv2.BackgroundSubtractorMOG()

        if self.backImage == None :
            self.fgbg.apply(self.backImage)
        
    def update(self, frame):
		
		super(self.__class__, self).update(frame)
		
        self.diffImage = self.fgbg.apply(self.frame)

    def updateBackgroundImage(self, capture, perfection, frameCountLimit):
		
        self.backExtr = be.BackgroundExtractor(perfection)
        if self.capture.isOpened :
            self.backImage = self.backExtr.extract(capture, frameCountLimit)
            if not self.backImage == None:
                cv2.imshow('backImage', self.backImage)
            return self.backImage
        
        return self.backImage
