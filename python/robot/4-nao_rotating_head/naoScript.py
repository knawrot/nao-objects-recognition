from naoqi import ALModule, ALProxy

NAO_IP = "169.254.113.113"
NAO_PORT = 9559

class RedBallDetectionModule(ALModule):
	""" A basic module to test events """
	
	def __init__(self, name):
		ALModule.__init__(self, name)
		self.name = name
		#self.tts = ALProxy("ALTextToSpeech")
		self.memory = ALProxy("ALMemory")
		self.motion = ALProxy("ALMotion")
		self.memory.subscribeToEvent("RedBallDetectedEvent", name, "handleBallDetection")
		
        
	def handleBallDetection(self, key, value, message):
		""" A method that handles detection of the ball. """
		names = ['HeadYaw', 'HeadPitch']
		times = [[0.01], [0.01]] # what is the fastest rate?
		xStep = 0.03
		yStep = 0.022
		moveX = -xStep if value[0]>0 else xStep if value[0]<0 else 0.0 # since robot camera has a mirror view, we need to alternate directions
		moveY = yStep if value[1]>0 else -yStep if value[1]<0 else 0.0
		print moveX, moveY
		self.memory.unsubscribeToEvent("RedBallDetectedEvent", self.name)
		self.motion.angleInterpolation(names, [moveX, moveY], times, False)
		#self.tts.say("Recevied the values! " + str(value[0]) + " " + str(value[1]))
		self.memory.subscribeToEvent("RedBallDetectedEvent", self.name, "handleBallDetection")
		

from naoqi import ALBroker
import time, sys

def stiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
	
def main():
	myBroker = ALBroker("RedBallDetectionBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       NAO_IP,      # parent broker IP
       NAO_PORT)    # parent broker port
	   
	motionProxy = ALProxy("ALMotion")
	stiffnessOn(motionProxy)
	   
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