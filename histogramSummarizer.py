import numpy as np
import cv2
import glob
import sys

startX = 0
startY = 0
endX = 0
endY = 0
image = None
mouseDown = False

def summarizeHistogram(crop, image):
    cv2.imshow('crop', crop)
    height, width, depth = crop.shape
    print str(height) + ', ' + str(width)
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    hsvt = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #roiHist = cv2.calcHist([hsv], [0,1], None, [width, height], [0, width, 0, height])
    roiHist = cv2.calcHist([hsv], [0,1], None, [height, width], [0, height, 0, width])

    cv2.normalize(roiHist, roiHist,0,255,cv2.NORM_MINMAX)
    #dst = cv2.calcBackProject([hsvt],[0,1],roiHist,[0,width,0,height],1)
    dst = cv2.calcBackProject([hsvt],[0,1],roiHist,[0,height,0,width],1)

    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
    cv2.filter2D(dst, -1,disc,dst)

    ret,thresh = cv2.threshold(dst,50,255,cv2.THRESH_BINARY)
    thresh = cv2.merge((thresh,thresh,thresh))
    res = cv2.bitwise_and(image,thresh)

    res = np.hstack((image,thresh,res))
    cv2.imshow('backProj', res)

def fixPoints():
    global startX, endX, startY, endY
    if startX > endX:
        tempX = startX
        startX = endX
        endX = tempX
    if startY > endY:
        tempY = startY
        startY = endY
        endY = tempY

def mouseEvent(event,x,y,flags,param):
    global startX, startY, endX, endY, image, mouseDown
    imageCopy = image.copy()
    if event == cv2.EVENT_LBUTTONDOWN:
        #print 'Start Mouse Position: ' + str(x) + ', ' + str(y)
        startX = x
        startY = y
        mouseDown = True
    elif event == cv2.EVENT_LBUTTONUP:
        #print 'End Mouse Position: ' + str(x) + ', ' + str(y)
        endX = x
        endY = y
        fixPoints()
        cropImg = image[startY:endY, startX:endX]
        mouseDown = False
        summarizeHistogram(cropImg, image)
    elif event == cv2.EVENT_MOUSEMOVE and mouseDown:
        endX = x
        endY = y
        cv2.rectangle(imageCopy,(startX,startY),(endX,endY),(0,255,0),1)
        cv2.imshow('image',imageCopy)

def main(argv):
    global image
    if len(argv[0]) > 0:
        image = cv2.imread(argv[0])

    cv2.imshow("image", image)
    cv2.cv.SetMouseCallback('image', mouseEvent, 0)

    if(cv2.waitKey(0)!=-1):
        cv2.destroyAllWindows()
    return

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
