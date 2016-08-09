# Description:
#

import cv2
import numpy as np
from naoqi import ALProxy
from collections import Counter
from recognition.constants import MIN_RATIO_OF_SCREEN, MIN_NUM_OF_CONTOURS, BRIGHT_OBJECTS_THRESHOLD

#MIN_RATIO_OF_SCREEN = 0.7	# ratio for telephone screen
#MIN_NUM_OF_CONTOURS = 10	# minimum number of objects (icons, letters etc) for telephone screen
#BRIGHT_OBJECTS_THRESHOLD = 200

class BasicFrameProcessing(object):
	""" A basic module to test camera """
		
	def autoCanny(self, image, sigma=0.33):
		v = np.median(image)
		lower = int(max(0, (1.0 - sigma) * v))
		upper = int(min(255, (1.0 + sigma) * v))
		edged = cv2.Canny(image, lower, upper)
		return edged
	
	def sortContoursByChildrenAndArea(self, contours, hierarchy):
		numOfChildren = [i[-1] for i in hierarchy]
		sortedNumOfChildren = Counter(numOfChildren)
		del sortedNumOfChildren[-1]
		screenCandidates = []
		candidates = []
		for f in sortedNumOfChildren.most_common(5):
			if f[1] > MIN_NUM_OF_CONTOURS:
				candidates.append(contours[f[0]])
		for c in candidates:
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.05 * peri, True)
			x,y,w,h = cv2.boundingRect(c)
			aspectRatio = float(w)/h
			if len(approx) == 4 and aspectRatio < MIN_RATIO_OF_SCREEN:
				screenCandidates.append(c)
		return max(screenCandidates, key=cv2.contourArea) if screenCandidates else np.array([])


		
def setup():
	global memory, basicFrameProcessing
	memory = ALProxy("ALMemory")
	basicFrameProcessing = BasicFrameProcessing()
	
def detect(img): 
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.bilateralFilter(gray, 10, 20, 20)
	_,th1 = cv2.threshold(gray,BRIGHT_OBJECTS_THRESHOLD,255,cv2.THRESH_BINARY)
	edged = basicFrameProcessing.autoCanny(th1)
	#th2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 1)
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
	#eroded = cv2.erode(edged, kernel, iterations = 1)
	dilated = cv2.dilate(edged, kernel, iterations = 2)
	contours,hierarchy = cv2.findContours(dilated.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	if hierarchy is not None and hierarchy.size:
		contoursWithMostChildren = basicFrameProcessing.sortContoursByChildrenAndArea(contours,hierarchy[0])
		if contoursWithMostChildren.size:
			memory.raiseEvent("PhoneDetectedEvent", 1)
			cv2.drawContours(img,contoursWithMostChildren,-1,(0,0,255),2) 
		
	edged = cv2.cvtColor(edged,cv2.COLOR_GRAY2BGR)
	both = np.hstack((img,edged))
	cv2.imshow("Detection of text", both)
	
	key = cv2.waitKey(25)
	if key == ord('a'):
		return "abort"
	elif key == ord('q'):
		return "quit"

	return True