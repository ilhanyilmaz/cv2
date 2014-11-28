import cv2
import numpy as np
import sys


class BackgroundExtractor():
    """Extracts the background image, given consecutive images."""

    def __init__(self, perfection):
        self.FRAMEDIST = 1
        self.THRESHOLD = 10
        self.PERFECTION = perfection

        self.backImage = None
        self.checkMat = None

    def feed(self, image):
        if self.backImage == None:
            self.backImage = image.copy()
            return

        diffImage = cv2.absdiff(self.backImage,image)

        ret, threshold1 = cv2.threshold(diffImage, self.THRESHOLD, 1, cv2.THRESH_BINARY_INV)
        ret, threshold255 = cv2.threshold(diffImage, self.THRESHOLD, 255, cv2.THRESH_BINARY_INV)

        if self.checkMat == None:
            self.checkMat = threshold1.copy()
            return

        #self.checkMat = cv2.multiply(self.checkMat, threshold)

        ret, fixedPoints255 = cv2.threshold(self.checkMat, self.PERFECTION, 255, cv2.THRESH_BINARY)
        notFixedPoints255 = cv2.bitwise_not(fixedPoints255)

        nonChanged = cv2.bitwise_and(self.checkMat, threshold255)
        nonChangedPlus1 = cv2.add(threshold1,nonChanged)

        ret, newFixedPoints255 = cv2.threshold(nonChangedPlus1, self.PERFECTION, 255, cv2.THRESH_BINARY)
        totalFixedPoints255 = cv2.bitwise_or(fixedPoints255, newFixedPoints255)
        totalNonFixedPoints255 = cv2.bitwise_not(totalFixedPoints255)

        tempMat = cv2.bitwise_or(nonChangedPlus1, totalFixedPoints255)
        ret, oldImageMask = cv2.threshold(tempMat, 1, 255, cv2.THRESH_BINARY)
        newImageMask = cv2.bitwise_not(oldImageMask)

        newBackImagePoints = cv2.bitwise_and(image,image,mask = newImageMask)
        oldBackImagePoints = cv2.bitwise_and(self.backImage, self.backImage, mask = oldImageMask)
        self.backImage = cv2.add(newBackImagePoints, oldBackImagePoints)

        self.checkMat = cv2.bitwise_or(nonChangedPlus1, totalFixedPoints255)

        cv2.imshow("newFinalPoints", self.backImage)
        if(cv2.waitKey(27)!=-1):
            cv2.destroyAllWindows()        



    def extract(self, capture, frameCount):
        count = 0
        while(capture.isOpened and count < frameCount): 
            count+=1
            i=0
            for i in range(self.FRAMEDIST):
                f,img=capture.read()

            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if f==True:
                self.feed(imgGray)

        return self.backImage
