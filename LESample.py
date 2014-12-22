import locationEstimator as le
import locationEstimator_old as leo

estimator = le.LocationEstimator('./sample/calibration/calibration.npz')
#estimator = leo.LocationEstimator('./sample/calibration/calibration.npz')

print "1: {}".format(estimator.get3dCoordinates(270,234))
print "2: {}".format(estimator.get3dCoordinates(372,150))
print "3: {}".format(estimator.get3dCoordinates(532,203))
print "4: {}".format(estimator.get3dCoordinates(458,311))
print "5: {}".format(estimator.get3dCoordinates(408,218))

#print "0-0: {}".format(estimator.get3dCoordinates(0,0))
#print "320-0: {}".format(estimator.get3dCoordinates(320,0))
#print "640-0: {}".format(estimator.get3dCoordinates(640,0))
#print "640-240: {}".format(estimator.get3dCoordinates(640,240))
#print "640-480: {}".format(estimator.get3dCoordinates(640,480))
#print "320-480: {}".format(estimator.get3dCoordinates(320,480))
#print "0-480: {}".format(estimator.get3dCoordinates(0,480))
#print "0-240: {}".format(estimator.get3dCoordinates(0,240))
