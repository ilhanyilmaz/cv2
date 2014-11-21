import numpy as np
import cv2
import cv2.cv as cv
import sys

cap = cv2.VideoCapture('../Videos/100ANV01/MAH00006.MP4')

height = cap.get(cv.CV_CAP_PROP_FRAME_WIDTH)
width = cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv.CV_CAP_PROP_FPS)
totalFrames = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))

#fourcc = cap.get(cv.CV_CAP_PROP_FOURCC)
fourcc = cv.CV_FOURCC('X','V','I','D')
print fps

videoWriter = cv2.VideoWriter("out.avi", int(fourcc), fps, (640,480))

for frameCount in range(totalFrames):
    #print ("{}/{}".format(frameCount, totalFrames), end='\r')
    perc= int(frameCount * 10.0 / totalFrames)
    sys.stdout.write("\r{0}> {1}/{2} completed...".format("="*perc, frameCount, totalFrames))
    ret, frame = cap.read()
    smallFrame = cv2.resize(frame, (640,480))    

    videoWriter.write(smallFrame)


    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
