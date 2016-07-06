import cv2

def nothing(x):
    pass

vc = cv2.VideoCapture(0)

# Create a black image, a window
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('H_min','image',0,180,nothing)
cv2.createTrackbar('H_max','image',0,180,nothing)
cv2.createTrackbar('S_min','image',0,255,nothing)
cv2.createTrackbar('S_max','image',0,255,nothing)
cv2.createTrackbar('V_min','image',0,255,nothing)
cv2.createTrackbar('V_max','image',0,255,nothing)

# create switch for ON/OFF functionality
#switch = '0 : OFF \n1 : ON'
#cv2.createTrackbar(switch, 'image',0,1,nothing)
ret,frame = vc.read()

while ret:
    # get current positions of four trackbars
	h_min = cv2.getTrackbarPos('H_min','image')
	h_max = cv2.getTrackbarPos('H_max','image')
	s_min = cv2.getTrackbarPos('S_min','image')
	s_max = cv2.getTrackbarPos('S_max','image')
	v_min = cv2.getTrackbarPos('V_min','image')
	v_max = cv2.getTrackbarPos('V_max','image')
	
	hsv_w = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	mask1 = cv2.inRange(hsv_w, (0,0,0), (h_min,s_min,v_min))
	mask2 = cv2.inRange(hsv_w, (h_max,s_max,v_max), (180,255,255))
	mask = mask1 | mask2

	ret,frame = vc.read()
	cv2.imshow('image', mask)
	k = cv2.waitKey(25)
	if k == ord('a'):
		break

cv2.destroyAllWindows()