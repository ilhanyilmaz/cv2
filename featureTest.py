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
frame = None

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
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    surf = cv2.SURF(400)
    kp, des = surf.detectAndCompute(gray,None)
    #frame = cv2.drawKeypoints(frame,kp,None,(255,0,0),4)
    return kp, des
   
def metSift(frame):
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5,5), 0)
    sift = cv2.SIFT()
    kp, des = sift.detectAndCompute(gray,None)
    #frame = cv2.drawKeypoints(frame,kp,None,(255,0,0),4)
    return kp, des


def metOrb(frame):
    orb = cv2.ORB()
    kp, des = orb.detectAndCompute(frame,None)
    #frame = cv2.drawKeypoints(frame,kp,None,(255,0,0),4)
    return kp, des
    
def filter_matches(matches, ratio = 0.75):
    filtered_matches = []
    for m in matches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            filtered_matches.append(m[0])
    
    return filtered_matches
    
def match_flann():
    # Parameters for nearest-neighbor matching
    FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing
    flann_params = dict(algorithm = FLANN_INDEX_KDTREE, 
        trees = 5)
    matcher = cv2.FlannBasedMatcher(flann_params, {})
    matches = matcher.knnMatch(des2, trainDescriptors=des1, k=2)
    #print "\t Match Count: ", len(matches)
    matches_subset = filter_matches(matches)
    print "\t Match Count: ", len(matches)
    # Sort them in the order of their distance.
    matches = sorted(matches_subset, key = lambda x:x.distance)

    
    h,w,d = frame1.shape
    h=h/3
    w=w/3
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
        #M = cv2.getAffineTransform(p1,p2)
        #pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        #dst = cv2.perspectiveTransform(pts,M)
        frame3 = cv2.warpPerspective(frame1, M, dsize=(w*3,h*3))
        #frame3 = cv2.warpAffine(frame1, M, dsize=(w*3,h*3))
        frame3[h:2*h,w:2*w,:] = frame2[h:2*h,w:2*w,:]
        
        #frame = cv2.absdiff(frame,frame2)
        #frame[0:h,0:w] = frame2
        #cv2.imshow('frame3', frame3)
        #frame2 = cv2.polylines(frame2,[np.int32(dst)],True,(0,255,0),3)
    
    #frame = np.hstack((frame1, frame2))
    
    #i=0
    #for match in matches:
    #    if i==20:
    #        break
        #pt1 = kp1[match.trainIdx].pt
        #pt1i = (int(pt1[0]),int(pt1[1]))
        #pt2 = kp2[match.queryIdx].pt
        #pt2i = (int(pt2[0]+w),int(pt2[1]))
        #cv2.line(frame, pt1i, pt2i, (255,0,0),1)
        #i+=1
        
    # Draw first 10 matches.
    #img3 = cv2.drawMatches(frame1,kp1,frame2,kp2,matches[:10], flags=2)
    
    
    return frame3

def match():
    global frame1, kp1, des1, frame2, kp2, des2, frame
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
        #pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        #dst = cv2.perspectiveTransform(pts,M)
        frame3 = cv2.warpPerspective(frame, M, dsize=(w*3,h*3))
        frame3[h:2*h,w:2*w,:] = frame2
        #frame = cv2.absdiff(frame,frame2)
        #frame[0:h,0:w] = frame2
        #cv2.imshow('frame3', frame3)
        #frame2 = cv2.polylines(frame2,[np.int32(dst)],True,(0,255,0),3)
    
    #frame = np.hstack((frame1, frame2))
    
    i=0
    for match in matches:
        if i==20:
            break
        pt1 = kp1[match.trainIdx].pt
        pt1i = (int(pt1[0]),int(pt1[1]))
        pt2 = kp2[match.queryIdx].pt
        pt2i = (int(pt2[0]+w),int(pt2[1]))
        #cv2.line(frame, pt1i, pt2i, (255,0,0),1)
        i+=1
        
    # Draw first 10 matches.
    #img3 = cv2.drawMatches(frame1,kp1,frame2,kp2,matches[:10], flags=2)
    
    
    return frame3

def main(argv):
    global frame1, kp1, des1, frame2, kp2, des2, frame
    #cap = cv2.VideoCapture("./sample/sample2.avi")
    if len(argv) > 0:
        cap = cv2.VideoCapture(argv[0])
    else:
        cap = cv2.VideoCapture(0)
        
    if cap.isOpened :
        f,frame = cap.read()
        #kp1, des1 = metOrb(frame1.copy())
        #kp1, des1 = metSurf(frame1.copy())
        h,w,d = frame.shape
        frame1 = np.zeros((h*3,w*3,d), np.uint8)
        frame1[h:2*h,w:2*w,:] = frame
        kp1, des1 = metSift(frame1)
        
        
        #cv2.imshow('frame', frame)
    
    while cap.isOpened :
        f,frame = cap.read()
        
        frame2 = np.zeros((h*3,w*3,d), np.uint8)
        frame2[h:2*h,w:2*w,:] = frame
        #frame = metGoodFeatures(frame.copy())
        #kp2, des2 = metOrb(frame2)
        #frame = metFast(frame.copy())
        #kp2, des2 = metSurf(frame2.copy())
        kp2, des2 = metSift(frame2)
        frame3 = match_flann()
        
        if frame3 != None:
            cv2.imshow('image', frame3)
            
        key = cv2.waitKey(30)
        if key == 32: #SPACE
        #if key == 1048608: #SPACE
            frame1 = frame3
            kp1, des1 = metSift(frame1)
        elif key != -1:
            print 'hallo'
            cap.release()
            cv2.destroyAllWindows()
            break
        

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
