import sys
import numpy as np
import cv2
import SeeBerries

REMAP_INTERPOLATION = cv2.INTER_LINEAR

DEPTH_VISUALIZATION_SCALE = 1024

if len(sys.argv) != 2:
    print("Syntax: {0} CALIBRATION_FILE".format(sys.argv[0]))
    sys.exit(1)

calibration = np.load(sys.argv[1], allow_pickle=False)
imageSize = tuple(calibration["imageSize"])
leftMapX = calibration["leftMapX"]
leftMapY = calibration["leftMapY"]
leftROI = tuple(calibration["leftROI"])
rightMapX = calibration["rightMapX"]
rightMapY = calibration["rightMapY"]
rightROI = tuple(calibration["rightROI"])

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

CHESSBOARD_SIZE = (5, 9)

# TODO: Use more stable identifiers
left = cv2.VideoCapture(1)
right = cv2.VideoCapture(0)

# Increase the resolution
left.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
left.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
right.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
right.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

# Use MJPEG to avoid overloading the USB 2.0 bus at this resolution
left.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
right.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

# The distortion in the left and right edges prevents a good calibration, so
# discard the edges
CROP_WIDTH = 960
def cropHorizontal(image):
    return image[:,
            int((CAMERA_WIDTH-CROP_WIDTH)/2):
            int(CROP_WIDTH+(CAMERA_WIDTH-CROP_WIDTH)/2)]

# TODO: Why these values in particular?
# TODO: Try applying brightness/contrast/gamma adjustments to the images
#stereoMatcher = cv2.StereoSGBM_create()
#stereoMatcher.setMinDisparity(4)
#stereoMatcher.setNumDisparities(128)
#stereoMatcher.setBlockSize(21)
#stereoMatcher.setROI1(leftROI)
#stereoMatcher.setROI2(rightROI)
#stereoMatcher.setSpeckleRange(16)
#stereoMatcher.setSpeckleWindowSize(45)

# Grab both frames first, then retrieve to minimize latency between cameras
while True:
	if not left.grab() or not right.grab():
		print("No more frames")
	#	break

	_, rightFrame = right.retrieve()
	rightFrame = cropHorizontal(rightFrame)
	rightHeight, rightWidth = rightFrame.shape[:2]

	if (rightWidth, rightHeight) != imageSize:
		print("Right camera has different size than the calibration data")
	#	break

	fixedRight = cv2.remap(rightFrame, rightMapX, rightMapY, REMAP_INTERPOLATION)

	#cv2.imshow('right', fixedRight)
	#cv2.waitKey(0)
	#if cv2.waitKey(1) & 0xFF == ord('q'):
	#	break

	ovalImg, numBerries, centers = SeeBerries.detect_berries(fixedRight, 'blah')
	cv2.imshow('oval', ovalImg)
	print(centers)
	cv2.waitKey(0)

left.release()
right.release()
cv2.destroyAllWindows()
