import cv2
import numpy as np
import argparse

def isWindowEmpty(r):
	(_,_,w,h) = r
	return (w <= 0) or (h <= 0)
	
def setWindowAsFrameSize(frame):
	width = np.size(frame, 1)
	height = np.size(frame, 0)
	window = (0,0,width,height)
	return window

def calculateWindowCenterBox(frame):
	width = np.size(frame, 1)
	height = np.size(frame, 0)
	centerPoint = (width/2, height/2)
	scale = 0.15
	vector = (width * scale, height * scale)
	rectangle = [(centerPoint[0] - int(vector[0]), centerPoint[1] - int(vector[1])), (centerPoint[0] + int(vector[0]), centerPoint[1] + int(vector[1]))]
	print rectangle
	return rectangle
	
	
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help = "path to the (optional) video file")
args = vars(ap.parse_args())

if not args.get("video", False):
	vc = cv2.VideoCapture(0)
else:
	vc = cv2.VideoCapture(args["video"])
		

ret, frame = vc.read()

#Calc Hist
#hist = cv2.calcHist([hsv],[0],acmask,[180],[0,180])

#normalise Hist
#normalize = cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)

#termination criteria
term = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

# Initial position of window
track = (0,0,0,0)
frameCenterBox = calculateWindowCenterBox(frame)




while ret:
	# read frames
	ret,frame = vc.read()
	if isWindowEmpty(track):
		track = setWindowAsFrameSize(frame)
	else:
		if frameCenterBox[0] > retn[0] < frameCenterBox[1]:
			print retn[0]
			pts = cv2.cv.BoxPoints(retn)
			pts = np.int0(pts)
			cv2.polylines(frame,[pts],True,255,2)		
		
	cv2.rectangle(frame,frameCenterBox[0],frameCenterBox[1],255,3)
	cv2.imshow('a',frame)		
	# convert to HSV
	hsv_w = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	acmask = cv2.inRange(hsv_w, (1,178,65), (7,232,138))
	hist = cv2.calcHist([hsv_w],[0,1],acmask,[180,255],[0,180,0,255])
	dst = cv2.calcBackProject([hsv_w],[0,1],hist,[0,180,0,255],1)
	
	retn, track = cv2.CamShift(dst, track, term)
	
	key = cv2.waitKey(25)
	if key == ord('a'):
		break

cv2.destroyAllWindows()