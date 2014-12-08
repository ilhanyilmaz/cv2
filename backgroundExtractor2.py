import cv2
import numpy as np
import sys


class BackgroundExtractor():
    """Extracts the background image, given consecutive images."""

    def __init__(self, perfection):
        self.FRAMEDIST = 1
        self.THRESHOLD = 10
        self.PERFECTION = perfection
        self.PERCENTAGE = 0.995
        self.minFixedPixel = 1000
        self.backImage = None
        self.checkMat = None
        self.nonZeroPoints = 1

    def feed(self, image):
        if self.bestMat == None:
            self.bestMat = image.copy()
            height, width = image.shape
            self.bestRun = np.ones((height,width), np.uint8)
            self.currentRun = np.zeros((height,width), np.uint8)
            self.currentMat = np.zeros((height,width), np.uint8)
            #self.minFixedPixel = int(image.size*self.PERCENTAGE)
            #print self.minFixedPixel
            return

        diffImage = cv2.absdiff(self.bestMat,image)

        ret, threshold1 = cv2.threshold(diffImage, self.THRESHOLD, 1, cv2.THRESH_BINARY_INV)
        ret, bestMask = cv2.threshold(diffImage, self.THRESHOLD, 255, cv2.THRESH_BINARY_INV)
        ret, nonBestMask = cv2.threshold(diffImage, self.THRESHOLD, 255, cv2.THRESH_BINARY)

        self.bestRun = cv2.add(threshold1, self.bestRun)


        diffImage = cv2.absdiff(self.currentMat,image)

        ret, threshold2 = cv2.threshold(diffImage, self.THRESHOLD, 1, cv2.THRESH_BINARY_INV, mask=nonBestMask)
        ret, nonCurrentMask = cv2.threshold(diffImage, self.THRESHOLD, 255, cv2.THRESH_BINARY, mask=nonBestMask)

        self.currentRun = cv2.add(threshold2, self.currentRun)

        newBestsMask = cv2.compare(self.currentRun, self.bestRun, cv2.CMP_GE)

        newBackImagePoints = cv2.bitwise_and(self.bestMat,self.bestMat,mask = bestMask)
        oldBackImagePoints = cv2.bitwise_and(self.backImage, self.backImage, mask = oldImageMask)
        self.bestMat = cv2.add(newBackImagePoints, oldBackImagePoints)


        

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
        self.nonZeroPoints = cv2.countNonZero(totalFixedPoints255)
        
    def extract(self, capture, frameCount):
        count = 0
        while(capture.isOpened and count < frameCount and self.nonZeroPoints < self.minFixedPixel):
            #print self.nonZeroPoints 
            count+=1
            i=0
            for i in range(self.FRAMEDIST):
                f,img=capture.read()

            if f==True:
                imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                self.feed(imgGray)
                cv2.imshow("backImage", self.backImage)

            if(cv2.waitKey(27)!=-1):
                capture.release()
                cv2.destroyAllWindows()
                return None

        return self.backImage
