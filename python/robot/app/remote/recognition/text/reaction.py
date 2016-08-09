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
		self.memory.subscribeToEvent("TextDetectedEvent", name, "handleDetection")
		
        
	def handleDetection(self, key, value, message):
		""" A method that handles detection. """
		self.memory.unsubscribeToEvent("TextDetectedEvent", self.name)
		self.tts.say("I see some text. Unfortunately, I can't read it!")
		self.memory.subscribeToEvent("TextDetectedEvent", self.name, "handleDetection")
		
	def disconnect(self):
		try:
			self.memory.unsubscribeToEvent("TextDetectedEvent", self.getName())
		except BaseException, err:
			print "Error while disconnecting from text reaction module: " + str(err)

		
def stayAlive():
	try:
		while not shutdownThread:
			time.sleep(1)
	except KeyboardInterrupt:
		print
		
def setup():   
	t = threading.Thread(target=stayAlive)
	t.start()		
