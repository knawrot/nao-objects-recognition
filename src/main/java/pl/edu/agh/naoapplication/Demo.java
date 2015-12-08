package pl.edu.agh.naoapplication;

import static org.bytedeco.javacpp.opencv_core.cvCreateImage;
import static org.bytedeco.javacpp.opencv_core.cvGetSize;
import static org.bytedeco.javacpp.opencv_core.cvInRangeS;
import static org.bytedeco.javacpp.opencv_core.cvScalar;
import static org.bytedeco.javacpp.opencv_imgcodecs.cvLoadImage;
import static org.bytedeco.javacpp.opencv_imgcodecs.cvSaveImage;

import org.bytedeco.javacpp.opencv_core.CvScalar;
import org.bytedeco.javacpp.opencv_core.IplImage;




/**
 * Hello JavaCV!
 *
 */
public class Demo 
{
	static CvScalar min = cvScalar(0, 0, 130, 0);//BGR-A
    static CvScalar max= cvScalar(140, 110, 255, 0);//BGR-A

    public static void main(String[] args) {
        //read image
        IplImage orgImg = cvLoadImage("resourcers/images/colordetectimage.jpg");
        //create binary image of original size
        IplImage imgThreshold = cvCreateImage(cvGetSize(orgImg), 8, 1);
        //apply thresholding
        cvInRangeS(orgImg, min, max, imgThreshold);
        //save
        cvSaveImage("threshold.jpg", imgThreshold); 
    }
}
