## code taken from: http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html#calibration

import numpy as np
import cv2
import glob
import sys

KEYSPACE = 32
KEYLEFT = 65361
KEYRIGHT = 65363
KEYESC = 27 

mtx = np.float32([[ 631.22109349,0.,298.14876851],[0.,666.24596045,244.10381178],[0.,0.,1.]])

dist= np.float32([[ 0.12338113, -1.04133076, -0.02325425, -0.01084442,  3.48500498]])

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
playing = True

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
    global criteria, mtx, dist

    axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
    #height, width, depth = imgorg.shape
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ret = False
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,7), None)

    h,w =image.shape[:2]

    # If found, add object points, image points (after refining them)
    if ret == True:
        #objpoints.append(objp)

        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        #imgpoints.append(corners)

        rvecs,tvecs,inliers = cv2.solvePnPRansac(objp, corners, mtx, dist)

        imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
        img = draw(image, corners, imgpts)
        
        return img

    return image
def main(argv):
    global playing

    if len(argv) > 0:
        capture = cv2.VideoCapture(argv[0])
    else:
        capture = cv2.VideoCapture(0)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((7*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:21.3:3.55,0:21.3:3.55].T.reshape(-1,2)
    #objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)
    #print objp



    while capture.isOpened :
        currentFrame =  capture.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
        f,image = capture.read()
        image = getCameraCalibration(image.copy(), objp)
        cv2.imshow("img",image)

        if playing:
            key = cv2.waitKey(25) 
            if(key == KEYSPACE):
                playing = False
            elif(key == 27):
                cv2.destroyAllWindows()
                capture.release()
                break
        else:
            key = cv2.waitKey(0) 
            if(key == 27):
                print key
                cv2.destroyAllWindows()
                capture.release()
                break
            elif(key == KEYLEFT):
                playing = False
                capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, currentFrame - 1.0)
            elif(key == KEYRIGHT):
                playing = False
                capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, currentFrame + 1.0)
            elif key == KEYSPACE :
                playing = True
            else :
                print key

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
