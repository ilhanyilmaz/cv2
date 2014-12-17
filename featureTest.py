import cv2
import numpy as np
import sys
import time

frame1 = None
kp1 = None
des1 = None
frame2 = None
kp2 = None
des2 = None

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


def metOrb(frame):
    orb = cv2.ORB()
    kp, des = orb.detectAndCompute(frame,None)
    #frame = cv2.drawKeypoints(frame,kp,None,(255,0,0),4)
    return kp, des
    
def match():
    global frame1, kp1, des1, frame2, kp2, des2
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des2,des1)

    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)

    
    h,w,d = frame1.shape
    i=0
    p1=[[0,0]]
    p2=[[0,0]]
    for match in matches:
        if i==20:
            break
        #print '{0}, {1}'.format(match.trainIdx, match.queryIdx)
        #print match.distance
        p1 = np.append(p1,[kp1[match.trainIdx].pt], axis=0)
        p2 = np.append(p2,[kp2[match.queryIdx].pt], axis=0)
        i+=1
        
    p1 = p1[1:]
    p2 = p2[1:]
    
    if len(p1)>4:
        M,mask = cv2.findHomography(p1,p2)
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)
        #frame2 = cv2.polylines(frame2,[np.int32(dst)],True,(0,255,0),3)
    
    frame = np.hstack((frame1, frame2))
    
    i=0
    for match in matches:
        if i==20:
            break
        pt1 = kp1[match.trainIdx].pt
        pt1i = (int(pt1[0]),int(pt1[1]))
        pt2 = kp2[match.queryIdx].pt
        pt2i = (int(pt2[0]+w),int(pt2[1]))
        cv2.line(frame, pt1i, pt2i, (255,0,0),1)
        i+=1
        
    # Draw first 10 matches.
    #img3 = cv2.drawMatches(frame1,kp1,frame2,kp2,matches[:10], flags=2)
    
    
    return frame

def main(argv):
    global frame1, kp1, des1, frame2, kp2, des2
    #cap = cv2.VideoCapture("./sample/sample2.avi")
    cap = cv2.VideoCapture(0)
    
    
    if cap.isOpened :
        f,frame1 = cap.read()
        kp1, des1 = metOrb(frame1.copy())
    
    while cap.isOpened :
        f,frame2 = cap.read()
        
        #frame = metGoodFeatures(frame.copy())
        kp2, des2 = metOrb(frame2)
        #frame = metFast(frame.copy())
        #frame = metSurf(frame.copy())
        #frame = metSift(frame.copy())
        frame = match()
        
        if frame != None:
            cv2.imshow('image', frame)
            
        key = cv2.waitKey(30)
        if key == 32: #SPACE
        #if key == 1048608: #SPACE
            frame1=frame2.copy()
            kp1, des1 = metOrb(frame1.copy())
        elif key != -1:
            cap.release()
            cv2.destroyAllWindows()
            break
        

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
