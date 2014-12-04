import cv2

class VideoPlayer():

    def __init__(self, capture, wait=50, show=True):
        self.capture = capture
        self.waitLength = wait
        self.playing = True
        self.step = 1
        self.show = show
    def loop(self):
        key = -1
        currentPos = self.capture.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
        nextPos = currentPos + self.step
        self.capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, nextPos)
        if self.show:
            ret, image = self.capture.retrieve()
            cv2.imshow('video player',image)
        if self.playing == True:
            key = cv2.waitKey(self.waitLength)
        else:
            key = cv2.waitKey(0)
        
        if key == 27: #ESCAPE
            self.capture.release()
            cv2.destroyAllWindows()     
        elif key == 32: # SPACE
            self.playing = not self.playing
        elif key == 65361: #LEFT
            self.slower()
            #currentPos = currentPos - 1            
            #currentPos = capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, currentPos-1)
        elif key == 65363: #RIGHT
            self.faster()
            #currentPos = currentPos + 1            
            #currentPos = capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, currentPos+1)
        elif not key == -1:
            print "pressed key: " + str(key)
            return key

    def faster(self):
        if self.step == -25:
            self.step = -5
        elif self.step == -5:
            self.step = -1
        elif self.step == -1:
            self.step = 0
        elif self.step == 0:
            self.step = 1
        elif self.step == 1:
            self.step = 5
        elif self.step == 5:
            self.step = 25
        print self.step

    def slower(self):
        if self.step == -5:
            self.step = -25
        elif self.step == -1:
            self.step = -5
        elif self.step == 0:
            self.step = -1
        elif self.step == 1:
            self.step = 0
        elif self.step == 5:
            self.step = 1
        elif self.step == 25:
            self.step = 5
        print self.step
 
