import cv2
import sys
import videoPlayer as vp

def main(argv):
    hsvV = False
    
    if len(argv) == 0:
        print "no input"
        return -1
    if len(argv) >= 2 and argv[1] == '-hsv':
        hsvV = True
    capture = cv2.VideoCapture(argv[0])
    player = vp.VideoPlayer(capture, hsv=hsvV)
    
    while capture.isOpened :
        player.loop()

if __name__=="__main__":
    sys.exit(main(sys.argv[1:]))
