import numpy as np
import cv2

cap = cv2.VideoCapture('../Videos/100ANV01/MAH00006.MP4')

fgbg = cv2.BackgroundSubtractorMOG2()

while(1):
    ret, frame = cap.read()
    smallFrame = cv2.resize(frame, (640,480))

    fgmask = fgbg.apply(smallFrame)
    kernel = np.ones((3,3),np.uint8)
    erosion = cv2.erode(fgmask,kernel,iterations = 1)

    #fgmask = cv2.morphologyEX(fgmask, cv2.MORPH_OPEN, kernel)
    
    cv2.imshow('frame',erosion)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
