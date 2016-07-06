from naoqi import ALModule, ALProxy

NAO_IP = "169.254.113.113"
NAO_PORT = 9559

class RedBallDetectionModule(ALModule):
	""" A basic module to test events """
	
	def __init__(self, name):
		ALModule.__init__(self, name)
		self.name = name
		self.tts = ALProxy("ALTextToSpeech")
		self.memory = ALProxy("ALMemory")
		self.memory.subscribeToEvent("HandDetectedEvent", name, "handleBallDetection")
		
        
	def handleBallDetection(self, key, value, message):
		""" A method that handles detection of the ball. """
		self.memory.unsubscribeToEvent("HandDetectedEvent", self.name)
		if value == 0:
			self.tts.say("closed!")
		elif value == 1:
			self.tts.say("open")
		self.memory.subscribeToEvent("HandDetectedEvent", self.name, "handleBallDetection")
		

from naoqi import ALBroker
import time, sys
		
def main():
	myBroker = ALBroker("SimpleRedBallDetectionBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       NAO_IP,      # parent broker IP
       NAO_PORT)    # parent broker port
	   
	global RedBallDetection
	RedBallDetection = RedBallDetectionModule("RedBallDetection")
	
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		print
		print "Interrupted by user, shutting down"
		myBroker.shutdown()
		sys.exit(0)



if __name__ == "__main__":
    main()