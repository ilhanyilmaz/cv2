import cv2
import numpy as np
import sys
import motionTracker

class MotionTracker2(motionTracker.MotionTracker):

    def __init__(self):
        self.THRESHOLD = 10
        self.KERNEL_OPEN = np.ones((2,2),np.uint8)
        self.KERNEL_CLOSE = np.ones((10,10),np.uint8)
        self.contours = None
        self.frame = None
        self.prevFrame = None
        self.nextFrame = None

    def getMovingObjects(self, frame):
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
        ret, t1 = cv2.threshold(d1, self.THRESHOLD, 255, cv2.THRESH_BINARY)
        d2 = cv2.absdiff(self.frame, self.nextFrame)
        ret, t2 = cv2.threshold(d2, self.THRESHOLD, 255, cv2.THRESH_BINARY)

        diff = cv2.bitwise_and(t1,t2)
        diff = cv2.morphologyEx(diff, cv2.MORPH_CLOSE, self.KERNEL_CLOSE)
        diff = cv2.morphologyEx(diff, cv2.MORPH_OPEN, self.KERNEL_OPEN)
        cv2.imshow('diff', diff)


        self.contours, hierachy = cv2.findContours(diff, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        return self.contours

    def drawContours(self):
        if self.contours == None:
            return self.frame
        for contour in self.contours:
            area = cv2.contourArea(contour)
            #print area
            if area < 10:
                continue
            x,y,w,h = cv2.boundingRect(contour)
            #print "{0}-{1}/{2}-{3}".format(x,y,w,h)
            cv2.rectangle(self.frame, (x,y), (x+w,y+h), (0,255,0))
        #cv2.drawContours(img,contours,-1,(0,255,0),3)
        return self.frame
