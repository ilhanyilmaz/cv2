import numpy as np
import math
import cv2

class LocationEstimator():
    def __init__(self, calibrationfile, showPositions=False):
        self.calibration = np.load(calibrationfile)
        self.showPositions = showPositions
        
        self.calcMatrix()
        self.scaleFactor = 1
        self.offsetX = 0.
        self.offsetY = 0.
        self.objPositions = []

        self.defineRange(640,480,500)
        
        if showPositions:
            self.initWindow()
        

    def calcMatrix(self):
        rVecs = self.calibration['rvecs'][0]
        mtx, jacobian = cv2.Rodrigues(rVecs)
        #print 'rVecs:'
        #print rVecs
        tVecs = self.calibration['tvecs'][0]
        mtx = np.concatenate((mtx, tVecs), axis=1)
        #print 'tVecs:'
        #print tVecs
        #print "mtx:\n{}".format(self.calibration['mtx'])
        self.mtx = np.dot(self.calibration['mtx'], mtx)
        #print "tvecs: {}".format(tVecs)
        #print "rvecs: {}".format(rVecs)
        #print "newMtx:\n{}".format(self.calibration['newMtx'])
        #print "result:\n{}".format(mtx)
        #print "new matrix:"
        #print self.mtx
        
    def initWindow(self):
        cv2.namedWindow('positions')
        print self.calibration['rvecs'][0][0]
        cv2.createTrackbar('rvec0','positions',int(self.calibration['rvecs'][0][0]*100), 314, np.uint8)
        cv2.createTrackbar('rvec1','positions',self.calibration['rvecs'][0][1], 314, np.uint8)
        cv2.createTrackbar('rvec2','positions',self.calibration['rvecs'][0][2], 314, np.uint8)
        
    def defineRange(self,w,h,range):
        imageCorners = np.array([[0,0],[w,0],[0,h],[w,h]])
        minX=999999
        minY=999999
        maxX=-999999
        maxY=-999999
        for pt in imageCorners:
            xyres = self.get3dCoordinates(pt[0],pt[1])
            if xyres[0] > maxX:
                maxX = xyres[0]
            if xyres[0] < minX:
                minX = xyres[0]
            if xyres[1] > maxY:
                maxY = xyres[1]
            if xyres[1] < minY:
                minY = xyres[1]
        self.offsetX = minX
        self.offsetY = minY
        diffX = maxX - minX
        #diffY = maxY - minY
        self.scaleFactor= 1.0/diffX * range
        #print str(minX) + "-" + str(maxX)
            
    def get3dCoordinates(self, u, v):
        #u=u-320
        #v=v-240
        eq = np.array([[self.mtx[0,0], self.mtx[0,2]],[self.mtx[1,0],self.mtx[1,2]]])
        re = np.array([u-self.mtx[0,3], v-self.mtx[1,3]])
        xyres= np.linalg.solve(eq,re)
        xyres[0] = (xyres[0]-self.offsetX) * self.scaleFactor
        xyres[1] = (xyres[1]-self.offsetY) * self.scaleFactor
        return xyres
        
    def getContours3dCoordinates(self, contours):
        if contours == None :
            return None
        
        self.objPositions = []
        for contour in contours:
            area = cv2.contourArea(contour)
            #print area
            if area < 10:
                continue
            x,y,w,h = cv2.boundingRect(contour)
            objPos = self.get3dCoordinates(x+w/2, y+h)
            self.objPositions.append(objPos)
        
        if self.showPositions:
            self.updateImage()
            
    def updateImage(self):
        posImage = np.zeros((500,500,3), np.uint8)
        
        for objPos in self.objPositions:
            cv2.circle(posImage, (int(objPos[0]),int(objPos[1])), 10, (0,255,0),-1)
        
        cv2.imshow("positions", posImage)
