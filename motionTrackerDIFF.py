import cv2
import numpy as np
import sys
import motionTracker as mt

class MotionTrackerDIFF(mt.MotionTracker):

    def __init__(self, calibration, capture):
        
        super(self.__class__, self).__init__(capture, calibrationFile = calibrationFile, blur=blur)
        #self.THRESHOLD = 10
        self.KERNEL_OPEN = np.ones((1,1),np.uint8)
        self.KERNEL_CLOSE = np.ones((10,10),np.uint8)
        #self.contours = None
        #self.frame = None
        self.prevFrame = None
        self.nextFrame = None
        #self.calibration = calibration

    def update(self, frame):
		if self.prevFrame == None :
            self.prevFrame = frame.copy()
            return None
        elif self.frame == None:
            self.frame = frame.copy()
            return None
        elif self.nextFrame == None:
            self.nextFrame = frame.copy()
        else :
            self.prevFrame = self.frame.copy()
            self.frame = self.nextFrame.copy()
            self.nextFrame = frame.copy()

        d1 = cv2.absdiff(self.prevFrame, self.frame)
        ret, t1 = cv2.threshold(d1, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
        #ret, t1 = cv2.threshold(d1, self.THRESHOLD, 255, cv2.THRESH_BINARY)
        d2 = cv2.absdiff(self.frame, self.nextFrame)
        #ret, t2 = cv2.threshold(d2, self.THRESHOLD, 255, cv2.THRESH_BINARY)
        ret, t2 = cv2.threshold(d2, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
        self.diffImage = cv2.bitwise_and(t1,t2)
        

