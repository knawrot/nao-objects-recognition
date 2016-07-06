from naoqi import ALProxy
import time, sys
import cv2
import numpy as np
from collections import Counter

NAO_IP = "169.254.113.113"
NAO_PORT = 9559
MIN_RATIO_OF_SCREEN = 0.33	# ratio for telephone screen

class BasicVideoProcessing(object):
	""" A basic module to test camera """
	
	def __init__(self):
		self.camProxy = ALProxy("ALVideoDevice", NAO_IP, NAO_PORT)		
        
	def connectToCamera(self):
		try:
			clientName = "red-ball-client"
			cameraNum = 0
			resolutionOptNum = 1
			colorspaceOptNum = 13
			fpsNum = 20
			self.clientId = self.camProxy.subscribeCamera(clientName, cameraNum, resolutionOptNum, colorspaceOptNum, fpsNum)
		except BaseException, err:
			print "Error while connecting camera: " + str(err)
			
	def disconnectFromCamera(self):
		try:
			self.camProxy.unsubscribe(self.clientId)
		except BaseException, err:
			print "Error while disconnecting camera: " + str(err)
			
	def getImageFromCamera(self):
		try:
			dataImage = self.camProxy.getImageRemote(self.clientId)
			if (dataImage != None):
				image = np.reshape(np.frombuffer(dataImage[6], dtype='%iuint8' % dataImage[2]), (dataImage[1], dataImage[0], dataImage[2]))
				return image
		except BaseException, err:
			print "Error while getting image from camera: " + str(err)
		return None
		
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
		for f in sortedNumOfChildren.most_common(10):
			candidates.append(contours[f[0]])
		for c in candidates:
			peri = cv2.arcLength(c, True)
			approx = cv2.approxPolyDP(c, 0.02 * peri, True)
			_,_,w,h = cv2.boundingRect(c)
			aspectRatio = float(w)/h
			if len(approx) == 4 and aspectRatio > MIN_RATIO_OF_SCREEN:
				screenCandidates.append(c)
		return max(screenCandidates, key=cv2.contourArea) if screenCandidates else np.array([])


		
def main():  
	memory = ALProxy("ALMemory", NAO_IP, NAO_PORT)
	basicVideoProcessing = BasicVideoProcessing()
	basicVideoProcessing.connectToCamera()
	
	try:
		while True:
			img = basicVideoProcessing.getImageFromCamera()
			if (img == None):
				print "Img is empty"
				break
			else:
				gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				gray = cv2.bilateralFilter(gray, 11, 17, 17)
				edged = basicVideoProcessing.autoCanny(gray)
				#_,th1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
				#th2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 1)
				kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
				#eroded = cv2.erode(edged, kernel, iterations = 1)
				dilated = cv2.dilate(edged, kernel, iterations = 2)
				contours,hierarchy = cv2.findContours(dilated.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
				contoursWithMostChildren = basicVideoProcessing.sortContoursByChildrenAndArea(contours,hierarchy[0])
				if contoursWithMostChildren.size:
					memory.raiseEvent("PhoneDetectedEvent", 1)
					print contoursWithMostChildren.size
					cv2.drawContours(img,contoursWithMostChildren,-1,(0,0,255),2) 
					
				edged = cv2.cvtColor(dilated,cv2.COLOR_GRAY2BGR)
				both = np.hstack((img,edged))
				cv2.imshow("Detection of text", both)
				
				key = cv2.waitKey(25)
				if key == ord('a'):
					break
	except BaseException, err:
		print "Undefined error: " + str(err)
	
	cv2.destroyAllWindows()
	basicVideoProcessing.disconnectFromCamera()
	sys.exit(0)



if __name__ == "__main__":
    main()