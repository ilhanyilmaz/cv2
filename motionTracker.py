import cv2
import numpy as np
import sys
import locationEstimator as le

class MotionTracker(object):

    def __init__(self, capture, calibrationFile = None, blur = 2):
		
        self.KERNEL_OPEN = np.ones((1,1),np.uint8)
        self.KERNEL_CLOSE = np.ones((12,5),np.uint8)
        self.blurValue = blur
        self.THRESHOLD = 22
        self.contours = None
        self.frame = None
        self.capture = capture
        self.showPositions = True
        self.showTracker = True
        self.showDiffImage = True
        self.diffImage = None
        if not calibrationFile == None :
            self.estimator = le.LocationEstimator(calibrationFile)
            
        self.createDiffImageWindow()
    
    
    def getMovingObjects(self):
        
        #kernel = np.ones((8,8),np.uint8)
        #threshold = cv2.erode(threshold,kernel,iterations = 1)
        #threshold = cv2.dilate(threshold,kernel,iterations = 1)
        if self.diffImage == None:
			return None

        #if self.showDiffImage:
		#	cv2.imshow('diff image', self.diffImage)
        #threshold = cv2.morphologyEx(self.diffImage, cv2.MORPH_OPEN, self.KERNEL_OPEN)
        #threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, self.KERNEL_CLOSE)
        threshold = cv2.erode(self.diffImage,self.KERNEL_OPEN,iterations = 1)
        threshold = cv2.dilate(threshold,self.KERNEL_OPEN,iterations = 1)
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, self.KERNEL_CLOSE)
        
        if self.showDiffImage:
			cv2.imshow('diff image', self.getDilatedDiffImage(self.frame))
			
        self.contours, hierachy = cv2.findContours(threshold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        return self.contours
        
    def update(self, frame):
		
        self.frame = frame.copy()
        self.frame = cv2.blur(self.frame, (self.blurValue,self.blurValue))

    def getDilatedDiffImage(self, frame):

        threshold = cv2.morphologyEx(self.diffImage, cv2.MORPH_OPEN, self.KERNEL_OPEN)
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, self.KERNEL_CLOSE)
        #threshold = cv2.erode(self.diffImage,self.KERNEL_OPEN,iterations = 1)
        #threshold = cv2.dilate(threshold,self.KERNEL_CLOSE,iterations = 1)
        return cv2.bitwise_and(frame, frame, mask = threshold)
		
    def getObjectPositions(self):
        if self.contours == None :
            return
        posImage = np.zeros((500,500,3), np.uint8)
        #i=1
        for contour in self.contours:
            area = cv2.contourArea(contour)
            #print area
            if area < 10:
                continue
            x,y,w,h = cv2.boundingRect(contour)
            objPos = self.estimator.get3dCoordinates(x+w/2, y+h)
            cv2.circle(posImage, (int(objPos[0]),int(objPos[1])), 10, (0,255,0),-1)
            #if i==1 :
                #print 'obj{0}= {1}-{2}'.format(i, str(x+w/2), str(y+h))
                #print self.estimator.get3dCoordinates(x+w/2, y+h)
            #i+=1
        if self.showPositions:
            cv2.imshow("positions", posImage)

    def drawContours(self):
        if self.contours == None:
            return self.frame
        for contour in self.contours:
            area = cv2.contourArea(contour)
            #print area
            if area < 10:
                continue
            x,y,w,h = cv2.boundingRect(contour)
            cv2.rectangle(self.frame, (x,y), (x+w,y+h), (0,255,0))
            #cv2.drawContours(img,contours,-1,(0,255,0),3)
        if self.showTracker:
			cv2.imshow('tracker', self.frame)
        return self.frame
        
    def setParameter(self, parameter, value, value2=None):
        
        if parameter == 'blur':
            self.blurValue = value
        elif parameter == 'threshold':
            self.THRESHOLD = value
        elif parameter == 'm_open':
            self.KERNEL_OPEN = np.ones((value,value),np.uint8)
            #print self.KERNEL_OPEN
        elif parameter == 'm_close':
            self.KERNEL_CLOSE = np.ones((value2,value),np.uint8)
            #print self.KERNEL_CLOSE
        elif parameter == 'show_positions':
            self.showPositions = value
        elif parameter == 'show_diff_image':
            self.showDiffImage = value
        elif parameter == 'show_tracker':
            self.showTracker = value
            
    def createDiffImageWindow(self):
    
        cv2.namedWindow('diff image')
        cv2.createTrackbar('blur','diff image',self.blurValue, 10, np.uint)
        cv2.createTrackbar('m_open','diff image',len(self.KERNEL_OPEN[:1]), 5, np.uint)
        j,i=self.KERNEL_CLOSE.shape
        cv2.createTrackbar('m_close_x','diff image',i, 20, np.uint)
        cv2.createTrackbar('m_close_y','diff image',j, 20, np.uint)
        cv2.createTrackbar('threshold','diff image',self.THRESHOLD, 100, np.uint)

    def diffImageWindowSettings(self):
		
        if not self.showDiffImage:
			return
			
        value = cv2.getTrackbarPos('blur','diff image')
        if value == 0:
            value = 1
        if value != self.blurValue :
            self.setParameter('blur', value)
                                   
        value = cv2.getTrackbarPos('threshold','diff image')
        if value != self.THRESHOLD :
            self.setParameter('threshold', value)

        j,i=self.KERNEL_OPEN.shape
        value = cv2.getTrackbarPos('m_open','diff image')
        if value == 0:
            value = 1
        if value != i :
            self.setParameter('m_open', value)
        
        value = cv2.getTrackbarPos('m_close_x','diff image')
        if value == 0:
            value = 1
        v2 = cv2.getTrackbarPos('m_close_y','diff image')
        if v2 == 0:
            v2 = 1
        self.setParameter('m_close', value, value2=v2)
        
        
    def checkSettings(self):
    
        if self.showDiffImage :
            self.diffImageWindowSettings()
            
            
