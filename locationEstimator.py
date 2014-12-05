import numpy as np
import math
import cv2

class LocationEstimator():
    def __init__(self, calibrationfile):
        self.calibration = np.load(calibrationfile)
        #print 'Mtx:'
        #print self.calibration['mtx']
        #print 'rvecs:'
        #print self.calibration['rvecs']
        #print 'tvecs:'
        #print self.calibration['tvecs']
        rVecs = self.calibration['rvecs'][0]
        mtx, jacobian = cv2.Rodrigues(rVecs)
        tVecs = self.calibration['tvecs'][0]
        mtx = np.concatenate((mtx, tVecs), axis=1)
        #print "mtx:\n{}".format(self.calibration['mtx'])
        self.mtx = np.dot(self.calibration['mtx'], mtx)

        self.scaleFactor = 1
        self.offsetX = 0.
        self.offsetY = 0.

        self.defineRange(640,480,500)

        #print self.mtx
        #print "tvecs: {}".format(tVecs)
        #print "rvecs: {}".format(rVecs)
        #print "newMtx:\n{}".format(self.calibration['newMtx'])
        #print "result:\n{}".format(mtx)

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
