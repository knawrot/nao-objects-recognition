import cv2
import numpy as np

MIN_RATIO_OF_SIMILIAR_OBJECTS = 0.65 	# letters in paragraph are supposed to have similiar height/width ratio
MIN_AREA_OF_SIMILIAR_OBJECTS = 0.5 		# letters in paragraph are supposed to occupy same area (i.e. have roughly equal size)
MIN_CONTOURS_DETECTED = 100


def autoCanny(image, sigma=0.33):
	v = np.median(image)

	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)

	return edged
	
def extractContoursStatistics(contours):
	contourBoundingRectAreas = []
	contourBoundingRectRatios = []
	
	for i in contours:
		_,_,w,h = cv2.boundingRect(i)
		contourBoundingRectAreas.append(w*h)
		contourBoundingRectRatios.append(float(w)/h)
		
	return np.median(contourBoundingRectAreas), np.mean(contourBoundingRectAreas), np.median(contourBoundingRectRatios), np.mean(contourBoundingRectRatios)

	
	
vc = cv2.VideoCapture(0)
ret, image = vc.read()

while ret:
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	edged = autoCanny(gray)
	contours,_ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	if len(contours) > MIN_CONTOURS_DETECTED: # simple condition to prevent constant evaluation of contours when it doesn't make sense
		areaMedian, areaMean, ratioMedian, ratioMean = extractContoursStatistics(contours)
		if ratioMedian/ratioMean >= MIN_RATIO_OF_SIMILIAR_OBJECTS and areaMedian/areaMean >= MIN_AREA_OF_SIMILIAR_OBJECTS:
			print 'Detected lines of text! '
		
		
	contoursImage = cv2.cvtColor(edged,cv2.COLOR_GRAY2BGR)
	both = np.hstack((image,contoursImage))
	cv2.imshow("Detection of text", both)
	key = cv2.waitKey(25)
	if key == ord('a'):
		break
	
	ret, image = vc.read()

cv2.destroyAllWindows()