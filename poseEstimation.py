## code taken from: http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html#calibration

import numpy as np
import cv2
import glob
import sys

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

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

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    #height, width, depth = imgorg.shape
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #gray = cv2.imread(fname,cv2.IMREAD_GRAYSCALE)
    #cv2.imshow("gray", gray)
    #height, width = gray.shape
    ret = False
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,7), None)

    h,w =image.shape[:2]

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners)


        # Draw and display the corners
        cv2.drawChessboardCorners(image, (7,7), corners,ret)
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
        ret, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)
        imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
        dst= draw(image,corners2,imgpts)
        #dst = cv2.undistort(image, mtx, dist)
        # undistort
        #newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
        #mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
        #dst = cv2.remap(image,mapx,mapy,cv2.INTER_LINEAR)

        #print "ret: {0}\nmtx: {0}\ndist: {1}".format(ret,mtx,dist,rvecs,tvecs)
        #print "ret: {0}\nmtx: {1}\ndist: {2}\nrvecs:{3}\ntvecs:{4}".format(ret,mtx,dist,rvecs,tvecs)
        return dst
    return image
def main(argv):
    capture = cv2.VideoCapture(0)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((7*7,3), np.float32)
    #objp[:,:2] = np.mgrid[0:21.3:3.55,0:21.3:3.55].T.reshape(-1,2)
    objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)
    #print objp



    while capture.isOpened :
        f,image = capture.read()
        image = getCameraCalibration(image.copy(), objp)
        cv2.imshow("img",image)

        if(cv2.waitKey(27)!=-1):
            cv2.destroyAllWindows()
            capture.release()
            break

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
