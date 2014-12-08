import cv2
import numpy as np
import sys
import locationEstimator as le
import motionTracker as mt


class MotionTrackerBACK(mt.MotionTracker):
    
    def __init__(self, calibrationFile, capture, backImage = None):
        super(self.__class__, self).__init__(calibrationFile, capture, backImage)
        if backImage == None :
            self.updateBackgroundImage(capture, 40)
    
    def getMovingObjects(self, frame):
        #imgGray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.frame = frame.copy()
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
