import cv2
import numpy as np
import time

capture = cv2.VideoCapture(0)
numFramesToCapture = 10
capturedImageCount = 0
filenamePrefix = "./captures/capture_0"
filenameSuffix = ".jpg"
print "Get ready!"
timeInterval = 10
nextTime = time.time() + timeInterval
while(capture.isOpened and capturedImageCount < numFramesToCapture):
    if time.time() < nextTime:
        f,img = capture.read()
        continue
    nextTime = time.time() + timeInterval
    print "taking picture no: {}".format(capturedImageCount)

    f,img = capture.read()
    filename = "{0}{1}{2}".format(filenamePrefix, capturedImageCount, filenameSuffix)
    cv2.imwrite(filename, img)
    capturedImageCount += 1
    cv2.imshow("capture", img)
    if(cv2.waitKey(30)!=-1):
        capture.release()
        cv2.destroyAllWindows()
        break
