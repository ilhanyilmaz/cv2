import cv2
import numpy as np
import sys

FRAMEDIST = 5
THRESHOLD = 20
PERFECTION = 10

capture = None
inputFile = None


if len(sys.argv) > 1 :
    inputFile = sys.argv[1]
    print "Opening file: {}".format(inputFile)
    capture=cv2.VideoCapture(inputFile)
else :
    print "Opening camera."
    capture=cv2.VideoCapture(0)

backImage = None
checkMat = None
anyChange = True
img = None
count = 0
while(capture.isOpened and anyChange and count < 50): 
    count+=1
    f = False
    for i in range(FRAMEDIST):
        f,img=capture.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if f==True:
        if backImage == None:
            backImage = imgGray
            continue
        diffImage = cv2.absdiff(backImage,imgGray)
        ret, threshold = cv2.threshold(diffImage, THRESHOLD, 1, cv2.THRESH_BINARY_INV)
        
        if checkMat == None:
            checkMat = threshold.copy()
            continue

        #bitwiseMat = cv2.bitwise_and(checkMat, threshold)

        #cv2.accumulate(threshold, checkMat)
        anyChange = False
        for j in range(640):
            for i in range(480):
                if checkMat[i][j] < PERFECTION: 
                    if threshold[i][j]==1:
                        checkMat[i][j] += 1
                        backImage[i][j] = (backImage[i][j]*(checkMat[i][j]-1) + imgGray[i][j]) / checkMat[i][j]
                    else:
                        checkMat[i][j] = 0
                        backImage[i][j] = imgGray[i][j]
                        anyChange = True                

        #checkMat = checkMat * bitwiseMat + checkMat
        #r, threshCheckMat = cv2.threshold(checkMat, 1,255,cv2.THRESH_BINARY)

        #backImage = cv2.bitwise_and(backImage,backImage,mask=threshCheckMat)
        cv2.imshow('track', backImage)
        if anyChange == False:
            break

    if(cv2.waitKey(27)!=-1):
        capture.release()
        cv2.destroyAllWindows()
        break 

capture.release()
cv2.destroyAllWindows()
cv2.imwrite("backgroundImageGray.jpg", backImage)
