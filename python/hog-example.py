import cv2
 
hog = cv2.HOGDescriptor()
im = cv2.imread('testimage.jpg')
r = ((100, 200), )
h = hog.compute(im, hog.blockStride, hog.cellSize, r)
print h.shape
hog.save("hog.xml")
hog.setSVMDetector(h)
(rects, weights) = hog.detect(im)
print rects
for (x, y) in rects:
	cv2.rectangle(im, (x, y), (x + 10, y + 10), (0, 255, 0), 2)
cv2.imshow("Detections", im)
cv2.waitKey(0)