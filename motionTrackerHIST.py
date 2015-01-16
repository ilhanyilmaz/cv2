import cv2
import numpy as np
import sys
import locationEstimator as le
import motionTracker as mt
import glob

class MotionTrackerHist(mt.MotionTracker):

    def __init__(self, capture, posHistFile=None, negHistFile=None, blur=2, filename=None, showTrackerImage=False):
        
        super(self.__class__, self).__init__(capture, showTrackerImage=showTrackerImage, blur=blur)
        #images = []
        self.negHistograms = []
        self.posHistograms = []
        
        if posHistFile != None:
            imageNames = glob.glob("{}*.jpg".format(posHistFile))
            print imageNames
            for fname in imageNames:
                print "Opening: {}".format(fname)
                image = cv2.imread(fname)
                self.addHistogram(image, '+')
            
        if negHistFile != None:
            imageNames = glob.glob("{}*.jpg".format(negHistFile))
            for fname in imageNames:
                print "Opening: {}".format(fname)
                image = cv2.imread(fname)
                self.addHistogram(image, '-')
            
    def update(self, frame):
		
        super(self.__class__, self).update(frame)
        diffImageRGB = self.removeBackground(frame.copy())
        self.diffImage = cv2.cvtColor(diffImageRGB, cv2.COLOR_BGR2GRAY)
        
    def addHistogram(self, crop, posNeg):
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array((0., 10.,10.)), np.array((180.,256.,256.)))
        roiHist = cv2.calcHist([hsv], [0,1], mask, [180, 256], [0, 180, 0, 256])
        cv2.normalize(roiHist, roiHist,0,255,cv2.NORM_MINMAX)
        if posNeg == '+':
            self.posHistograms.append(roiHist)
        else :
            self.negHistograms.append(roiHist)
        
    def removeBackground(self, image):
        discValue = 10
        threshold = 1
        hsvt = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        for roiHist in self.negHistograms:
            dst = cv2.calcBackProject([hsvt],[0,1],roiHist,[0,180,0,256],1)
            cv2.imshow('dst', dst)
            disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(discValue,discValue))
            cv2.filter2D(dst, -1,disc,dst)
            ret,thresh = cv2.threshold(dst,threshold,255,cv2.THRESH_BINARY_INV)
            thresh = cv2.merge((thresh,thresh,thresh))
            image = cv2.bitwise_and(image,thresh)
        
        
        for roiHist in self.posHistograms:
            dst = cv2.calcBackProject([hsvt],[0,1],roiHist,[0,180,0,256],1)
            #cv2.imshow('dst', dst)
            disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(discValue,discValue))
            cv2.filter2D(dst, -1,disc,dst)
            ret,thresh = cv2.threshold(dst,threshold,255,cv2.THRESH_BINARY)
            thresh = cv2.merge((thresh,thresh,thresh))
            image = cv2.bitwise_and(image,thresh)
            
            
            #res = np.hstack((thresh,res))
        
        cv2.imshow('backProj', image)
        return image
