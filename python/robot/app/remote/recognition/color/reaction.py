import time
import threading
from naoqi import ALProxy, ALModule

shutdownThread = False

class ReactionModule(ALModule):
	""" A basic module to test events """
	
	def __init__(self, name):
		ALModule.__init__(self, name)
		self.name = name
		self.memory = ALProxy("ALMemory")
		self.motion = ALProxy("ALMotion")
		self.memory.subscribeToEvent("ColorDetectedEvent", name, "handleDetection")
		
        
	def handleDetection(self, key, value, message):
		""" A method that handles detection of the color. """
		names = ['HeadYaw', 'HeadPitch']
		times = [[0.01], [0.01]] # what is the fastest rate?
		xStep = 0.03
		yStep = 0.022
		moveX = -xStep if value[0]>0 else xStep if value[0]<0 else 0.0 # since robot camera has a mirror view, we need to alternate directions
		moveY = yStep if value[1]>0 else -yStep if value[1]<0 else 0.0
		print moveX, moveY
		self.memory.unsubscribeToEvent("ColorDetectedEvent", self.name)
		self.motion.angleInterpolation(names, [moveX, moveY], times, False)
		self.memory.subscribeToEvent("ColorDetectedEvent", self.name, "handleDetection")
		
	def disconnect(self):
		try:
			self.memory.unsubscribeToEvent("ColorDetectedEvent", self.getName())
		except BaseException, err:
			print "Error while disconnecting from color reaction module: " + str(err)
		

def stayAlive():
	global shutdownThread
	try:
		while not shutdownThread:
			time.sleep(1)
	except KeyboardInterrupt:
		print

def stiffnessOn(proxy):
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
	
def setup():   
	motionProxy = ALProxy("ALMotion")
	stiffnessOn(motionProxy)
		
	t = threading.Thread(target=stayAlive)
	t.start()
	
