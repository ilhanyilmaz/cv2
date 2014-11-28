import cv2
import numpy as np
import sys


class MotionTracker():

    def __init__(self, backImage):
        self.THRESHOLD = 20
        self.backImage = backImage
        self.KERNEL_OPEN = np.ones((2,2),np.uint8)
        self.KERNEL_CLOSE = np.ones((10,10),np.uint8)
        self.contours = None
        self.frame = None

    def getMovingObjects(self, frame):
        #imgGray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.frame = frame.copy()
        diffImage = cv2.absdiff(self.backImage,self.frame)
        ret, threshold = cv2.threshold(diffImage, self.THRESHOLD, 255, cv2.THRESH_BINARY)
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, self.KERNEL_OPEN)
        #threshold = cv2.erode(threshold,kernel,iterations = 1)
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, self.KERNEL_CLOSE)
        #threshold = cv2.dilate(threshold,kernel,iterations = 1)
        #kernel = np.ones((8,8),np.uint8)
        #threshold = cv2.erode(threshold,kernel,iterations = 1)
        self.contours, hierachy = cv2.findContours(threshold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        return self.contours

    def drawContours(self, image):
        for contour in self.contours:
            area = cv2.contourArea(contour)
            #print area
            if area < 10:
                continue
            x,y,w,h = cv2.boundingRect(contour)
            #print "{0}-{1}/{2}-{3}".format(x,y,w,h)
            cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0))
        #cv2.drawContours(img,contours,-1,(0,255,0),3)
        return image