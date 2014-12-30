import numpy as np
import math
import cv2

class LocationEstimator():
    def __init__(self, calibrationfile, showPositions=False):
        
        
        self.calibration = np.load(calibrationfile)
        self.rvecs = np.array(self.calibration['rvecs'])
        self.tvecs = np.array(self.calibration['tvecs'])
        
        
        print self.rvecs
        print self.tvecs
        print self.calibration['mtx']
        
        self.rvecs = np.array([[[self.celciusToRadian(281)],[self.celciusToRadian(191)],[self.celciusToRadian(96)]]], np.float32)
        self.tvecs = np.array([[[3977],[1958],[-9659]]], np.float32)
        #self.tvecs = np.array([[[-10000],[2000],[10000]]], np.float32)
        self.mtx = np.array(self.calibration['mtx'])
        self.mtx[0,2]=320
        self.mtx[1,2]=240
        
        
        self.showPositions = showPositions
        
        self.calcMatrix()
        self.scaleFactor = 1
        self.offsetX = 0.
        self.offsetY = 0.
        self.objPositions = []

        #self.defineRange(640,480,500)
        
        if showPositions:
            self.initWindow()
        

    def calcMatrix(self):
        rVecs = self.rvecs[0]
        mtx, jacobian = cv2.Rodrigues(rVecs)
        #print 'rVecs:'
        #print rVecs
        tVecs = self.tvecs[0]
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
        
    def radianToCelcius(self,radian):
        celcius = int(radian/np.pi*180.0)
        if celcius < 0:
            celcius = 360 + celcius
        return celcius
    
    def celciusToRadian(self, celcius):
        radian = celcius * np.pi / 180.0
        if radian > np.pi:
            radian = radian - 2*np.pi
        return radian
        
    def initWindow(self):
        
        cv2.namedWindow('positions')
        cv2.createTrackbar('scale','positions',self.scaleFactor, 100, np.int8)
        cv2.createTrackbar('offsetX','positions',int(self.offsetX+10000), 20000, np.int8)
        cv2.createTrackbar('offsetY','positions',int(self.offsetY+10000), 20000, np.int8)
        cv2.createTrackbar('rvec0','positions',self.radianToCelcius(self.rvecs[0][0]), 360, np.uint8)
        cv2.createTrackbar('rvec1','positions',self.radianToCelcius(self.rvecs[0][1]), 360, np.uint8)
        cv2.createTrackbar('rvec2','positions',self.radianToCelcius(self.rvecs[0][2]), 360, np.uint8)
        cv2.createTrackbar('tvec0','positions',int(self.tvecs[0][0]+25000), 50000, np.int8)
        cv2.createTrackbar('tvec1','positions',int(self.tvecs[0][1]), 4000, np.int8)
        cv2.createTrackbar('tvec2','positions',int(self.tvecs[0][2]+25000), 50000, np.int8)
        
        
    def checkSettings(self):
        
        change = False
        self.scaleFactor = cv2.getTrackbarPos('scale','positions')
        self.offsetX = cv2.getTrackbarPos('offsetX','positions')-10000
        self.offsetY = cv2.getTrackbarPos('offsetY','positions')-10000
        
        value = self.celciusToRadian(cv2.getTrackbarPos('rvec0','positions'))
        if value != self.rvecs[0][0]:
            change = True
            self.rvecs[0][0] = value
        value = self.celciusToRadian(cv2.getTrackbarPos('rvec1','positions'))
        if value != self.rvecs[0][1]:
            change = True
            self.rvecs[0][1] = value
        value = self.celciusToRadian(cv2.getTrackbarPos('rvec2','positions'))
        if value != self.rvecs[0][2]:
            change = True
            self.rvecs[0][2] = value
        
        value = (cv2.getTrackbarPos('tvec0','positions'))-25000
        if value != self.tvecs[0][0]:
            change = True
            self.tvecs[0][0] = value
        value = (cv2.getTrackbarPos('tvec1','positions'))
        if value != self.tvecs[0][1]:
            change = True
            self.tvecs[0][1] = value
        value = (cv2.getTrackbarPos('tvec2','positions'))-25000
        if value != self.tvecs[0][2]:
            change = True
            self.tvecs[0][2] = value
        
        if change:
            self.calcMatrix()
            #self.defineRange(640,480,500)
    
    """    
    def defineRange(self,w,h,size):
        
        imageCorners = np.array([[0,0],[w,0],[0,h],[w,h]])
        minX=9999999
        minY=9999999
        maxX=-9999999
        maxY=-9999999
        for pt in imageCorners:
            xyres = self.get3dCoordinates(pt[0],pt[1])
            print xyres
            if xyres[0] > maxX:
                maxX = xyres[0]
            if xyres[0] < minX:
                minX = xyres[0]
            if xyres[1] > maxY:
                maxY = xyres[1]
            if xyres[1] < minY:
                minY = xyres[1]
        self.offsetX = (maxX + minX) / 2 - size/self.scaleFactor
        self.offsetY = (maxY + minY) / 2 - size/self.scaleFactor
        diffX = maxX - minX
        diffY = maxY - minY
        if diffX < diffY :
            self.scaleFactor= 1.0/diffX * size
        else :
            self.scaleFactor= 1.0/diffY * size
        #print str(minX) + "-" + str(maxX)
        #print str(minY) + "-" + str(maxY)"""

    def get3dCoordinates(self, u, v):
        m00 = self.mtx[0,0]
        m01 = self.mtx[0,1]
        m03 = self.mtx[0,3]
        m10 = self.mtx[1,0]
        m11 = self.mtx[1,1]
        m13 = self.mtx[1,3]
        m20 = self.mtx[2,0]
        m21 = self.mtx[2,1]
        m23 = self.mtx[2,3]
        
        m00_m20u = m00 - m20*u
        m01_m21u = m01 - m21*u
        m10_m20v = m10 - m20*v
        m11_m21v = m11 - m21*v
        m23u_m03 = m23*u - m03
        m23v_m13 = m23*v - m13
        
        eq = np.array([[m00_m20u, m01_m21u],[m10_m20v,m11_m21v]])
        print "uv: \n{}:{}".format(u,v)
        re = np.array([m23u_m03, m23v_m13])
        xyres= np.linalg.solve(eq,re)
        return xyres
    """
    def get3dCoordinates(self, u, v):
        #u=u-320
        #v=v-240
        s = self.mtx[2,3]
        #print "mtx: \n{}".format(self.mtx)
        eq = np.array([[self.mtx[0,0], self.mtx[0,1]],[self.mtx[1,0],self.mtx[1,1]]])
        #eq = np.array([[self.mtx[0,0], self.mtx[0,2]],[self.mtx[1,0],self.mtx[1,2]]])
        #print "uv: \n{}:{}".format(u,v)
        re = np.array([u*s-self.mtx[0,3], v*s-self.mtx[1,3]])
        xyres= np.linalg.solve(eq,re)
        #xyres[0] = xyres[0] * self.scaleFactor + self.offsetX
        #xyres[1] = xyres[1] * self.scaleFactor + self.offsetY
        return xyres
    """
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
            #print objPos
            self.objPositions.append(objPos)
        
        if self.showPositions:
            self.updateImage()
    
    def updateImage(self):
        self.checkSettings()
        posImage = np.zeros((500,500,3), np.uint8)
        size = 500
        for objPos in self.objPositions:
            print objPos
            if (objPos[0]/40+250) > 0 and (objPos[0]/40+250)<size and (objPos[1]/40+250) > 0 and (objPos[1]/40+250)<size:
                cv2.circle(posImage, (int(objPos[0]/40+250),int(250-objPos[1]/40)), 10, (0,255,0),-1)
        
        cv2.imshow("positions", posImage)

    def get2dCoordinates(self, point3d):
        #u=u-320
        #v=v-240
        #print self.mtx
        #print point3d
        uvPoint = np.dot(self.mtx, point3d)
        #print uvPoint[2][0]
        #return (int(uvPoint[0][0]),int(uvPoint[1][0]))
        return (int(uvPoint[0][0]/uvPoint[2][0]),int(uvPoint[1][0]/uvPoint[2][0]))
    
    def draw3dAxis(self, image):
        
        pCenter = np.array([[0],[0],[0],[1]],np.float32)
        pX = np.array([[1000],[0],[0],[1]],np.float32)
        pY = np.array([[0],[1000],[0],[1]],np.float32)
        pZ = np.array([[0],[0],[1000],[1]],np.float32)
        
        pCuv = self.get2dCoordinates(pCenter)
        pXuv = self.get2dCoordinates(pX)
        pYuv = self.get2dCoordinates(pY)
        pZuv = self.get2dCoordinates(pZ)
        
        
        #print 'pX: ' + str(pCuv)
        print 'C: ' + str(self.get3dCoordinates(pCuv[0], pCuv[1]))
        print 'X: ' + str(self.get3dCoordinates(pXuv[0], pXuv[1]))
        print 'Y: ' + str(self.get3dCoordinates(pYuv[0], pYuv[1]))
        
        #print pXuv
        #print pYuv
        #print pZuv
        
        
        cv2.line(image, pCuv, pXuv, (0,0,255), 3)
        cv2.line(image, pCuv, pYuv, (0,255,0), 3)
        cv2.line(image, pCuv, pZuv, (255,0,0), 3)
        
        return image
