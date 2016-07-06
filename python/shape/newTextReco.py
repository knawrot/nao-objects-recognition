import cv2
import numpy as np

def autoCanny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
 
	# return the edged image
	return edged

vc = cv2.VideoCapture(0)
ret, image = vc.read()

while ret:
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale
	edged = autoCanny(gray)
	edged2 = edged.copy()
	#kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(2,2))
	#dilated = cv2.dilate(edged,kernel,iterations = 3)
	#kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
	#morpho = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
	#_,thresh = cv2.threshold(morpho, 0, 255, cv2.THRESH_OTSU)
	contours,_ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours,_ = cv2.findContours(edged2, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
	
	#if len(contours) > 100:
	#	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
	#	dilated = cv2.dilate(thresh,kernel,iterations = 3)
	#	cv2.rectangle(image,(0,0),(640,480),(255,0,255),2)
		#inrange
		#boundingRect
		#for contour in contours:
			# get rectangle bounding contour
			#[x,y,w,h] = cv2.boundingRect(contour)
			# draw rectangle around contour on original image
			#cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)
		
		
	img1 = cv2.cvtColor(edged,cv2.COLOR_GRAY2BGR)
	img2 = cv2.cvtColor(edged2,cv2.COLOR_GRAY2BGR)
	both = np.hstack((img1,img2))
	cv2.imshow("contoured", both)
	key = cv2.waitKey(25)
	if key == ord('a'):
		break
	
	ret, image = vc.read()

cv2.destroyAllWindows()