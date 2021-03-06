########################################
# written by ilhanyilmaz
# crops and resizes the given video
# according to provided arguments
# input:
#   -i :  input video
#   -o :  output video
#   -w :  target width
#   -h :  target height
#   -s :  crop starts from given input
#   -e :  crop ends from given input
########################################


import numpy as np
import cv2
#import cv2.cv as cv
import sys, getopt

inputfile = ''
outputfile = ''
targetWidth = int(0)
targetHeight = int(0)
startAt = int(0)
endAt = int(0)
totalFrames = int(0)
fps = 0.0
cap = None
changeSize = False

def editVideo():
    global inputfile
    global outputfile
    global targetWidth
    global targetHeight
    global startAt
    global endAt
    global cap
    global fps
    global changeSize

    #cap.set(cv.CV_CAP_PROP_POS_FRAMES, startAt)
    cap.set(cv2.CAP_PROP_POS_FRAMES, startAt)
    frameInRange = endAt - startAt
    #fourcc = cap.get(cv.CV_CAP_PROP_FOURCC)
    #fourcc = cv.CV_FOURCC('X','V','I','D')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    videoWriter = cv2.VideoWriter(outputfile, int(fourcc), fps, (targetWidth,targetHeight))

    for frameCount in range(frameInRange):
        #print ("{}/{}".format(frameCount, totalFrames), end='\r')
        perc= int(frameCount * 10.0 / frameInRange)
        sys.stdout.write("\r{0}> {1}/{2} completed...".format("="*perc, frameCount, frameInRange))
        ret, frame = cap.read()
        smallFrame = cv2.resize(frame, (targetWidth,targetHeight))    

        videoWriter.write(smallFrame)


        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    videoWriter.release()
    cv2.destroyAllWindows()
    print "\nEditing completed. File saved at {}.".format(outputfile)

def main(argv):
    global inputfile
    global outputfile
    global targetWidth
    global targetHeight
    global startAt
    global endAt
    global totalFrames
    global cap
    global fps
    global changeSize

    try:
        opts, args = getopt.getopt(argv, "i:o:w:h:s:e:", ["ifile=","ofile=","width=", "height=", "start=", "end="])
    except getopt.GetoptError:
        print 'resizeVideo.py -i <inputfile> -o <outputfile> -w <width> -h <height> -s <startsec> -e <endsec>'
        sys.exit(2)
    if len(opts) == 0:
        print 'resizeVideo.py -i <inputfile> -o <outputfile> -w <width> -h <height> -s <startsec> -e <endsec>'
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-h", "--height"):
            targetHeight = int(arg)
        elif opt in ("-w", "--width"):
            targetWidth = int(arg)
        elif opt in ("-s", "--start"):
            startAt = int(arg)
        elif opt in ("-e", "--end"):
            endAt = int(arg)

    if inputfile == '':
        print 'resizeVideo.py -i <inputfile> -o <outputfile> -w <width> -h <height> -s <startsec> -e <endsec>'
    if outputfile == '':
        inputfilesplit = inputfile.rsplit(".", 1)
        outputfile = "{}_edited.avi".format(inputfilesplit[0])
        print inputfilesplit


    cap = cv2.VideoCapture(inputfile)
    orgHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    orgWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    #orgHeight = int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
    #orgWidth = int(cap.get(cv.CV_CAP_PROP_FRAME_WIDTH))
    fps = cap.get(cv2.CAP_PROP_FPS)
    #fps = cap.get(cv.CV_CAP_PROP_FPS)
    #totalFrames = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
    totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    anyChange = False
    if not startAt == 0:
        startAt = int(startAt * fps) # turn seconds into frames

    if endAt == 0:
        endAt = totalFrames  # set end frame if not provided
    else :
        endAt = int(endAt * fps) # turn seconds into frames


    if targetWidth == 0:
        targetWidth = orgWidth
    else :
        anyChange = True
        changeSize = True

    if targetHeight == 0:
        targetHeight = orgHeight
    else :
        anyChange = True
        changeSize = True

    if startAt > 0:
        anyChange = True
    elif startAt < 0:
        print '-s <startsec> cannot be less than 0! '
        sys.exit(2)


    if endAt < startAt:
        print '-e <endsec> cannot be smaller than -s <startsec>! '
        sys.exit(2)
    elif endAt > totalFrames:
        print '-e <endsec> cannot be bigger than video size({})! '.format(totalFrames)
        sys.exit(2)
    elif not endAt == totalFrames :
        anyChange = True
    
    if not anyChange:
        print 'Nothing to do here with there arguments you provided.'
        sys.exit(2)

    print "Input file is {}".format(inputfile)
    print "Output file is {}".format(outputfile)
    print "Target size is: {}-{}".format(targetWidth,targetHeight)
    print "Crop between : {}-{}".format(startAt,endAt)

    editVideo()    

if __name__ == "__main__":
    main(sys.argv[1:])
