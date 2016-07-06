import cv2
import numpy as np
from collections import Counter

MIN_RATIO_OF_SCREEN = 0.33	# ratio for telephone screen


def autoCanny(image, sigma=0.33):
	v = np.median(image)

	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)

	return edged
	
def sortContoursByChildrenAndArea(contours, hierarchy):
	numOfChildren = [i[-1] for i in hierarchy]
	sortedNumOfChildren = Counter(numOfChildren)
	del sortedNumOfChildren[-1]
	
	screenCandidates = []
	candidates = []
	for f in sortedNumOfChildren.most_common(10):
		candidates.append(contours[f[0]])
		
	for c in candidates:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		_,_,w,h = cv2.boundingRect(c)
		aspectRatio = float(w)/h
		if len(approx) == 4 and aspectRatio > MIN_RATIO_OF_SCREEN:
			screenCandidates.append(c)
		
	return max(screenCandidates, key=cv2.contourArea) if screenCandidates else np.array([])

	
	
vc = cv2.VideoCapture(0)
ret, image = vc.read()

#TODO: make edges of display more visible (not overwhelmed by objects on display)

while ret:
	_,img = vc.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray = cv2.bilateralFilter(gray, 11, 17, 17)
	edged = autoCanny(gray)
	#gray = cv2.bilateralFilter(gray, 11, 17, 17)
	#_,th1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
	#th2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 1)
	#kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(2,2))
	#opening = cv2.morphologyEx(edged, cv2.MORPH_OPEN, kernel)
	#dilated = cv2.dilate(edged, kernel, iterations = 2)
	contours,hierarchy = cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	contoursWithMostChildren = sortContoursByChildrenAndArea(contours,hierarchy[0])
	if contoursWithMostChildren != None:
		cv2.drawContours(img,[contoursWithMostChildren],-1,(0,0,255),2) 
		
	edged = cv2.cvtColor(edged,cv2.COLOR_GRAY2BGR)
	#th2 = cv2.cvtColor(th2,cv2.COLOR_GRAY2BGR)
	both = np.hstack((img,edged))
	cv2.imshow("Detection of text", both)
	key = cv2.waitKey(25)
	if key == ord('a'):
		break
	
	ret, image = vc.read()

cv2.destroyAllWindows()