import numpy as np
import math

class LocationEstimator():
    def __init__(self, calibrationfile):
        self.calibration = np.load(calibrationfile)
        #print 'Mtx:'
        #print self.calibration['mtx']
        #print 'rvecs:'
        #print self.calibration['rvecs']
        #print 'tvecs:'
        #print self.calibration['tvecs']
        #mtx= np.dot(self.calibration['mtx'], self.calibration['rvecs'])
        rotXMtx = self.rotXMtx(self.calibration['rvecs'][0,0])
        #print rotXMtx
        rotYMtx = self.rotYMtx(self.calibration['rvecs'][0,1])
        #print rotYMtx
        rotZMtx = self.rotZMtx(self.calibration['rvecs'][0,2])
        #print rotZMtx
        tVecs = self.calibration['tvecs'][0]
        rVecs = np.array([self.calibration['rvecs'][0,0],self.calibration['rvecs'][0,1], self.calibration['rvecs'][0,0]])
        mtx = np.dot(rotZMtx,rotYMtx)
        mtx = np.dot(mtx, rotXMtx)
        mtx = np.concatenate((mtx, tVecs), axis=1)
        #print mtx
        self.mtx = np.dot(self.calibration['mtx'], mtx)
        #print self.mtx
        print "mtx:\n{}".format(mtx)
        print "tvecs: {}".format(tVecs)
        print "rvecs: {}".format(rVecs)

    def rotXMtx(self,a):
        sina = np.sin(a)
        cosa = np.cos(a)
        mtx = np.zeros(9).reshape(3,3)
        mtx[0,0] = 1
        mtx[1,1] = cosa[0]
        mtx[1,2] = -sina[0]
        mtx[2,1] = sina[0]
        mtx[2,2] = cosa[0]
        return mtx

    def rotYMtx(self,a):
        sina = np.sin(a)
        cosa = np.cos(a)
        mtx = np.zeros(9).reshape(3,3)
        mtx[0,0] = cosa[0]
        mtx[0,2] = sina[0]
        mtx[1,1] = 1
        mtx[2,0] = -sina[0]
        mtx[2,2] = cosa[0]
        return mtx

    def rotZMtx(self,a):
        sina = np.sin(a)
        cosa = np.cos(a)
        mtx = np.zeros(9).reshape(3,3)
        mtx[0,0] = cosa
        mtx[0,1] = -sina[0]
        mtx[1,0] = sina[0]
        mtx[1,1] = cosa[0]
        mtx[2,2] = 1
        return mtx

    def get3dCoordinates(self, u, v):
        eq = np.array([[self.mtx[0,0], self.mtx[0,2]],[self.mtx[1,0],self.mtx[1,2]]])
        re = np.array([u-self.mtx[0,3], v-self.mtx[1,3]])
        xyres= np.linalg.solve(eq,re)
        return xyres
