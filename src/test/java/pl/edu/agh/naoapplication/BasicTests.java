package pl.edu.agh.naoapplication;

import static org.bytedeco.javacpp.opencv_core.cvCreateImage;
import static org.bytedeco.javacpp.opencv_core.cvGetSize;
import static org.bytedeco.javacpp.opencv_core.cvInRangeS;
import static org.bytedeco.javacpp.opencv_core.cvScalar;
import static org.bytedeco.javacpp.opencv_imgcodecs.cvLoadImage;
import static org.bytedeco.javacpp.opencv_imgcodecs.cvSaveImage;

import org.bytedeco.javacpp.opencv_core.CvScalar;
import org.bytedeco.javacpp.opencv_core.IplImage;
import org.junit.Test;



/**
 * Unit test for simple App.
 */
public class BasicTests {
	
	/* Basic test to run after configuring environment */
	@Test
    public void basicConfigurationTest() {
    	CvScalar min = cvScalar(0, 0, 130, 0);//BGR-A
        CvScalar max = cvScalar(140, 110, 255, 0);//BGR-A
        IplImage orgImg = cvLoadImage("resourcers/images/colordetectimage.jpg");
        IplImage imgThreshold = cvCreateImage(cvGetSize(orgImg), 8, 1);
        cvInRangeS(orgImg, min, max, imgThreshold);
        cvSaveImage("threshold.jpg", imgThreshold); 
    }
}
