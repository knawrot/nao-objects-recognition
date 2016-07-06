from naoqi import ALProxy
import time, sys
import cv2
import numpy as np

NAO_IP = "169.254.113.113"
NAO_PORT = 9559

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
		
	def checkContours(self, contours):
		contours = sorted(contours, key=cv2.contourArea, reverse=True)
		maxContour = contours[0]
		hull = cv2.convexHull(maxContour)
		if len(contours) > 1 and float(cv2.contourArea(contours[1]))/cv2.contourArea(maxContour) > 0.2:
			return -1, hull
		area = cv2.contourArea(maxContour)
		hull_area = cv2.contourArea(hull)
		solidity = float(area)/hull_area
		print solidity
		if solidity > 0.6:
			return 0, hull
		else:
			return 1, hull


		
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
				hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
				thresh1 = cv2.inRange(hsv, (0,100,38), (29,177,147))
				kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
				eroded = cv2.erode(thresh1, kernel, iterations = 3)
				dilated = cv2.dilate(eroded, kernel, iterations = 3)
				contours,_ = cv2.findContours(dilated.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
				
				if len(contours) > 0:
					status,hull = basicVideoProcessing.checkContours(contours)
					if status != -1:
						memory.raiseEvent("HandDetectedEvent", status)
						cv2.drawContours(img,[hull],0,(0,0,255),2) 
						
				contoursImage = cv2.cvtColor(dilated,cv2.COLOR_GRAY2BGR)
				both = np.hstack((img,contoursImage))
				cv2.imshow("Detection of palm", both)
				
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