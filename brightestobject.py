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
        maskArea = mask[y-5:y+h+5,x-5:x+w+5]
        
        if area < minSize:
            i+=1
            continue

        if squareness(w,h) < 0.8:
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
        
