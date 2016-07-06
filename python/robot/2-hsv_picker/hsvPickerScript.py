from naoqi import ALProxy
import time, sys
import cv2
import numpy

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
				image = numpy.reshape(numpy.frombuffer(dataImage[6], dtype='%iuint8' % dataImage[2]), (dataImage[1], dataImage[0], dataImage[2]))
				return image
		except BaseException, err:
			print "Error while getting image from camera: " + str(err)
		return None


		
def doNothing(x):
	pass

def printRange(event,x,y,flags,param):
	if event == cv2.EVENT_LBUTTONDBLCLK:
		print '(%s,%s,%s), (%s,%s,%s)' % (h_min,s_min,v_min,h_max,s_max,v_max)
		
def main():  
	basicVideoProcessing = BasicVideoProcessing()
	basicVideoProcessing.connectToCamera()
	
	cv2.namedWindow('color-range-window')

	# create trackbars for color change
	cv2.createTrackbar('H_min','color-range-window',0,180,doNothing)
	cv2.createTrackbar('H_max','color-range-window',0,180,doNothing)
	cv2.createTrackbar('S_min','color-range-window',0,255,doNothing)
	cv2.createTrackbar('S_max','color-range-window',0,255,doNothing)
	cv2.createTrackbar('V_min','color-range-window',0,255,doNothing)
	cv2.createTrackbar('V_max','color-range-window',0,255,doNothing)
	cv2.setMouseCallback('color-range-window',printRange)
	
	try:
		while True:
			img = basicVideoProcessing.getImageFromCamera()
			if (img == None):
				print "Img is empty"
				break
			else:
				h_min = cv2.getTrackbarPos('H_min','color-range-window')
				h_max = cv2.getTrackbarPos('H_max','color-range-window')
				s_min = cv2.getTrackbarPos('S_min','color-range-window')
				s_max = cv2.getTrackbarPos('S_max','color-range-window')
				v_min = cv2.getTrackbarPos('V_min','color-range-window')
				v_max = cv2.getTrackbarPos('V_max','color-range-window')
				
				hsv_w = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
				mask = cv2.inRange(hsv_w, (h_min,s_min,v_min), (h_max,s_max,v_max))
				
				cv2.imshow('color-range-window', mask)
				cv2.imshow('original-frame', img)
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