import cv2
import numpy as np

MIN_MATCH_COUNT = 1
FLANN_INDEX_KDTREE = 0

def drawMatches(img1, kp1, img2, kp2, matches):
	if len(matches) > MIN_MATCH_COUNT:
		for mat in matches:
	
			# Get the matching keypoints for each of the images
			#img1_idx = mat.queryIdx
			img2_idx = mat.trainIdx
	
			# x - columns
			# y - rows
			(x1,y1) = kp2[img2_idx].pt
			#(x2,y2) = kp2[img2_idx].pt
	
			# Draw a small circle at both co-ordinates
			# radius 4
			# colour blue
			# thickness = 1
			cv2.circle(img2, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
			#cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)
	
			# Draw a line in between the two points
			# thickness = 1
			# colour blue
			#cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)


    # Also return the image if you'd like a copy
	return img2



img = cv2.imread('sample1.jpg',0)
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # grayscale
# Create ORB detector with 1000 keypoints with a scaling pyramid factor
# of 1.2
cv2.imshow("contoured", img)
key = cv2.waitKey(0)
orb = cv2.ORB(1000, 1.2)

# Detect keypoints of original image
(kp1,des1) = orb.detectAndCompute(img, None)

vc = cv2.VideoCapture(0)

ret, image = vc.read()
###################

#########
while ret:
	#gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale
	# Detect keypoints of rotated image
	(kp2,des2) = orb.detectAndCompute(image, None)
	
	# Create matcher
	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
	
	# Do matching
	matches = bf.match(des1,des2)
	print matches, des1
	
	# Sort the matches based on distance.  Least distance
	# is better
	matches = sorted(matches, key=lambda val: val.distance)
	
	# Show only the top 10 matches - also save a copy for use later
	out = drawMatches(img, kp1, image, kp2, matches)
	
	cv2.imshow("contoured", out)
	key = cv2.waitKey(25)
	if key == ord('a'):
		break
	
	ret, image = vc.read()

cv2.destroyAllWindows()