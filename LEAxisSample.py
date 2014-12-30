import cv2
import numpy as np
import locationEstimator as le

cap = cv2.VideoCapture('./sample/sample2.avi')
estimator = le.LocationEstimator('./sample/calibration/calibration.npz', showPositions=True)

while cap.isOpened:
    f, frame = cap.read()
    estimator.checkSettings()
    frame2 = estimator.draw3dAxis(frame)
    
    cv2.imshow("axis", frame2)
    if cv2.waitKey(20) != -1:
        cap.release()
        cv2.destroyAllWindows()
        break
