import cv2
import sys
import numpy as np
import spherify as sp


if len(sys.argv) > 1 :
    filename = sys.argv[1]

image = cv2.imread(filename)
image = sp.spherify(image)
cv2.imshow('image', image)

while True:
    
    key = cv2.waitKey(27)
    
    #if key == 1048691: #S libopencv3.0.0
    if key == 115: #S libopencv3.0.0
        filename = "./sample/spherify.jpg"
        cv2.imwrite(filename, image)
        print "saved image to: {0}".format(filename)
    elif key != -1:
        print "pressed key: " + str(key)
        cv2.destroyAllWindows()
        break
    
