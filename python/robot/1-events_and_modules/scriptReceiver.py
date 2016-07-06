from naoqi import ALModule, ALProxy

NAO_IP = "127.0.0.1"
NAO_PORT = 9559

class BasicEventHandlingModule(ALModule):
	""" A basic module to test events """
	
	def __init__(self, name):
		ALModule.__init__(self, name)
		self.tts = ALProxy("ALTextToSpeech")
		self.memory = ALProxy("ALMemory")
		self.memory.subscribeToEvent("BasicEvent", name, "handleEvent")
		
        
	def handleEvent(self, key, value, message):
		""" A method that handles the CODE. """
		self.tts.say("Received the event with value " + str(value))
		

from naoqi import ALBroker
import time, sys
		
def main():
	myBroker = ALBroker("basicEventHandlingBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       NAO_IP,      # parent broker IP
       NAO_PORT)    # parent broker port
	   
	global BasicEventHandling
	BasicEventHandling = BasicEventHandlingModule("BasicEventHandling")
	
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