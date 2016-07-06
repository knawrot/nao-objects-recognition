from naoqi import ALProxy
import time, sys
import cv2
import numpy as np

NAO_IP = "127.0.0.1"
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

	def isWindowEmpty(self, r):
		(_,_,w,h) = r
		return (w <= 0) or (h <= 0)
	
	def setWindowAsFrameSize(self, frame):
		width = np.size(frame, 1)
		height = np.size(frame, 0)
		window = (0,0,width,height)
		return window
		
		
def main():  
	memory = ALProxy("ALMemory", NAO_IP, NAO_PORT)
	basicVideoProcessing = BasicVideoProcessing()
	basicVideoProcessing.connectToCamera()
		
	track = (0,0,0,0)
	term = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
	
	try:
		while True:
			img = basicVideoProcessing.getImageFromCamera()
			if (img == None):
				print "Img is empty"
				break
			else:
				if basicVideoProcessing.isWindowEmpty(track):
					track = basicVideoProcessing.setWindowAsFrameSize(img )
				else:
					center = retn[1]
					memory.raiseEvent("RedBallDetectedEvent", (640-center[0], 480-center[1]))
					
				hsv_w = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
				#mask1 = cv2.inRange(hsv_w, (0,204,138), (3,210,254))
				#mask2 = cv2.inRange(hsv_w, (171,173,51), (176,209,77))
				acmask = cv2.inRange(hsv_w, np.array([110,125,61]), np.array([144,156,136]))
				acmask = cv2.erode(acmask, None, iterations=1)
				acmask = cv2.dilate(acmask, None, iterations=1)
				hist = cv2.calcHist([hsv_w],[0,1],acmask,[180,255],[0,180,0,255])
				cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)
				dst = cv2.calcBackProject([hsv_w],[0,1],hist,[0,180,0,255],1)
				
				retn, track = cv2.CamShift(dst, track, term)
				
	except BaseException, err:
		print "Undefined error: " + str(err)
	
	basicVideoProcessing.disconnectFromCamera()
	sys.exit(0)



if __name__ == "__main__":
    main()