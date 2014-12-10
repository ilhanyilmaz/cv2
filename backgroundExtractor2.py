import cv2
import numpy as np
import sys


class BackgroundExtractor():
    """Extracts the background image, given consecutive images."""

    def __init__(self, perfection):
        
        self.FRAMEDIST = 1
        self.THRESHOLD = 3
        self.PERFECTION = perfection
        self.PERCENTAGE = 0.999
        self.minFixedPixel = 1000
        self.backImg = None
        self.prevImg = None
        self.bestRun = None
        self.currentRun = None
        self.nonZeroPoints = 1
        self.showBackImage = True

    def createTrackbars(self):

        cv2.namedWindow('backImage')
        cv2.createTrackbar('perfection','backImage',self.PERFECTION, 250, np.uint)
        cv2.createTrackbar('back_threshold','backImage',self.THRESHOLD, 30, np.uint)
        
    def checkSettings(self):

        if self.showBackImage == False:
            return

        self.PERFECTION = cv2.getTrackbarPos('perfection','backImage')
        self.THRESHOLD = cv2.getTrackbarPos('back_threshold', 'backImage')
        
    def feed(self, image):
        if self.backImg == None:
            self.backImg = image.copy()
            self.prevImg = image.copy()
            height, width = image.shape
            self.bestRun = np.ones((height,width), np.uint8)
            self.currentRun = np.ones((height,width), np.uint8)
            self.minFixedPixel = int(image.size*self.PERCENTAGE)
            #print self.minFixedPixel
            self.createTrackbars()
            if self.showBackImage:
                cv2.imshow("backImage", self.backImg)
            return self.backImg

        self.checkSettings()
        diffImage = cv2.absdiff(self.prevImg,image)
        ret, threshold1 = cv2.threshold(diffImage, self.THRESHOLD, 1, cv2.THRESH_BINARY_INV)
        ret, threshold255 = cv2.threshold(diffImage, self.THRESHOLD, 255, cv2.THRESH_BINARY_INV)

        nonChanged = cv2.bitwise_and(self.currentRun, threshold255)
        self.currentRun = cv2.add(threshold1,nonChanged)

        newBestsMask = cv2.compare(self.currentRun, self.bestRun, cv2.CMP_GE)
        oldBestsMask = cv2.compare(self.currentRun, self.bestRun, cv2.CMP_LT)

        newBestRuns = cv2.bitwise_and(self.currentRun, self.currentRun, mask = newBestsMask)
        oldBestRuns = cv2.bitwise_and(self.bestRun, self.bestRun, mask = oldBestsMask)
        self.bestRun = cv2.add(newBestRuns, oldBestRuns)

        newBackImgPoints = cv2.bitwise_and(image, image,mask = newBestsMask)
        oldBackImgPoints = cv2.bitwise_and(self.backImg, self.backImg, mask = oldBestsMask)
        self.backImg = cv2.add(newBackImgPoints, oldBackImgPoints)

        stablePoints = cv2.compare(self.bestRun, self.PERFECTION, cv2.CMP_GT)
        unstablePoints = cv2.bitwise_not(stablePoints)
        stablePoints = cv2.bitwise_and(stablePoints, self.PERFECTION)
        unstablePoints = cv2.bitwise_and(unstablePoints, self.bestRun)
        self.bestRun = cv2.add(stablePoints, unstablePoints)
        
        self.nonZeroPoints = cv2.countNonZero(stablePoints)
        self.prevImg = image.copy()

        if self.showBackImage:
            cv2.imshow("backImage", self.backImg)
            
        return self.backImg
        
    def extract(self, capture, frameCount):
        count = 0
        while(capture.isOpened and count < frameCount and self.nonZeroPoints < self.minFixedPixel):
            print self.nonZeroPoints 
            count+=1
            i=0
            for i in range(self.FRAMEDIST):
                f,img=capture.read()

            if f==True:
                imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                self.feed(imgGray)
                cv2.imshow("backImage", self.backImg)

            if(cv2.waitKey(27)!=-1):
                capture.release()
                cv2.destroyAllWindows()
                return None

        return self.backImg
