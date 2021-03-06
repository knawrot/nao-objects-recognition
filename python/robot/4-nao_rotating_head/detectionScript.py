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
		#self.vc = cv2.VideoCapture(0)
		self.frameCenterBox = self.calculateWindowCenterBox(320, 240) # for given resolutionOptNum
        
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
		#return self.vc.read()
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
					track = basicVideoProcessing.setWindowAsFrameSize(img)
				else:
					if basicVideoProcessing.frameCenterBox[0][0] > retn[0][0] or retn[0][0] > basicVideoProcessing.frameCenterBox[1][0] or basicVideoProcessing.frameCenterBox[0][1] > retn[0][1] or retn[0][1] > basicVideoProcessing.frameCenterBox[1][1]:
						#print retn[0], basicVideoProcessing.centerPoint, [retn[0][0] - basicVideoProcessing.centerPoint[0], retn[0][1] - basicVideoProcessing.centerPoint[1]]
						vector = [retn[0][0] - basicVideoProcessing.centerPoint[0], retn[0][1] - basicVideoProcessing.centerPoint[1]]
						if basicVideoProcessing.frameCenterBox[0][0] < retn[0][0] < basicVideoProcessing.frameCenterBox[1][0]:
							vector = [0, vector[1]]
						if basicVideoProcessing.frameCenterBox[0][1] < retn[0][1] < basicVideoProcessing.frameCenterBox[1][1]:
							vector = [vector[0], 0]
						memory.raiseEvent("RedBallDetectedEvent", vector)
						pts = cv2.cv.BoxPoints(retn)
						pts = np.int0(pts)
						cv2.polylines(img,[pts],True,255,2)
				
				cv2.rectangle(img,basicVideoProcessing.frameCenterBox[0],basicVideoProcessing.frameCenterBox[1],255,3)
				cv2.imshow('Detection',img)
				hsv_w = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
				mask1 = cv2.inRange(hsv_w, (0,124,178), (11,232,255))
				mask2 = cv2.inRange(hsv_w, (166,122,171), (180,250,255))
				acmask = mask1 | mask2
				acmask = cv2.erode(acmask, None, iterations=1)
				acmask = cv2.dilate(acmask, None, iterations=1)
				cv2.imshow('Mask',acmask)
				hist = cv2.calcHist([hsv_w],[0,1],acmask,[180,255],[0,180,0,255])
				cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)
				dst = cv2.calcBackProject([hsv_w],[0,1],hist,[0,180,0,255],1)
				
				retn, track = cv2.CamShift(dst, track, term)
				
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