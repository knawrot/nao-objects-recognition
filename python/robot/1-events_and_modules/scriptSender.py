from naoqi import ALProxy

host = "127.0.0.1"
port = 9559
		
memory = ALProxy("ALMemory", host, port)
memory.raiseEvent("BasicEvent", 19)