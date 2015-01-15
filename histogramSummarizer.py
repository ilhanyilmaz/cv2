import numpy as np
import cv2
import glob
import sys

startX = 0
startY = 0
endX = 0
endY = 0
image = None
crop = None
mouseDown = False
discValue = 10
threshold = 30

def createTrackbars():
    global discValue, threshold
    cv2.namedWindow('image')
    cv2.createTrackbar('disc','image',discValue, 30, np.uint)
    cv2.createTrackbar('threshold','image',threshold, 50, np.uint)

def checkSettings():
    global discValue, threshold, crop, image
    change = False
    val = cv2.getTrackbarPos('disc','image')
    if val == 0:
        val = 1
    if discValue != val:
        discValue = val
        change = True
        
    val = cv2.getTrackbarPos('threshold', 'image')
    if val == 0:
        val = 1
    if threshold != val:
        threshold = val
        change = True    
    if change :
        summarizeHistogram(crop, image)
            
def summarizeHistogram(crop, image):
    global discValue, threshold
    #cv2.imshow('crop', crop)
    height, width, depth = crop.shape
    #print str(height) + ', ' + str(width)
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    hsvt = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array((0., 15.,15.)), np.array((180.,256.,256.)))
    #roiHist = cv2.calcHist([hsv], [0], None, [180], [0, 180])
    roiHist = cv2.calcHist([hsv], [0,1], mask, [180, 256], [0, 180, 0, 256])
    #roiHist = cv2.calcHist([hsv], [0,1], None, [180, 256], [0, 180, 0, 256])

    cv2.normalize(roiHist, roiHist,0,255,cv2.NORM_MINMAX)
    #dst = cv2.calcBackProject([hsvt],[0],roiHist,[0,180],1)
    dst = cv2.calcBackProject([hsvt],[0,1],roiHist,[0,180,0,256],1)
    cv2.imshow('dst', dst)
    disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(discValue,discValue))
    cv2.filter2D(dst, -1,disc,dst)
    ret,thresh = cv2.threshold(dst,threshold,255,cv2.THRESH_BINARY)
    thresh = cv2.merge((thresh,thresh,thresh))
    res = cv2.bitwise_and(image,thresh)

    res = np.hstack((thresh,res))
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
    global startX, startY, endX, endY, image, mouseDown, crop
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
        crop = image[startY:endY, startX:endX]
        mouseDown = False
        summarizeHistogram(crop, image)
    elif event == cv2.EVENT_MOUSEMOVE and mouseDown:
        endX = x
        endY = y
        cv2.rectangle(imageCopy,(startX,startY),(endX,endY),(0,255,0),1)
        cv2.imshow('image',imageCopy)

def main(argv):
    global image
    captureNo = 0;
    if len(argv[0]) > 0:
        filename = argv[0]
        image = cv2.imread(filename)
    createTrackbars()
    cv2.imshow("image", image)
    cv2.setMouseCallback('image', mouseEvent)

    while(True):
        checkSettings()
        key = cv2.waitKey(90)
        
        if key == 1048691:
            captureName = filename + '_' + str(captureNo) + '.jpg'
            cv2.imwrite(captureName,image[startY:endY, startX:endX])
            print 'cropped frame saved to: ' + captureName
            captureNo = captureNo + 1   
        elif key != -1:
            print key
            break
    
    cv2.destroyAllWindows()
    return

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
