import cv2
import numpy as np
import math

imageSize = 360
maxSize = 1280

def getAngleDist(i,j):
    global imageSize
    halfSize = imageSize / 2
    x = i - halfSize
    y = j - halfSize
    angle = math.atan2(y,x)
    if angle > 0:
        angle = angle * 180 / math.pi
    else :
        angle = 360 + angle * 180 / math.pi
    
    if angle == 360:
        angle = 0
    
    dist = math.hypot(x,y)
    return angle, dist

def getUniformCoordinates(angle, dist):
    global imageSize
    v = dist / (imageSize/2)
    u = angle / 360.0
    #circleLengthAtDist = 2 * math.pi * dist
    #v = angle * circleLengthAtDist / 360.0
    #u = angle / 360.0
    #print str(u) + " - " + str(v)
    return u, v

def rotateImage(image, angle):
    cols, rows, depth = image.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    dst = cv2.warpAffine(image,M,(cols,rows))
    return dst
    
def spherify(image):
    global imageSize, maxSize
    
    #image = rotateImage(image, 270)
    height, width, depth = image.shape
    if height / 2 > imageSize:
        imageSize = height / 2
    if imageSize > maxSize:
        imageSize = maxSize
    #scaleFactorX = width / imageSize
    #scaleFactorY =  height / imageSize
    #print str(width) + " - " + str(height)
    halfSize = imageSize / 2
    size = (imageSize,imageSize,3)
    newImg = np.zeros(size, np.uint8)
    for j in range(imageSize):
        for i in range(imageSize):
            angle, dist = getAngleDist(i,j)
            u, v = getUniformCoordinates(angle,dist)
            if u < 1 and v < 1:
                x = u * width
                y = height - v * height - 1
                newImg[j,i,:] = image[y,x,:]
    
    #newImg = rotateImage(newImg, 270)
    return newImg
