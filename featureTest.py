import cv2
import numpy as np
import sys


def metGoodFeatures(frame):
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
    corners = np.int0(corners)

    for i in corners:
        x,y = i.ravel()
        cv2.circle(frame,(x,y),3,255,-1)
    return frame
    
def metFast(frame):
    fast = cv2.FastFeatureDetector()
    kp = fast.detect(frame,None)
    frame = cv2.drawKeypoints(frame,kp,None,(255,0,0))
    return frame
    
def metSurf(frame):
    surf = cv2.SURF(400)
    kp, des = surf.detectAndCompute(frame,None)
    frame = cv2.drawKeypoints(frame,kp,None,(255,0,0),4)
    return frame
   
def metSift(frame):
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT()
    kp, des = sift.detectAndCompute(gray,None)
    frame = cv2.drawKeypoints(frame,kp,None,(255,0,0),4)
    return frame
    
def main(argv):
    cap = cv2.VideoCapture(0)

    while cap.isOpened :
        f,frame = cap.read()
        
        frame = metGoodFeatures(frame.copy())
        #frame = metFast(frame.copy())
        #frame = metSurf(frame.copy())
        #frame = metSift(frame.copy())
        
        cv2.imshow('image', frame)
        if cv2.waitKey(30) != -1:
            cap.release()
            cv2.destroyAllWindows()
            break    

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
