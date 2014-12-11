import cv2
import numpy as np


def getBrightness(frame, mask, contour):
    
    cv2.drawContours(mask, [contour], 0, 255, -1)
    r = cv2.mean(frame, mask)
    return r

def squareness(w,h):
    if w>h:
        return h/float(w)
    else:
        return w/float(h)

def circle(frame, mask, contour):
    cv2.drawContours(mask, [contour], 0, 255, -1)
    edges = cv2.Canny(mask,100,200)
    #circles = cv2.HoughCircles(mask,cv2.cv.CV_HOUGH_GRADIENT,1,10,param1=100,param2=100,minRadius=5,maxRadius=20)
    # detect circles in the image
    circles = cv2.HoughCircles(mask, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100, 100, 50)
    if circles is not None:
        circles = np.round(circles[0,:]).astype('int')

        for (x,y,r) in circles:
            cv2.circle(frame, (x,y), r, 255, -1)
            print 'alo'

    cv2.imshow('circles', edges)

def nonZeroRatio(mask):
	return cv2.countNonZero(mask) / float(mask.size)

def findBall(frame, contours, minSize=64):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hue,sat,val = cv2.split(hsv)
    if len(contours) == 0:
        return -1
    
    points = np.zeros(len(contours), np.uint8)
    height, width = g.shape
    i=0
    for contour in contours:
        area = cv2.contourArea(contour)
        x,y,w,h = cv2.boundingRect(contour)
        frameArea = g[y:y+h,x:x+w]
        mask = np.zeros((height,width), np.uint8)
        cv2.drawContours(mask, [contour], 0, 255, -1)
        maskArea = mask[y:y+h,x:x+w]
        
        if area < minSize:
            i+=1
            continue

        if squareness(w,h) < 0.8:
            i+=1
            continue
            
        print nonZeroRatio(maskArea)
        if nonZeroRatio(maskArea) < 0.65:
			i+=1
			continue
        
        #satur = getBrightness(sat, mask, contour)
        #if satur[0] > 40:
        #    i+=1
        #    continue
        
        mask = np.zeros((height,width), np.uint8)
        value = getBrightness(g, mask, contour)
        points[i] = value[0]
        
        if value > 100:
            circle(frameArea, maskArea, contour)
        i+=1

        
        
    index= np.argmax(points)
    if points[index] > 100:
        print points[index]
        return np.argmax(points)
    else:
        return -1
        
def getContours(diffImage):
    
    #threshold = cv2.erode(threshold,kernel,iterations = 1)
    #threshold = cv2.dilate(threshold,kernel,iterations = 1)
    kernel = np.ones((2,2),np.uint8)
    threshold = cv2.morphologyEx(diffImage, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((2,2),np.uint8)
    threshold = cv2.morphologyEx(diffImage, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('threshold', threshold)
    contours, hierachy = cv2.findContours(threshold, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    return contours
        
def getBall(frame, diffImage):
    
    contours = getContours(diffImage)
    index = findBall(frame, contours)
    if index == -1:
        return None
    return contours[index]
	
