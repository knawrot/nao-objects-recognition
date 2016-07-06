from naoqi import ALProxy, ALModule, ALBroker
import time, sys
import cv2
import numpy as np
import sample

# constants
NAO_IP = "169.254.76.7"
NAO_PORT = 9559
# global
naoWorkingMode = None

#TODO - ROZDZIELIC MODUL ROZPOZNAWANIA MOWY I OBSLUGI KAMERY

class SpeechDetectionModule(ALModule):
	""" A basic module to test speech """
	
	def __init__(self, name):
		ALModule.__init__(self, name)
		self.name = name
		self.camProxy = ALProxy("ALVideoDevice")		
		self.memory = ALProxy("ALMemory")
		self.asr = ALProxy("ALSpeechRecognition")
		self.asr.setLanguage("English")
		vocabulary = ["color", "text", "hand", "phone"]
		self.asr.setVocabulary(vocabulary, False)
		self.asr.subscribe(self.getName())
		self.memory.subscribeToEvent("WordRecognized", self.getName(), "onMyWordRecognized")
        
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
			self.memory.unsubscribeToEvent("WordRecognized", self.getName())
			self.asr.unsubscribe(self.getName())
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
	
	
	def onMyWordRecognized(self, key, value, message):	
		""" A method that handles speech reco. """
		global naoWorkingMode
		if(len(value) > 1 and value[1] >= 0.5):
			print 'recognized the word :', value[0]
			naoWorkingMode = value[0]
		else:
			print 'unsifficient threshold'
			naoWorkingMode = None

		
def main():  
	myBroker = ALBroker("NaoAppBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       NAO_IP,      # parent broker IP
       NAO_PORT)    # parent broker port
	
		
	global SpeechDetection
	SpeechDetection = SpeechDetectionModule("SpeechDetection")
	SpeechDetection.connectToCamera()
	
	global naoWorkingMode
	try:
		while True:
			img = SpeechDetection.getImageFromCamera()
			if (img == None):
				print "Img is empty"
				break
			else:
				if naoWorkingMode == None:
					sample.sample()
				elif naoWorkingMode == "color":
					print 'Working in color detection mode...'
					#cv2.imshow('Color', img) - cos nie dziala, pewnie kwestia tego, ze to kod ladowany jako modul
				elif naoWorkingMode == "text":
					print 'Working in text detection mode...'
				elif naoWorkingMode == "hand":
					print 'Working in hand gesture detection mode...'
				elif naoWorkingMode == "phone":
					print 'Working in mobile phone detection mode...'
	except KeyboardInterrupt:
		print
		print "Interrupted by user, shutting down"
	except RuntimeError, err:
		print "An error occured: " + str(err)
		
	cv2.destroyAllWindows()
	SpeechDetection.disconnectFromCamera()
	myBroker.shutdown()
	sys.exit(0)


	
if __name__ == "__main__":
    main()
	