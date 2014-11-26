import cv2
import numpy as np

image = cv2.imread("backgroundImage.jpg")

hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
#cv2.imshow("hsv", hsv)

WHITEMIN = np.array([0,0,100], dtype=np.uint8)
WHITEMAX = np.array([255,40,255], dtype=np.uint8)
mask = cv2.inRange(hsv, WHITEMIN, WHITEMAX)
cv2.imshow("mask", mask)

ret, threshold = cv2.threshold(mask, 100, 255, cv2.THRESH_BINARY)

kernel = np.ones((10,10),np.uint8)
threshold = cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
cv2.imshow("threshold", threshold)

edges = cv2.Canny(threshold,50,150,apertureSize = 3)
cv2.imshow("edges", edges)

lines = cv2.HoughLines(edges,1,np.pi/180,92)
if not lines == None :
    for rho,theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)

        cv2.imshow("image",image)

cv2.waitKey()
cv2.destroyAllWindows()
