import cv2
import numpy as np
import sys
import locationEstimator as le

class MotionTracker(object):

    def __init__(self, capture, showTrackerImage = False, calibrationFile = None, blur = 2):
		
        self.KERNEL_OPEN = np.ones((1,1),np.uint8)
        self.KERNEL_CLOSE = np.ones((12,5),np.uint8)
        self.blurValue = blur
        self.THRESHOLD = 40
        self.THRESHOLD2 = 17
        self.contours = None
        self.frame = None
        self.capture = capture
        self.showPositions = False
        self.showTracker = showTrackerImage
        self.showDiffImage = False
        self.diffImage = None
        if not calibrationFile == None :
            self.estimator = le.LocationEstimator(calibrationFile)
        if self.showDiffImage:
            self.createDiffImageWindow()
        self.rectangles = None
    #return a dict of row: index with value in row > 0 
    """def first_true1(a):
    
        di={}
        for i in range(len(a)):
            idx=np.where(a[i]>0)
            try:
                di[i]=idx[0][0]
            except IndexError:
                di[i]=None    
    return di 
    
    def subThreshold(threshold):
        h,w = threshold.shape
        for i in range(w):
            l = i
            r = w-i
            if threshold(:)
    """
    def findNonZeroBoundary(self,roi,x,y):
        h,w = roi.shape
        #print roi
        lFound = False
        rFound = False
        l=0
        r=w-1
        for i in range(w):
            if not lFound:
                l = i
            if not rFound:
                r = w-i-1
            if np.sum(roi[:,l]) > 0:
                lFound = True
            if np.sum(roi[:,r]) > 0:
                rFound = True
            if lFound and rFound:
                break
                
        uFound = False
        bFound = False
        u=0
        b=h-1
        for i in range(h):
            if not uFound:
                u = i
            if not bFound:
                b = h-i-1
            if np.sum(roi[u,:]) > 0:
                uFound = True
            if np.sum(roi[b,:]) > 0:
                bFound = True
            if uFound and bFound:
                break
        
        #if l!=0 or r!=w or u!=w or b!=h:
        #    print "{0}-{1}:{2}-{3}".format(l,r,u,b)
        
        return [l+x,u+y,r+x,b+y]
        
    def getMovingObjects(self):
        
        if self.diffImage == None:
			return None

        ref, tDiffImage = cv2.threshold(self.diffImage, self.THRESHOLD, 128, cv2.THRESH_BINARY)
        ref, tDiffImage2 = cv2.threshold(self.diffImage, self.THRESHOLD2, 127, cv2.THRESH_BINARY)
        threshold = tDiffImage + tDiffImage2
        
        
            
        #threshold = cv2.morphologyEx(self.diffImage, cv2.MORPH_OPEN, self.KERNEL_OPEN)
        #threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, self.KERNEL_CLOSE)
        
        
        #threshold = cv2.morphologyEx(self.diffImage, cv2.MORPH_OPEN, self.KERNEL_OPEN)
        threshold = cv2.erode(threshold,self.KERNEL_OPEN,iterations = 1)
        threshold = cv2.dilate(threshold,self.KERNEL_OPEN,iterations = 1)
        
        if self.showDiffImage:
			cv2.imshow('diff image', threshold)
            
        # CONVOLUTION
        #disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,6))
        #cv2.filter2D(tDiffImage,-1,disc,threshold)
        #ret,threshold = cv2.threshold(threshold,10,255,0)
        threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, self.KERNEL_CLOSE)
        
        
        
        
			
        # libopencv 2.4.9
        self.contours, hierachy = cv2.findContours(threshold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #return self.contours
        # libopencv 2.4.9
        #image, self.contours, hierachy = cv2.findContours(threshold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        
        self.rectangles = []
        for contour in self.contours:
            area = cv2.contourArea(contour)
            if area < 10:
                continue
            
            
            x,y,w,h = cv2.boundingRect(contour)
            rect= cv2.boundingRect(contour)
            conDiffImg = tDiffImage[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]]
            self.rectangles.append(self.findNonZeroBoundary(conDiffImg,x,y))
            
            """if cv2.isContourConvex(contour):
                if len(contour) > 5:
                    (x,y),(MA,ma),angle = cv2.fitEllipse(contour)
                    print "{0}-{1}".format(MA,ma)
            """
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
		
    """def getObjectPositions(self):
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
    """
    def getBiggestMovingObjectContour(self):
        if self.contours == None :
            return None
        
        maxArea = 0
        biggestContour = None
        i=0
        pos = 0
        for contour in self.contours:
            area = cv2.contourArea(contour)
            if area > maxArea:
                maxArea = area
                biggestContour = contour
                pos = i
            i+=1

        if not biggestContour == None:
            print 'alo'
            return biggestContour
        else :
            return None
            
    def getBiggestMovingObject(self):
        if self.contours == None :
            return
        
        maxArea = 0
        biggestContour = None
        i=0
        pos = 0
        for contour in self.contours:
            area = cv2.contourArea(contour)
            if area > maxArea:
                maxArea = area
                biggestContour = contour
                pos = i
            i+=1

        if not biggestContour == None:
            x,y,w,h = cv2.boundingRect(biggestContour)
            return (x+w/2, y+h/2)
            
    def getMovingRectangles(self):
        return self.rectangles
    
    def drawRectangles(self):
        if self.rectangles == None:
            return self.frame
        for rect in self.rectangles:
            cv2.rectangle(self.frame, (rect[0],rect[1]), (rect[2],rect[3]), (0,255,0))
        if self.showTracker:
			cv2.imshow('tracker', self.frame)
        return self.frame
    
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
    
    def update2dPoints(self):
        if self.contours == None :
            return None
        
        self.estimator.getContours3dCoordinates(self.contours)
        
    def setParameter(self, parameter, value, value2=None):
        
        if parameter == 'blur':
            self.blurValue = value
        elif parameter == 'threshold':
            self.THRESHOLD = value
        elif parameter == 'threshold2':
            self.THRESHOLD2 = value
        elif parameter == 'm_open':
            self.KERNEL_OPEN = np.ones((value,value),np.uint8)
            #print self.KERNEL_OPEN
        elif parameter == 'm_close':
            self.KERNEL_CLOSE = np.ones((value2,value),np.uint8)
            #print self.KERNEL_CLOSE
        elif parameter == 'show_positions':
            self.showPositions = value
            self.estimator.showPositions = value
            self.estimator.initWindow()
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
        cv2.createTrackbar('threshold2','diff image',self.THRESHOLD2, 100, np.uint)

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

        value = cv2.getTrackbarPos('threshold2','diff image')
        if value != self.THRESHOLD2 :
            self.setParameter('threshold2', value)
            
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
    
    
            
