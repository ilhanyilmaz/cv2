## code taken from: http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html#calibration

import numpy as np
import cv2
import glob
import sys
import videoPlayer as vp

KEY_S = 115 # Save calibration
KEY_D = 100 # CHANGE DISPLAY matrix-tvecs-rvecs

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

lastMtx = None
lastDist = None
lastTVecs = None
lastRVecs = None
SAVEDIRECTORY = './sample/calibration/'

def saveCalibration():
    global lastMtx, lastDist, lastTVecs, lastRVecs
    if not lastMtx==None and not lastDist==None and not lastTVecs==None and not lastRVecs==None :
        file = SAVEDIRECTORY + 'calibration'
        np.savez(file, mtx=lastMtx, dist=lastDist, tvecs=lastTVecs, rvecs=lastRVecs)

def draw(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1,2)

    # draw ground floor in green
    img = cv2.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)

    # draw pillars in blue color
    for i,j in zip(range(4),range(4,8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)

    # draw top layer in red color
    img = cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)

    return img

def getCameraCalibration(image, objp):
    global criteria
    global lastMtx, lastDist, lastTVecs, lastRVecs

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    #height, width, depth = imgorg.shape
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ret = False
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,7), None)

    h,w =image.shape[:2]

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners)


        # Draw and display the corners
        cv2.drawChessboardCorners(image, (7,7), corners,ret)

        #calibration
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

        
        #undistort
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
        dst = cv2.undistort(image, mtx, dist, None, newcameramtx)
        
        #print "mtx: {0}\ndist: {1}".format(mtx,dist)

        lastMtx = newcameramtx
        lastDist = dist
        lastRVecs = rvecs
        lastTVecs = tvecs
        return dst

        #ret, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)
        #imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
        #dst= draw(image,corners2,imgpts)
        # undistort
        #mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
        #dst = cv2.remap(image,mapx,mapy,cv2.INTER_LINEAR)

        #return dst
    return image
def main(argv):
    global lastMtx, lastDist, lastTVecs, lastRVecs

    player = None
    if len(argv) > 0:
        capture = cv2.VideoCapture(argv[0])
        player = vp.VideoPlayer(capture)

    else:
        capture = cv2.VideoCapture(0)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((7*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:21.3:3.55,0:21.3:3.55].T.reshape(-1,2)
    #objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

    image = None
    displayInfo = 0
    while capture.isOpened :
        if not player == None:
            currentFrame =  capture.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
            f,image = capture.retrieve()
            key = player.loop()
        else :
            f,image = capture.read()

        image = getCameraCalibration(image.copy(), objp)
        cv2.imshow("img",image)

        if player == None:
            key = cv2.waitKey(50)
        
        if(key == 27):
            capture.release()
            cv2.destroyAllWindows()
            break
        elif key == KEY_S:
            saveCalibration()
        elif key == KEY_D:
            displayInfo+=1
        elif not key == -1 :
            print key

        if displayInfo % 4 == 0 :
            print "mtx: {0}".format(lastMtx)
        elif displayInfo % 4 == 1 :
            print "tvecs: {0}".format(lastTVecs)
        elif displayInfo % 4 == 2 :
            print "rvecs: {0}".format(lastRVecs)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
