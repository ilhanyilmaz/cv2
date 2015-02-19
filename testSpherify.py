import cv2
import sys
import numpy as np
import spherify as sp

showHSV = False
capture = cv2.VideoCapture(0)
saveDirectory = './sample/captures/showWebcam_'
captureNo = 0

if len(sys.argv) > 1 and sys.argv[1] == '-hsv':
    showHSV = True

while capture.isOpened :
    #print capture.get(cv2.cv.CV_CAP_PROP_FPS)
    capture.grab()
    f,frame = capture.retrieve()
    
    frame = sp.spherify(frame)
    cv2.imshow('frame', frame)
    key = cv2.waitKey(27)
    
    #if key == 1048691: #S libopencv3.0.0
    if key == 115: #S libopencv3.0.0
        filename = "{0}capture_{1}.jpg".format(saveDirectory, captureNo)
        cv2.imwrite(filename, frame)
        print "saved frame to: {0}".format(filename)
        captureNo+=1
    elif key != -1:
        print "pressed key: " + str(key)
        capture.release()
        cv2.destroyAllWindows()
        break
    
