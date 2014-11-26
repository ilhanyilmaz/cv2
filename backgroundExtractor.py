import cv2
import numpy as np
import sys


class BackgroundExtractor():
    """Extracts the background image, given consecutive images."""

    def __init__(self):
        self.FRAMEDIST = 5
        self.THRESHOLD = 20
        self.PERFECTION = 10

        self.backImage = None
        self.checkMat = None
        self.height = 0
        self.width = 0

    def feed(self, image):
        if self.backImage == None:
            self.backImage = image.copy()
            self.height, self.width = image.shape[:2]
            return

        diffImage = cv2.absdiff(self.backImage,image)
        ret, threshold = cv2.threshold(diffImage, self.THRESHOLD, 1, cv2.THRESH_BINARY_INV)
        
        if self.checkMat == None:
            self.checkMat = threshold.copy()
            return

        self.checkMat = cv2.multiply(self.checkMat, threshold)
        self.checkMat = cv2.add(threshold,self.checkMat)
        ret, newFinalizedPoints = cv2.threshold(self.checkMat, self.PERFECTION, 255, cv2.THRESH_BINARY)
        newBackImagePoints = cv2.bitwise_and(image,image,mask = newFinalizedPoints)
        self.backImage = cv2.bitwise_or(newBackImagePoints, self.backImage)

    def extract(self, capture, frameCount):
        count = 0
        while(capture.isOpened and count < frameCount): 
            count+=1
            for i in range(self.FRAMEDIST):
                f,img=capture.read()

            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if f==True:
                self.feed(imgGray)

        return self.backImage
