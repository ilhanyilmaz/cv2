########################################
# written by ilhanyilmaz
# records the webcam capture as video
# according to provided arguments
# input:
#   -o :  output video
#   -w :  target width
#   -h :  target height
#   -t :  record length
########################################


import numpy as np
import cv2
import cv2.cv as cv
import sys, getopt
import time

outputfile = ''
targetWidth = int(0)
targetHeight = int(0)
recordTime = int(0)
fps = 0
cap = None
sleepTime = 0

def recordVideo():
    global outputfile
    global targetWidth
    global targetHeight
    global recordTime
    global cap
    global fps
    global sleepTime

    #fourcc = cap.get(cv.CV_CAP_PROP_FOURCC)
    fourcc = cv.CV_FOURCC('X','V','I','D')

    videoWriter = cv2.VideoWriter(outputfile, int(fourcc), fps, (targetHeight,targetWidth))

    for frameCount in range(recordTime):
        #print ("{}/{}".format(frameCount, totalFrames), end='\r')
        sys.stdout.write("\r {0}/{1} recorded...".format(frameCount/fps, recordTime / fps))
        ret, frame = cap.read()
        smallFrame = cv2.resize(frame, (targetHeight,targetWidth))    

        videoWriter.write(smallFrame)

        time.sleep(sleepTime)
        #k = cv2.waitKey(40) & 0xff
        #if k == 27:
        #    break

    cap.release()
    videoWriter.release()
    cv2.destroyAllWindows()
    print "\nRecording completed. File saved at {}.".format(outputfile)

def main(argv):
    global outputfile
    global targetWidth
    global targetHeight
    global recordTime
    global cap
    global fps
    global sleepTime

    try:
        opts, args = getopt.getopt(argv, "o:w:h:t:f:", ["ofile=","width=", "height=", "length=", "recordfps="])
    except getopt.GetoptError:
        print 'resizeVideo.py -o <outputfile> -w <width> -h <height> -t <recordlength>'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-h", "--height"):
            targetHeight = int(arg)
        elif opt in ("-w", "--width"):
            targetWidth = int(arg)
        elif opt in ("-t", "--recordTime"):
            recordTime = int(arg)
        elif opt in ("-f", "--fps"):
            fps = int(arg)
        #elif opt in ("-h", "--help"):
        #    print 'resizeVideo.py -o <outputfile> -w <width> -h <height> -t <recordlength>'
        #    sys.exit(2)
            

    if outputfile == '':
        #print 'resizeVideo.py -o <outputfile> -w <width> -h <height> -t <recordlength>'
        outputfile = "record{}.avi".format(time.clock())
        print outputfile


    cap = cv2.VideoCapture(0)
    orgHeight = int(cap.get(cv.CV_CAP_PROP_FRAME_WIDTH))
    orgWidth = int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
    #fps = cap.get(cv.CV_CAP_PROP_FPS)

    if fps == 0:
        fps = 25

    sleepTime = 1.0/fps
    if recordTime == 0:
        recordTime = 60 * fps  # set end frame if not provided
    else :
        recordTime = int(recordTime * fps) # turn seconds into frames


    if targetWidth == 0:
        targetWidth = orgWidth

    if targetHeight == 0:
        targetHeight = orgHeight

    print "Output file is {}".format(outputfile)
    print "Target size is: {}-{}".format(targetWidth,targetHeight)
    print "Record length : {}".format(recordTime / fps)

    recordVideo()    

if __name__ == "__main__":
    main(sys.argv[1:])
