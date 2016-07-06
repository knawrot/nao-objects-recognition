package pl.edu.agh.naoapplication.learning.svm;

import static org.bytedeco.javacpp.opencv_imgcodecs.cvLoadImage;

import java.util.ArrayList;
import java.util.List;

import static org.bytedeco.javacpp.opencv_core.*;

import org.bytedeco.javacpp.opencv_objdetect.HOGDescriptor;

import static org.bytedeco.javacpp.opencv_imgproc.*;

public class HOGClassifier {
	
	public static void main(String[] args) {
//		float[] featureVector = new float[10];
//		IplImage img = cvLoadImage("resourcers/images/64x64.jpg");
//		Size winSize = new Size(64,64),
//			blockSize = new Size(16,16),
//			blockStride = new Size(8,8),
//			cellSize = new Size(8,8),
//			trainPadding = new Size(0,0);
//		int numOfBins = 9;
//		HOGDescriptor hogDesc = new HOGDescriptor(winSize, blockSize, blockStride, cellSize, numOfBins);
//		CvRect rect = new CvRect();
//		//hogDesc.compute(img, rect, 5, 6, 7);
//		//cvCvtColor(img, img, CV_BGR2GRAY);
//		hogDesc.compute(new Mat(img), featureVector, blockStride, trainPadding, new PointVector());
//		System.out.println(featureVector);
//		hogDesc.close();
		//hogDesc.detectMultiScale(img, rect, 0, cvSize(8,8), cvSize(32,32), 1.05);
		RectVector found = new RectVector(); 
		IplImage img = cvLoadImage("resourcers/images/testimage.jpg"); 
		HOGDescriptor hog = new HOGDescriptor(); 
		hog.detectMultiScale(new Mat(img), found, 0.0, new Size(8,8), new Size(32,32), 1.05, 2.0, true); 
		System.out.println(found);
	}

}
