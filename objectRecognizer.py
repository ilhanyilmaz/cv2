import cv2
import numpy as np

hValue=47
sValue=82
vValue=109
reqRatio=60

hThreshold=23
sThreshold=98
vThreshold=135


def createJerseyWindow():
    global hValue, vValue, sValue, reqRatio, hThreshold, sThreshold, vThreshold
    cv2.namedWindow('jersey')
    cv2.createTrackbar('h','jersey', hValue, 255, np.uint)
    cv2.createTrackbar('s','jersey', sValue, 255, np.uint)
    cv2.createTrackbar('v','jersey', vValue, 255, np.uint)
    cv2.createTrackbar('ratio','jersey', reqRatio, 100, np.uint)
    cv2.createTrackbar('hThreshold','jersey', hThreshold, 255, np.uint)
    cv2.createTrackbar('sThreshold','jersey', sThreshold, 255, np.uint)
    cv2.createTrackbar('vThreshold','jersey', vThreshold, 255, np.uint)

def updateParameters():
	global hValue, vValue, sValue, reqRatio, hThreshold, sThreshold, vThreshold
	value = cv2.getTrackbarPos('h','jersey')
	hValue = value
	value = cv2.getTrackbarPos('s','jersey')
	sValue = value
	value = cv2.getTrackbarPos('v','jersey')
	vValue = value
	value = cv2.getTrackbarPos('ratio','jersey')
	reqRatio = value
	value = cv2.getTrackbarPos('hThreshold','jersey')
	hThreshold = value
	value = cv2.getTrackbarPos('sThreshold','jersey')
	sThreshold = value
	value = cv2.getTrackbarPos('vThreshold','jersey')
	vThreshold = value
	
def colorRatio(frame, mask, contour):
    
    cv2.drawContours(mask, [contour], 0, 255, -1)
    r = cv2.mean(frame, mask)
    return r
    
def nonZeroRatio(mask, size):
	return cv2.countNonZero(mask) / float(size)
	
def playersWithGreenJersey(frame, contours):
    
    global hValue, vValue, sValue, reqRatio, hThreshold, sThreshold, vThreshold
    
    updateParameters()
    players = []
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hue,sat,val = cv2.split(hsv)
    
    height, width = frame.shape[:2]
    
    hueDiff = cv2.absdiff(hue, hValue)
    satDiff = cv2.absdiff(sat, sValue)
    valDiff = cv2.absdiff(val, vValue)
    ret, hMask = cv2.threshold(hueDiff, hThreshold, 255, cv2.THRESH_BINARY_INV)
    ret, sMask = cv2.threshold(satDiff, sThreshold, 255, cv2.THRESH_BINARY_INV)
    ret, vMask = cv2.threshold(valDiff, vThreshold, 255, cv2.THRESH_BINARY_INV)
    
    jerseyMask = cv2.bitwise_and(hMask, sMask)
    jerseyMask = cv2.bitwise_and(jerseyMask, vMask)
    cv2.imshow("colormask",jerseyMask)
    #cv2.imshow("sat",sat)
    #cv2.imshow("val",val)
    
    
    for contour in contours:
		
        area = cv2.contourArea(contour)
        if area < 20:
			continue
        x,y,w,h = cv2.boundingRect(contour)
        #frameArea = h[y:y+h,x:x+w]
        mask = np.zeros((height,width), np.uint8)
        cv2.drawContours(mask, [contour], 0, 255, -1)
        #maskArea = mask[y:y+h,x:x+w]
        
        objMask = cv2.bitwise_and(jerseyMask,mask)
        if nonZeroRatio(objMask, area) > reqRatio / 100.0:
			players.append(contour)
			cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0))
        
    
    cv2.imshow("jersey",frame)     
    
    #contours = getContours(diffImage)
    #index = findBall(frame, contours)
    #if index == -1:
    #    return None
    #return contours[index]
	
