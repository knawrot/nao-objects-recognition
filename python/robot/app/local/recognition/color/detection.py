# Description:
#

import cv2
import numpy as np
from naoqi import ALProxy
from recognition.constants import COLOR_LOWER_BOUNDARY, COLOR_UPPER_BOUNDARY

track = (0,0,0,0)
term = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)	
retn = None
memory = None
basicFrameProcessing = None
	
	
class BasicFrameProcessing(object):
	""" A class to do some basic calculations on a particular frame. """
	
	def __init__(self):	
		self.frameCenterBox = self.calculateWindowCenterBox(320, 240) # for given resolutionOptNum
        
	def isWindowEmpty(self, r):
		(_,_,w,h) = r
		return (w <= 0) or (h <= 0)
	
	def calculateWindowAsFrame(self, frame):
		wd = np.size(frame, 1)
		ht = np.size(frame, 0)
		window = (0,0,wd,ht)
		return window
		
	def calculateWindowCenterBox(self, width, height):
		self.centerPoint = (width/2, height/2)
		scale = 0.1
		vector = (width * scale, height * scale)
		rectangle = [(self.centerPoint[0] - int(vector[0]), self.centerPoint[1] - int(vector[1])), (self.centerPoint[0] + int(vector[0]), self.centerPoint[1] + int(vector[1]))]
		return rectangle
	
	
		
def setup():
	global memory, basicFrameProcessing
	memory = ALProxy("ALMemory")
	basicFrameProcessing = BasicFrameProcessing()

	
def detect(img):  
	try:
		global track, retn
		if basicFrameProcessing.isWindowEmpty(track):
			track = basicFrameProcessing.calculateWindowAsFrame(img)
		else:
			if basicFrameProcessing.frameCenterBox[0][0] > retn[0][0] or retn[0][0] > basicFrameProcessing.frameCenterBox[1][0] or basicFrameProcessing.frameCenterBox[0][1] > retn[0][1] or retn[0][1] > basicFrameProcessing.frameCenterBox[1][1]:
				vector = [retn[0][0] - basicFrameProcessing.centerPoint[0], retn[0][1] - basicFrameProcessing.centerPoint[1]]
				if basicFrameProcessing.frameCenterBox[0][0] < retn[0][0] < basicFrameProcessing.frameCenterBox[1][0]:
					vector = [0, vector[1]]
				if basicFrameProcessing.frameCenterBox[0][1] < retn[0][1] < basicFrameProcessing.frameCenterBox[1][1]:
					vector = [vector[0], 0]
				memory.raiseEvent("ColorDetectedEvent", vector)
		
		hsv_w = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
		acmask = cv2.inRange(hsv_w, np.array(COLOR_LOWER_BOUNDARY), np.array(COLOR_UPPER_BOUNDARY))
		#mask2 = cv2.inRange(hsv_w, (166,122,171), (180,250,255))
		#acmask = mask1 | mask2
		acmask = cv2.erode(acmask, None, iterations=1)
		acmask = cv2.dilate(acmask, None, iterations=1)
		hist = cv2.calcHist([hsv_w],[0,1],acmask,[180,255],[0,180,0,255])
		cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)
		dst = cv2.calcBackProject([hsv_w],[0,1],hist,[0,180,0,255],1)
		
		retn, track = cv2.CamShift(dst, track, term)
		
	except KeyboardInterrupt:
		print "Interrupted by user, shutting down..."
		return False

	return True