import cv2
import numpy as np
import sys
import locationEstimator as le
import motionTracker as mt
import backgroundExtractor2 as be


class MotionTrackerBACK(mt.MotionTracker):
    
    def __init__(self, capture, calibrationFile=None, blur=2, perfection=100, showTrackerImage=False, backImage = None, showBackImage = False):
        
        super(self.__class__, self).__init__(capture, calibrationFile=calibrationFile, showTrackerImage=showTrackerImage, blur=blur)
        
        self.perfection = perfection
        self.backExtr = be.BackgroundExtractor(self.perfection, showBackImage)
        
        if not backImage == None :
            self.backImage = backImage
        else :
            self.backImage = None
    
    def update(self, frame):
		
        super(self.__class__, self).update(frame)
		
        self.backImage = self.backExtr.feed(self.frame)
        self.diffImage = cv2.absdiff(self.backImage,self.frame)
        #ref, self.diffImage = cv2.threshold(self.diffImage, self.THRESHOLD, 255, cv2.THRESH_BINARY) # HANDLED IN MOTIONTRACKER.PY
        #ret, threshold = cv2.threshold(diffImage, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
        
    def updateBackgroundImage(self, capture, perfection, frameCountLimit):
        ### NOT USED FOR A WHILE, SO CHECK IT BEFORE USING IT
        self.backExtr = be.BackgroundExtractor(perfection)
        if self.capture.isOpened :
            self.backImage = self.backExtr.extract(capture, frameCountLimit)
            if not self.backImage == None:
                cv2.imshow('backImage', self.backImage)
            return self.backImage
        
        return self.backImage

    def setParameter(self, parameter, value, value2=None):
        
        if parameter == 'show_back_image':
            self.backExtr.showBackImage = value
            if value :
                self.backExtr.createTrackbars()
        else :
            super(self.__class__, self).setParameter(parameter, value, value2)
