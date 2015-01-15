import cv2
import numpy as np
import sys
import locationEstimator as le
import motionTracker as mt
import glob

class MotionTrackerHist(mt.MotionTracker):

    def __init__(self, capture, histogramFile=None, blur=2, filename=None, showTrackerImage=False):
        
        super(self.__class__, self).__init__(capture, showTrackerImage=showTrackerImage, blur=blur)
        #images = []
        self.histograms = []
        imageNames = glob.glob("{}*.jpg".format(histogramFile))

        print histogramFile
        for fname in imageNames:
            print "Opening: {}".format(fname)
            image = cv2.imread(fname)
            self.addHistogram(image)
            #images.append(image)
            #cv2.imshow(fname, image)
        
    def update(self, frame):
		
        super(self.__class__, self).update(frame)
        self.diffImage = self.removeBackground(frame.copy())
        #absdiff(backImg, frame, diffImg);   // find out how much pixels are changed
        #self.diffImage = cv2.absdiff(self.backImage,self.frame)
        
    def addHistogram(self, crop):
        height, width, depth = crop.shape
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array((0., 10.,10.)), np.array((180.,256.,256.)))
        roiHist = cv2.calcHist([hsv], [0,1], mask, [180, 256], [0, 180, 0, 256])
        cv2.normalize(roiHist, roiHist,0,255,cv2.NORM_MINMAX)
        self.histograms.append(roiHist)
        
    def removeBackground(self, image):
        discValue = 2
        threshold = 1
        hsvt = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        for roiHist in self.histograms:
            dst = cv2.calcBackProject([hsvt],[0,1],roiHist,[0,180,0,256],1)
            #cv2.imshow('dst', dst)
            disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(discValue,discValue))
            cv2.filter2D(dst, -1,disc,dst)
            ret,thresh = cv2.threshold(dst,threshold,255,cv2.THRESH_BINARY_INV)
            thresh = cv2.merge((thresh,thresh,thresh))
            image = cv2.bitwise_and(image,thresh)
            
            #res = np.hstack((thresh,res))
        
        cv2.imshow('backProj', image)
        return image
