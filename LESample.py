import locationEstimator as le

estimator = le.LocationEstimator('./sample/calibration/calibration.npz')
print "0-0: {}".format(estimator.get3dCoordinates(0,0))
print "320-0: {}".format(estimator.get3dCoordinates(320,0))
print "640-0: {}".format(estimator.get3dCoordinates(640,0))
print "640-240: {}".format(estimator.get3dCoordinates(640,240))
print "640-480: {}".format(estimator.get3dCoordinates(640,480))
print "320-480: {}".format(estimator.get3dCoordinates(320,480))
print "0-480: {}".format(estimator.get3dCoordinates(0,480))
print "0-240: {}".format(estimator.get3dCoordinates(0,240))
