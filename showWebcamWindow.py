import cv2
import sys
import numpy as np

showHSV = False
capture = cv2.VideoCapture(0)
saveDirectory = './sample/captures/showWebcam_'
captureNo = 0

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
    key = cv2.waitKey(27)
    
    if key == 1048691: #S libopencv3.0.0
        filename = "{0}capture_{1}.jpg".format(saveDirectory, captureNo)
        cv2.imwrite(filename, frame)
        print "saved frame to: {0}".format(filename)
        captureNo+=1
    elif key != -1:
        print "pressed key: " + str(key)
        capture.release()
        cv2.destroyAllWindows()
        break
    
