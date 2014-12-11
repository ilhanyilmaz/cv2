import cv2
import numpy as np
import sys
import locationEstimator as le

class MotionTracker(object):

    def __init__(self, capture, calibrationFile = None, blur = 5):
		
        self.KERNEL_OPEN = np.ones((1,1),np.uint8)
        self.KERNEL_CLOSE = np.ones((10,10),np.uint8)
        self.blurValue = blur
        self.THRESHOLD = 20
        self.contours = None
        self.frame = None
        self.capture = capture
        self.showPositions = True
        self.showTracker = True
        self.showDiffImage = True
        self.diffImage = None
        if not calibrationFile == None :
            self.estimator = le.LocationEstimator(calibrationFile)
            
        self.createTrackerWindow()
    
    
    def getMovingObjects(self):
        
        #kernel = np.ones((8,8),np.uint8)
        #threshold = cv2.erode(threshold,kernel,iterations = 1)
        #threshold = cv2.dilate(threshold,kernel,iterations = 1)
        if self.diffImage == None:
			return None

        if self.showDiffImage:
			cv2.imshow('diff image', self.diffImage)
        threshold = cv2.morphologyEx(self.diffImage, cv2.MORPH_OPEN, self.KERNEL_OPEN)
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, self.KERNEL_CLOSE)

        self.contours, hierachy = cv2.findContours(threshold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        return self.contours
        
    def update(self, frame):
		
        self.frame = frame.copy()
        self.frame = cv2.blur(self.frame, (self.blurValue,self.blurValue))

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
        
    def setParameter(self, parameter, value):
        
        if parameter == 'blur':
            self.blurValue = value
        elif parameter == 'threshold':
            self.THRESHOLD = value
        elif parameter == 'm_open':
            self.KERNEL_OPEN = np.ones((value,value),np.uint8)
        elif parameter == 'm_close':
            self.KERNEL_CLOSE = np.ones((value,value/2),np.uint8)
        elif parameter == 'show_positions':
            self.showPositions = value
        elif parameter == 'show_diff_image':
            self.showDiffImage = value
        elif parameter == 'show_tracker':
            self.showTracker = value
            
    def createTrackerWindow(self):
    
        cv2.namedWindow('tracker')
        cv2.createTrackbar('blur','tracker',self.blurValue, 10, np.uint)
        print len(self.KERNEL_OPEN[:1])
        cv2.createTrackbar('m_open','tracker',len(self.KERNEL_OPEN[:1]), 5, np.uint)
        cv2.createTrackbar('m_close','tracker',len(self.KERNEL_CLOSE[:1]), 20, np.uint)
        cv2.createTrackbar('threshold','tracker',self.THRESHOLD, 100, np.uint)

    def trackerWindowSettings(self):
		
        if not self.showTracker:
			return
			
        value = cv2.getTrackbarPos('blur','tracker')
        if value == 0:
            value = 1
        if value != self.blurValue :
            self.setParameter('blur', value)
                                   
        value = cv2.getTrackbarPos('threshold','tracker')
        if value != self.THRESHOLD :
            self.setParameter('threshold', value)

        value = cv2.getTrackbarPos('m_open','tracker')
        if value == 0:
            value = 1
        if value != len(self.KERNEL_OPEN[:1]) :
            self.setParameter('m_open', value)

        value = cv2.getTrackbarPos('m_close','tracker')
        if value == 0:
            value = 1
        if value != len(self.KERNEL_CLOSE[:1]):
            self.setParameter('m_close', value)
        
    def checkSettings(self):
    
        if self.showTracker :
            self.trackerWindowSettings()
            
            
