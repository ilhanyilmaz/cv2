import cv2
import sys
import numpy as np

showHSV = False
capture = cv2.VideoCapture(0)
if len(sys.argv) > 1 and sys.argv[1] == '-hsv':
    showHSV = True
    
while capture.isOpened :
    #print capture.get(cv2.cv.CV_CAP_PROP_)
    f,frame = capture.read()
    if showHSV:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h,s,v = cv2.split(hsv)
        hs = np.hstack((h,s))
        vg = np.hstack((v,gray))
        hsvg = np.vstack((hs,vg))
        cv2.imshow('frame', hsvg)
    else :
        cv2.imshow('frame', frame)
        
    if(cv2.waitKey(27)!=-1):
        capture.release()
        cv2.destroyAllWindows()
        break
