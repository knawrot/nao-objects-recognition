from naoqi import ALModule, ALProxy

NAO_IP = "127.0.0.1"
NAO_PORT = 9559

class PersonalModule(ALModule):
	""" A simple module that should test basic configuration """
	
	def __init__(self, name):
		ALModule.__init__(self, name)
		self.tts = ALProxy("ALTextToSpeech")
		
        
	def complimentMe():
		""" Just to ensure on how cool I am. """
		self.tts.say("Chris, you did well on importing!")
		

from naoqi import ALBroker
import time, sys
		
def main():
	myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       NAO_IP,      # parent broker IP
       NAO_PORT)    # parent broker port
	   
	global Personal
	Personal = PersonalModule("Personal")
	
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