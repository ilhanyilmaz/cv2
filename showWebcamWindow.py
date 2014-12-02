import cv2

capture = cv2.VideoCapture(0)

while capture.isOpened :
    f,frame = capture.read()
    cv2.imshow('frame', frame)
    if(cv2.waitKey(27)!=-1):
        capture.release()
        cv2.destroyAllWindows()
        break
