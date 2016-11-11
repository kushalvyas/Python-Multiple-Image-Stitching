import cv2
import numpy as np 

class matchers:
	def __init__(self):
		self.surf = cv2.xfeatures2d.SURF_create()
		FLANN_INDEX_KDTREE = 0
		index_params = dict(algorithm=0, trees=5)
		search_params = dict(checks=50)
		self.flann = cv2.FlannBasedMatcher(index_params, search_params)

	def match(self, i1, i2, direction=None):
		imageSet1 = self.getSURFFeatures(i1)
		imageSet2 = self.getSURFFeatures(i2)
		print "Direction : ", direction
		matches = self.flann.knnMatch(
			imageSet2['des'],
			imageSet1['des'],
			k=2
			)
		good = []
		for i , (m, n) in enumerate(matches):
			if m.distance < 0.7*n.distance:
				good.append((m.trainIdx, m.queryIdx))

		if len(good) > 4:
			pointsCurrent = imageSet2['kp']
			pointsPrevious = imageSet1['kp']

			matchedPointsCurrent = np.float32(
				[pointsCurrent[i].pt for (__, i) in good]
			)
			matchedPointsPrev = np.float32(
				[pointsPrevious[i].pt for (i, __) in good]
				)

			H, s = cv2.findHomography(matchedPointsCurrent, matchedPointsPrev, cv2.RANSAC, 4)
			return H
		return None

	def getSURFFeatures(self, im):
		gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		kp, des = self.surf.detectAndCompute(gray, None)
		return {'kp':kp, 'des':des}