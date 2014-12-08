import cv2
import numpy as np
import sys
import locationEstimator as le
import motionTracker as mt

class MotionTrackerMOG(mt.MotionTracker):

    def __init__(self, calibration, capture, backImage = None):
        super(self.__class__,self).__init__(calibration, capture, backImage)
        if backImage == None :
                self.updateBackgroundImage(capture, 40)
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
