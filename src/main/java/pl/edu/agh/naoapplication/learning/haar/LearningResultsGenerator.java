package pl.edu.agh.naoapplication.learning.haar;

import org.bytedeco.javacpp.opencv_core.IplImage;
import static org.bytedeco.javacpp.opencv_core.*;
import static org.bytedeco.javacpp.opencv_highgui.*;
import static org.bytedeco.javacpp.opencv_objdetect.*;
import static org.bytedeco.javacpp.opencv_imgcodecs.cvLoadImage;
import static org.bytedeco.javacpp.opencv_imgproc.*;


public class LearningResultsGenerator {
	public static final String XML_FILE = "data/cascade.xml";

	public static void main(String[] args){
		IplImage img = cvLoadImage("resourcers/images/o_bb1e271b16459137-62.jpg");		
		detect(img);		
	}	

	public static void detect(IplImage src){
		CvHaarClassifierCascade cascade = new CvHaarClassifierCascade(cvLoad(XML_FILE));
		CvMemStorage storage = CvMemStorage.create();
		CvSeq sign = cvHaarDetectObjects(
				src,
				cascade,
				storage,
				1.5,
				3,
				CV_HAAR_DO_CANNY_PRUNING);

		cvClearMemStorage(storage);

		int total_Faces = sign.total();		

		for(int i = 0; i < total_Faces; i++){
			CvRect r = new CvRect(cvGetSeqElem(sign, i));
			cvRectangle (
					src,
					cvPoint(r.x(), r.y()),
					cvPoint(r.width() + r.x(), r.height() + r.y()),
					CvScalar.RED,
					2,
					CV_AA,
					0);

		}

		cvShowImage("Result", src);
		cvWaitKey(0);

	}			
}