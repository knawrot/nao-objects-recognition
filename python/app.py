from naoqi import ALProxy, ALModule, ALBroker
import sys
import cv2
import numpy as np
import sample

# constants
NAO_IP = "169.254.76.7"
NAO_PORT = 9559
# global
NaoWorkingMode = None


class BasicVideoProcessing(object):
	""" A class that handles some basic operations with NAO's camera. """
	
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
		
		
class SpeechDetectionModule(ALModule):
	""" A module that handles NAO recognition app commands. """
	
	def __init__(self, name):
		ALModule.__init__(self, name)
		self.name = name
		self.memory = ALProxy("ALMemory")
		self.asr = ALProxy("ALSpeechRecognition")
		self.asr.setLanguage("English")
		vocabulary = ["color", "text", "hand", "phone"]
		self.asr.setVocabulary(vocabulary, False)
		self.asr.subscribe(self.getName())
		self.memory.subscribeToEvent("WordRecognized", self.getName(), "onWordRecognized")
	
	def onWordRecognized(self, key, value, message):	
		""" A method that handles command recognition. """
		global NaoWorkingMode
		if(len(value) > 1 and value[1] >= 0.5):
			print 'recognized the word :', value[0]
			NaoWorkingMode = value[0]
		else:
			print 'unsifficient threshold'
			NaoWorkingMode = None

			
		
def main():  
	myBroker = ALBroker("NaoAppBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       NAO_IP,      # parent broker IP
       NAO_PORT)    # parent broker port
	
		
	global SpeechDetection, NaoWorkingMode
	SpeechDetection = SpeechDetectionModule("SpeechDetection")
	basicVideoProcessing = BasicVideoProcessing()
	basicVideoProcessing.connectToCamera()
	
	try:
		while True:
			img = basicVideoProcessing.getImageFromCamera()
			if (img == None):
				print "Image from camera is empty!"
				break
			else:
				if NaoWorkingMode == None:
					sample.sample()
				elif NaoWorkingMode == "color":
					print 'Working in color detection mode...'
					#cv2.imshow('Color', img) - cos nie dziala, pewnie kwestia tego, ze to kod ladowany jako modul
				elif NaoWorkingMode == "text":
					print 'Working in text detection mode...'
				elif NaoWorkingMode == "hand":
					print 'Working in hand gesture detection mode...'
				elif NaoWorkingMode == "phone":
					print 'Working in mobile phone detection mode...'
	except KeyboardInterrupt:
		print "Interrupted by user, shutting down"
	except RuntimeError, err:
		print "An error occured: " + str(err)
		
	cv2.destroyAllWindows()
	basicVideoProcessing.disconnectFromCamera()
	myBroker.shutdown()
	sys.exit(0)


	
if __name__ == "__main__":
    main()
	