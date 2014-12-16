import cv2
import numpy as np

class CamShiftTracker():
    def __init__(self):
		
        self.term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
        #updateContours(contours)
        
    def updateContours(self, frame, contours):

        self.movingObjects = []
        self.histograms = []
        
        height, width = frame.shape[:2]
        
        i=0
        for contour in contours:
            c,r,w,h = cv2.boundingRect(contour)
            if w*h < 20:
				continue
			# set up the ROI for tracking
            roi = frame[r:r+h, c:c+w]
            hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            
            mask2 = cv2.inRange(hsv_roi, np.array((0., 30.,30.)), np.array((180.,250.,250.)))
            mask = np.zeros((height,width), np.uint8)
            cv2.drawContours(mask, [contour], 0, 255, -1)
            maskArea = mask[r:r+h,c:c+w]
            maskArea = cv2.bitwise_and(maskArea, mask2)
            img = cv2.bitwise_and(roi,roi,mask=maskArea)
            #cv2.imshow('maskarea', mask2)
            roi_hist = cv2.calcHist([hsv_roi],[0,1],maskArea,[180,256],[0,180,0,256])
            #roi_hist = cv2.calcHist([hsv_roi],[0],maskArea,[180],[0,180])
            cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
            #print i
            i+=1
            self.movingObjects.append((c,r,w,h))
            self.histograms.append(roi_hist)
            
            
    def track(self, frame):
        
        for i in range(len(self.movingObjects)):
			
            track_window = self.movingObjects[i]
			#track_window = (c,r,w,h)
            c = track_window[0]
            r = track_window[1]
            w = track_window[2]
            h = track_window[3]
            
            if w == 0 or h == 0:
                continue
            
            #mask = cv2.inRange(hsv_roi, np.array((0., 0.,0.)), np.array((180.,255.,255.)))
            roi_hist = self.histograms[i]
            
            
        
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            #dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,256],1)
            dst = cv2.calcBackProject([hsv],[0,1],roi_hist,[0,180,0,256],1)

            #ret, self.movingObjects[i] = cv2.meanShift(dst, track_window, self.term_crit)
            # apply meanshift to get the new location
            ret, self.movingObjects[i] = cv2.CamShift(dst, track_window, self.term_crit)
            
            
            # Draw it on image
            #pts = cv2.boxPoints(ret)
            #pts = np.int0(pts)
            #self.movingObjects.append(pts)
            #img2 = cv2.polylines(frame,[pts],True, 255,2)
        
        self.drawContours(frame)
        #return self.movingObjects
        
    def drawContours(self, frame):
        
        for window in self.movingObjects:
            
            x = window[0]
            y = window[1]
            w = window[2]
            h = window[3]
            #print area
            if w*h < 20:
                continue

            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0))
            #cv2.drawContours(img,contours,-1,(0,255,0),3)
        
	    cv2.imshow('camshift', frame)
        
