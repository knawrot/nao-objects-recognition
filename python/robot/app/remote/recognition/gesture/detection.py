# Description:
#

import cv2
import numpy as np
from naoqi import ALProxy
from recognition.constants import SKIN_LOWER_BOUNDARY, SKIN_UPPER_BOUNDARY, MIN_HAND_AREA, OPEN_PALM_SOLIDITY_UPPER_BOUNDARY, FIST_SOLIDITY_LOWER_BOUNDARY

#MIN_HAND_AREA = 3200 # minimum hand area
#OPEN_PALM_SOLIDITY_UPPER_BOUNDARY = 0.6
#FIST_SOLIDITY_LOWER_BOUNDARY = 0.7
#SKIN_LOWER_BOUNDARY = (0,16,39)
#SKIN_UPPER_BOUNDARY = (20,78,255)

class BasicFrameProcessing(object):
	""" A basic module to test camera """
        		
	def checkContours(self, contours):
		contours = sorted(contours, key=cv2.contourArea, reverse=True)
		maxContour = contours[0]
		hull = cv2.convexHull(maxContour)
		area = cv2.contourArea(maxContour)
		if (len(contours) > 1 and float(cv2.contourArea(contours[1]))/cv2.contourArea(maxContour) > 0.2) or area < MIN_HAND_AREA:
			return -1, hull, maxContour
		hull_area = cv2.contourArea(hull)
		solidity = float(area)/hull_area
		print solidity, area
		if solidity < OPEN_PALM_SOLIDITY_UPPER_BOUNDARY:
			return 1, hull, maxContour
		elif solidity > FIST_SOLIDITY_LOWER_BOUNDARY:
			return 0, hull, maxContour
		else:
			return -1, hull, maxContour


def setup():
	global memory, basicFrameProcessing
	memory = ALProxy("ALMemory")
	basicFrameProcessing = BasicFrameProcessing()
		
def detect(img):  
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	thresh1 = cv2.inRange(hsv, SKIN_LOWER_BOUNDARY, SKIN_UPPER_BOUNDARY)
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
	eroded = cv2.erode(thresh1, kernel, iterations = 2)
	dilated = cv2.dilate(eroded, kernel, iterations = 2)
	contours,_ = cv2.findContours(dilated.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	if len(contours) > 0:
		status,hull,maxContour = basicFrameProcessing.checkContours(contours)
		if status != -1:
			#memory.raiseEvent("HandDetectedEvent", status)
			cv2.drawContours(img,[maxContour],0,(0,255,0),2) 
			cv2.drawContours(img,[hull],0,(0,0,255),2) 
			
	contoursImage = cv2.cvtColor(dilated,cv2.COLOR_GRAY2BGR)
	both = np.hstack((img,contoursImage))
	cv2.imshow("Detection of palm", both)
	
	key = cv2.waitKey(25)
	if key == ord('a'):
		return "abort"
	elif key == ord('q'):
		return "quit"

	return True
	