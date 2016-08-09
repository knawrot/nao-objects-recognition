# Description:
#

import cv2
import numpy as np
from naoqi import ALProxy
from recognition.constants import MIN_RATIO_OF_SIMILIAR_OBJECTS, MIN_AREA_OF_SIMILIAR_OBJECTS, MIN_CONTOURS_DETECTED

#MIN_RATIO_OF_SIMILIAR_OBJECTS = 0.65 	# letters in paragraph are supposed to have similiar height/width ratio
#MIN_AREA_OF_SIMILIAR_OBJECTS = 0.5 		# letters in paragraph are supposed to occupy same area (i.e. have roughly equal size)
#MIN_CONTOURS_DETECTED = 100

class BasicFrameProcessing(object):
	""" A basic module to test camera """	
		
	def autoCanny(self, image, sigma=0.33):
		v = np.median(image)
		lower = int(max(0, (1.0 - sigma) * v))
		upper = int(min(255, (1.0 + sigma) * v))
		edged = cv2.Canny(image, lower, upper)
		return edged
	
	def extractContoursStatistics(self, contours):
		contourBoundingRectAreas = []
		contourBoundingRectRatios = []
		for i in contours:
			_,_,w,h = cv2.boundingRect(i)
			contourBoundingRectAreas.append(w*h)
			contourBoundingRectRatios.append(float(w)/h)
		return np.median(contourBoundingRectAreas), np.mean(contourBoundingRectAreas), np.median(contourBoundingRectRatios), np.mean(contourBoundingRectRatios)


def setup():
	global memory, basicFrameProcessing
	memory = ALProxy("ALMemory")
	basicFrameProcessing = BasicFrameProcessing()
		
		
def detect(img):
	try:
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		edged = basicFrameProcessing.autoCanny(gray)
		contours,_ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		
		if contours is not None and len(contours) > MIN_CONTOURS_DETECTED: # simple condition to prevent constant evaluation of contours when it doesn't make sense
			areaMedian, areaMean, ratioMedian, ratioMean = basicFrameProcessing.extractContoursStatistics(contours)
			if ratioMedian/ratioMean >= MIN_RATIO_OF_SIMILIAR_OBJECTS and areaMedian/areaMean >= MIN_AREA_OF_SIMILIAR_OBJECTS:
				memory.raiseEvent("TextDetectedEvent", 1)
	except KeyboardInterrupt:
		return False
		
	return True
	