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
		self.posture = ALProxy("ALRobotPosture")
		self.memory = ALProxy("ALMemory")
		self.memory.subscribeToEvent("HandDetectedEvent", name, "handleDetection")
		
        
	def handleDetection(self, key, value, message):
		""" A method that handles detection of the ball. """
		self.memory.unsubscribeToEvent("HandDetectedEvent", self.name)
		if value == 0 and self.posture.getPostureFamily() != "Sitting":
			self.posture.goToPosture("Sit", 1.0)
		elif value == 1 and self.posture.getPostureFamily() != "Standing":
			self.posture.goToPosture("Stand", 1.0)
		self.memory.subscribeToEvent("HandDetectedEvent", self.name, "handleDetection")
		
	def disconnect(self):
		try:
			self.memory.unsubscribeToEvent("HandDetectedEvent", self.getName())
		except BaseException, err:
			print "Error while disconnecting from gesture reaction module: " + str(err)

			
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
	