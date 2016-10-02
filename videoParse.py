import numpy as np
import cv2
import argparse
import sys
import time

def main():
	args_parser = argparse.ArgumentParser()
	args_parser.add_argument("-v", "--video", help = "path  to the video file")
	args = vars(args_parser.parse_args())

	if not args.get("video", False):
		print("Video argument is required")
		sys.exit(1)
	else:
		camera = cv2.VideoCapture(args["video"])

	cv2.namedWindow("frame")

	termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT , 10, 1)
	roiBox = None

	while True:
		(grabbed, frame) = camera.read()
		time.sleep(.1)

		if not grabbed:
			break

		if roiBox is not None:
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			backProj = cv2.calcBackProject([hsv], [0], roiHist, [0, 180], 1)

			(r, roiBox) = cv2.CamShift(backProj, roiBox, termination)
			pts = np.int0(cv2.boxPoints(r))
			cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

		cv2.imshow("frame", frame)
		cv2.waitKey(1)
		#Create initial rectangle frame
		if roiBox is None:
			print("TEST")
			orig = frame.copy()

			tl = [50,50] #TODO: Top Left of rectangle
			br = [100,500] #TODO: Bottom Right of rectangle

			roi = orig[tl[1]:br[1], tl[0]:br[0]]
			roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

			roiHist = cv2.calcHist([roi], [0], None, [16], [0, 180])
			roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
			roiBox = (tl[0], tl[1], br[0], br[1])

	camera.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()