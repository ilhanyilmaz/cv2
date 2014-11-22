import cv2
import numpy as np

cam=cv2.VideoCapture(0)
fgbg = cv2.BackgroundSubtractorMOG()

while(cam.isOpened): 
   f,img=cam.read()
   if f==True:
       #img=cv2.flip(img,1)
       #img=cv2.medianBlur(img,3)
       fgmask = fgbg.apply(img)
       cv2.imshow('track',fgmask)
   if(cv2.waitKey(27)!=-1):
       cam.release()
       cv2.destroyAllWindows()
       break 
