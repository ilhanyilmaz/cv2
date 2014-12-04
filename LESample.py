import locationEstimator as le

estimator = le.LocationEstimator('./sample/calibration/calibration.npy.npz')
print estimator.get3dCoordinates(100,100)
