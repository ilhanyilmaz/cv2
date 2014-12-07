import cv2
import sys

if len(sys.argv) == 1:
    print "no input"
    sys.exit(-1)

capture = cv2.VideoCapture(sys.argv[1])

while capture.isOpened :
    f,frame = capture.read()
    cv2.imshow('frame', frame)
    if(cv2.waitKey(27)!=-1):
        capture.release()
        cv2.destroyAllWindows()
        break
