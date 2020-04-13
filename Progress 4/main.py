# import the necessary packages
from collections import deque
from imutils.video import VideoStream
from pyimagesearch.shapedetector import ShapeDetector
import numpy as np
import argparse
import cv2
import imutils
import time


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
lower = {'blue': (110, 100, 100), 'red': (-10, 100, 100), 'green': (40, 70, 70),
                 'yellow': (20, 100, 117)}  # assign new item lower['blue'] = (93, 10, 0)
upper = {'blue': (130, 255, 255), 'red': (10, 255, 255), 'green': (70, 255, 255),  'yellow': (40, 255, 255)}

pts = deque(maxlen=args["buffer"])
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)

# make a call for ShapeDetector class
sd = ShapeDetector()

# keep looping
while True:
    # grab the current frame
    frame = vs.read()
    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
    	break
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask

    for key, value in upper.items():
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if (x+y+w+h) >400:
                # Do when reach the minimum contours length
                shape = sd.detect(c)
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.putText(frame, key, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
                cv2.drawContours(frame, [c], -1, (0, 0, 0), 2)

                cv2.putText(frame, shape, (x + 15, y + 15), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 0), 2)
                #cv2.circle(frame, (int(x), int(y)), int(radius),
                #           (0, 255, 255), 2)
                #cv2.circle(frame, center, 5, (0, 0, 255), -1)
        # update the points queue
        #pts.appendleft(center)

    # loop over the set of tracked points
    for i in range(1, len(pts)):
    	# if either of the tracked points are None, ignore
    	# them
    	if pts[i - 1] is None or pts[i] is None:
    		continue
    	# otherwise, compute the thickness of the line and
    	# draw the connecting lines
    	thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
    	cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
    	break
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()
# otherwise, release the camera
else:
    vs.release()
# close all windows
cv2.destroyAllWindows()