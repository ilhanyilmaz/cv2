## code taken from: http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html#calibration

import numpy as np
import cv2
import glob
import sys

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

def getCameraCalibration(fname):
    global criteria

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((7*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

    #height, width, depth = imgorg.shape
    image = cv2.imread(fname)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #gray = cv2.imread(fname,cv2.IMREAD_GRAYSCALE)
    cv2.imshow("gray", gray)
    #height, width = gray.shape
    ret = False
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,7))

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners)


        # Draw and display the corners
        cv2.drawChessboardCorners(image, (7,7), corners,ret)
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

        dst = cv2.undistort(image, mtx, dist)
        cv2.imshow("img",dst)
        cv2.imwrite("{}_edit.jpg".format(fname),dst)
        print fname
        #print "ret: {0}\nmtx: {0}\ndist: {1}".format(ret,mtx,dist,rvecs,tvecs)
        print "ret: {0}\nmtx: {1}\ndist: {2}\nrvecs:{3}\ntvecs:{4}".format(ret,mtx,dist,rvecs,tvecs)

def main(argv):
    global images
    if len(sys.argv[1]) > 1:
        images = []
        images.append(sys.argv[1])
    else:
        foldername = "./captures/"
        images = glob.glob("{}*.jpg".format(foldername))

    for fname in images:
        print "Opening: {}".format(fname)
        getCameraCalibration(fname)

    if(cv2.waitKey(0)!=-1):
        cv2.destroyAllWindows()
        return

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
