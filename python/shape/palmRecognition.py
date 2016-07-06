import cv2
import numpy as np
import math

def checkContours(contours):
	contours = sorted(contours, key=cv2.contourArea, reverse=True)
	maxContour = contours[0]
	hull = cv2.convexHull(maxContour)
	if len(contours) > 1 and float(cv2.contourArea(contours[1]))/cv2.contourArea(maxContour) > 0.3:
		return -1, hull
	area = cv2.contourArea(maxContour)
	hull_area = cv2.contourArea(hull)
	solidity = float(area)/hull_area
	if solidity > 0.75:
		return 0, hull
	else:
		return 1, hull


cap = cv2.VideoCapture(0)

while( cap.isOpened() ):
	ret,img = cap.read()
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	thresh1 = cv2.inRange(hsv, (0,16,83), (13,135,200))
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
	eroded = cv2.erode(thresh1, kernel, iterations = 3)
	dilated = cv2.dilate(eroded, kernel, iterations = 3)
	contours,_ = cv2.findContours(dilated.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	if len(contours) > 0:
		status,hull = checkContours(contours)
		if status == 0:
			cv2.putText(img, "Closed hand", (50,100), cv2.FONT_HERSHEY_SIMPLEX, fontScale=3, color=[255,0,0], thickness=5)
		elif status == 1:
			cv2.putText(img, "Opened hand", (50,100), cv2.FONT_HERSHEY_SIMPLEX, fontScale=3, color=[255,0,0], thickness=5)
		cv2.drawContours(img,[hull],0,(0,0,255),2) 
			
	contoursImage = cv2.cvtColor(dilated,cv2.COLOR_GRAY2BGR)
	both = np.hstack((img,contoursImage))
	cv2.imshow("Detection of palm", both)
	key = cv2.waitKey(25)
	if key == ord('a'):
		break