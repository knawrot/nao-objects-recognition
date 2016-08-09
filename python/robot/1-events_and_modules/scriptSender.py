from naoqi import ALProxy

host = "169.254.113.113"
port = 9559
		
memory = ALProxy("ALMemory", host, port)
memory.raiseEvent("BasicEvent", 19)