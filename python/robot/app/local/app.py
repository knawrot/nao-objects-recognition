import sys
from time import sleep
from importlib import import_module
import numpy as np
from naoqi import ALProxy, ALModule, ALBroker

# constants
NAO_IP = "127.0.0.1"
NAO_PORT = 9559
# global
NaoWorkingMode = None


class BasicVideoProcessing(object):
	""" A class that handles some basic operations with NAO's camera. """
	
	def __init__(self):
		self.camProxy = ALProxy("ALVideoDevice")		
        
	def connectToCamera(self):
		try:
			clientName = "nao-app-client"
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
		vocabulary = ["color", "text", "gesture", "phone"]
		self.asr.setVocabulary(vocabulary, False)
		self.asr.subscribe(self.getName())
		self.memory.subscribeToEvent("WordRecognized", self.getName(), "onMyWordRecognized")
	
	def onMyWordRecognized(self, key, value, message):	
		""" A method that handles command recognition. """
		global NaoWorkingMode
		if(len(value) > 1 and value[1] >= 0.5):
			print 'recognized the word :', value[0]
			NaoWorkingMode = value[0]
		else:
			print 'unsifficient threshold'
			NaoWorkingMode = None
			
	def disconnect(self):
		try:
			self.memory.unsubscribeToEvent("WordRecognized", self.getName())
			self.asr.unsubscribe(self.getName())
		except BaseException, err:
			print "Error while disconnecting from speech module: " + str(err)

			
		
def main():  
	myBroker = ALBroker("NaoAppBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       NAO_IP,      # parent broker IP
       NAO_PORT)    # parent broker port
	
		
	global SpeechDetection, NaoWorkingMode
	SpeechDetection = SpeechDetectionModule("SpeechDetection")
	NaoWorkingMode = None
		
	try:
		while NaoWorkingMode not in ["color", "text", "gesture", "phone"]:
			pass
		
		SpeechDetection.disconnect()
		
		print 'Working in ' + NaoWorkingMode + ' detection mode...'
		proxyDetection = import_module('recognition.' + NaoWorkingMode + '.detection')
		proxyReaction = import_module('recognition.' + NaoWorkingMode + '.reaction')	
		global ReactionUnit
		ReactionUnit = proxyReaction.ReactionModule("ReactionUnit")			
			
		proxyDetection.setup()
		proxyReaction.setup()
		basicVideoProcessing = BasicVideoProcessing()
		basicVideoProcessing.connectToCamera()
	    
		sleep(1) # wait a second for the camera to get proper amount of lightning (not overflooded by light on startup)
		
		while True:
			img = basicVideoProcessing.getImageFromCamera()
			if (img == None):
				print "Image from camera is empty!"
				break
			else:
				if not proxyDetection.detect(img):
					break
			
	except KeyboardInterrupt:
		print "Interrupted by user, shutting down..."
	except RuntimeError, err:
		print "An error occured: " + str(err)
	
	proxyReaction.shutdownThread = True
	ReactionUnit.disconnect()
	basicVideoProcessing.disconnectFromCamera()
	myBroker.shutdown()
	sys.exit(0)


	
if __name__ == "__main__":
    main()
	