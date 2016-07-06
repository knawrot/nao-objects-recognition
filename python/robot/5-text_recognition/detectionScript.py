from naoqi import ALProxy
import time, sys
import cv2
import numpy as np

NAO_IP = "169.254.113.113"
NAO_PORT = 9559
MIN_RATIO_OF_SIMILIAR_OBJECTS = 0.65 	# letters in paragraph are supposed to have similiar height/width ratio
MIN_AREA_OF_SIMILIAR_OBJECTS = 0.5 		# letters in paragraph are supposed to occupy same area (i.e. have roughly equal size)
MIN_CONTOURS_DETECTED = 100
#red boundaries - (169,177,0), (180,232,117)

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
	
	def extractContoursStatistics(self, contours):
		contourBoundingRectAreas = []
		contourBoundingRectRatios = []
		for i in contours:
			_,_,w,h = cv2.boundingRect(i)
			contourBoundingRectAreas.append(w*h)
			contourBoundingRectRatios.append(float(w)/h)
		return np.median(contourBoundingRectAreas), np.mean(contourBoundingRectAreas), np.median(contourBoundingRectRatios), np.mean(contourBoundingRectRatios)


		
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
				gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
				edged = basicVideoProcessing.autoCanny(gray)
				contours,_ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			
				if len(contours) > MIN_CONTOURS_DETECTED: # simple condition to prevent constant evaluation of contours when it doesn't make sense
					areaMedian, areaMean, ratioMedian, ratioMean = basicVideoProcessing.extractContoursStatistics(contours)
					if ratioMedian/ratioMean >= MIN_RATIO_OF_SIMILIAR_OBJECTS and areaMedian/areaMean >= MIN_AREA_OF_SIMILIAR_OBJECTS:
						memory.raiseEvent("TextDetectedEvent", 1)
					
				contoursImage = cv2.cvtColor(edged,cv2.COLOR_GRAY2BGR)
				both = np.hstack((img,contoursImage))
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