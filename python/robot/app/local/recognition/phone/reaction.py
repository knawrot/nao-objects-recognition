import time
import threading
from naoqi import ALModule, ALProxy

shutdownThread = False

class ReactionModule(ALModule):
	""" A basic module to test events """
	
	def __init__(self, name):
		ALModule.__init__(self, name)
		self.name = name
		self.tts = ALProxy("ALTextToSpeech")
		self.memory = ALProxy("ALMemory")
		self.memory.subscribeToEvent("PhoneDetectedEvent", name, "handleDetection")
		
	def handleDetection(self, key, value, message):
		""" A method that handles detection of the ball. """
		self.memory.unsubscribeToEvent("PhoneDetectedEvent", self.name)
		self.tts.say("I see phone!")
		self.memory.subscribeToEvent("PhoneDetectedEvent", self.name, "handleDetection")
		
	def disconnect(self):
		try:
			self.memory.unsubscribeToEvent("PhoneDetectedEvent", self.getName())
		except BaseException, err:
			print "Error while disconnecting from phone reaction module: " + str(err)

			
def stayAlive():
	global shutdownThread
	try:
		while not shutdownThread:
			time.sleep(1)
	except KeyboardInterrupt:
		print
	
	
def setup():
	t = threading.Thread(target=stayAlive)
	t.start()