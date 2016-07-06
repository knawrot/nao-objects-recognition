import cv2

vc = cv2.VideoCapture(0)

ret, image = vc.read()

while ret:	
	cv2.imshow("Stream", image)
	key = cv2.waitKey(25)
	if key == ord('a'):
		break
	if key == ord('s'):
		cv2.imwrite('image.jpg', image)
	
	ret, image = vc.read()

cv2.destroyAllWindows()