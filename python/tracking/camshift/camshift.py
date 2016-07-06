#!/usr/bin/env python

import cv2

def is_rect_nonzero(r):
    (_,_,w,h) = r
    return (w > 0) and (h > 0)

class CamShiftDemo:

    def __init__(self):
        self.capture = cv2.VideoCapture()
        cv2.namedWindow( "CamShiftDemo", 1 )
        cv2.namedWindow("Backprojection", 1)
        cv2.namedWindow( "Histogram", 1 )
        
        cv2.setMouseCallback( "CamShiftDemo", self.on_mouse) #Instantiate call back for mouse event

        self.drag_start = None      # Set to (x,y) when mouse starts drag
        self.track_window = None    # Set to rect when the mouse drag finishes


    def hue_histogram_as_image(self, hist):
        """ Returns a nice representation of a hue histogram """

        histimg_hsv = cv2.createImage( (320,200), 8, 3)
        
        mybins = cv2.cloneMatND(hist.bins) #Contain all values
        cv2.log(mybins, mybins) #Calculate logarithm of all values (so there are all above 0)
        
        (_, hi, _, _) = cv2.MinMaxLoc(mybins)
        cv2.convertScale(mybins, mybins, 255. / hi) #Rescale all element to get the highest at 255

        w,h = cv2.getSize(histimg_hsv)
        hdims = cv2.getDims(mybins)[0]
        for x in range(w):
            xh = (180 * x) / (w - 1)  # hue sweeps from 0-180 across the image
            val = int(mybins[int(hdims * x / w)] * h / 255)
            cv2.rectangle( histimg_hsv, (x, 0), (x, h-val), (xh,255,64), -1)
            cv2.rectangle( histimg_hsv, (x, h-val), (x, h), (xh,255,255), -1)

        histimg = cv2.createImage( (320,200), 8, 3) #Convert image from hsv to RGB
        cv2.cvtColor(histimg_hsv, histimg, cv2.CV_HSV2BGR)
        return histimg

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.CV_EVENT_LBUTTONDOWN: #when start pressing
            self.drag_start = (x, y)
        if event == cv2.CV_EVENT_LBUTTONUP: #when release left click
            self.drag_start = None
            self.track_window = self.selection
        if self.drag_start: #in both cases compute coordinates
            xmin = min(x, self.drag_start[0])
            ymin = min(y, self.drag_start[1])
            xmax = max(x, self.drag_start[0])
            ymax = max(y, self.drag_start[1])
            self.selection = (xmin, ymin, xmax - xmin, ymax - ymin)


    def run(self):
        hist = cv2.createHist([180], cv2.CV_HIST_ARRAY, [(0,180)], 1 )
        backproject_mode = True
        
        while True:
            frame = cv2.QueryFrame( self.capture )

            # Convert to HSV and keep the hue
            hsv = cv2.createImage(cv2.GetSize(frame), 8, 3)
            cv2.cvtColor(frame, hsv, cv2.CV_BGR2HSV)
            self.hue = cv2.createImage(cv2.GetSize(frame), 8, 1)
            cv2.split(hsv, self.hue, None, None, None)

            # Compute back projection
            backproject = cv2.createImage(cv2.GetSize(frame), 8, 1)
            cv2.calcArrBackProject( [self.hue], backproject, hist )

            # Run the cam-shift (if the a window is set and != 0)
            if self.track_window and is_rect_nonzero(self.track_window):
                crit = ( cv2.CV_TERMCRIT_EPS | cv2.CV_TERMCRIT_ITER, 10, 1)
                (iters, (area, value, rect), track_box) = cv2.camShift(backproject, self.track_window, crit) #Call the camshift !!
                self.track_window = rect #Put the current rectangle as the tracked area


            # If mouse is pressed, highlight the current selected rectangle and recompute histogram
            if self.drag_start and is_rect_nonzero(self.selection):
                sub = cv2.getSubRect(frame, self.selection) #Get specified area
                
                #Make the effect of background shadow when selecting a window
                save = cv2.cloneMat(sub)
                cv2.convertScale(frame, frame, 0.5)
                cv2.copy(save, sub)
                
                #Draw temporary rectangle
                x,y,w,h = self.selection
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255,255,255))

                #Take the same area but in hue image to calculate histogram
                sel = cv2.getSubRect(self.hue, self.selection ) 
                cv2.calcArrHist( [sel], hist, 0)
                
                #Used to rescale the histogram with the max value (to draw it later on)
                (_, max_val, _, _) = cv2.getMinMaxHistValue( hist)
                if max_val != 0:
                    cv2.convertScale(hist.bins, hist.bins, 255. / max_val) 
                    
            elif self.track_window and is_rect_nonzero(self.track_window): #If window set draw an elipseBox
                cv2.ellipseBox( frame, track_box, cv2.CV_RGB(255,0,0), 3, cv2.CV_AA, 0 )


            cv2.showImage( "CamShiftDemo", frame )
            cv2.showImage( "Backprojection", backproject)
            cv2.showImage( "Histogram", self.hue_histogram_as_image(hist))

            c = cv2.waitKey(7) % 0x100
            if c == 27:
                break


if __name__=="__main__":
    demo = CamShiftDemo()
    demo.run()
