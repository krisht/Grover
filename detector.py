import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import shutil


def find_biggest_contour(image):
	# Copy to prevent modification
	image = image.copy()
	_, contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


	centers = []
	for ii in range(len(contours)):
		moments = cv2.moments(contours[ii])
		centers.append((int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00'])))

	mask = np.zeros(image.shape, np.uint8)
	cv2.drawContours(mask, contours, -1, 255, -1)
	return contours, mask, centers

if __name__ == '__main__':

	files = [os.path.join('./inputs', file) for file in os.listdir('./inputs') if file.endswith('.jpeg') or file.endswith('.jpg')]

	if os.path.exists("./outputs"):
		shutil.rmtree('./outputs')
	os.makedirs("./outputs")

	for fname in files:
		# Convert image to RGB
		image = cv2.imread(fname)
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		# Blur image slightly
		image_blur = cv2.GaussianBlur(image, (7, 7), 0)
		image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)
		# 0-10 hue
		min_red = np.array([0, 100, 80])
		max_red = np.array([10, 256, 256])
		image_red1 = cv2.inRange(image_blur_hsv, min_red, max_red)
		# 170-180 hue
		min_red2 = np.array([170, 100, 80])
		max_red2 = np.array([180, 256, 256])
		image_red2 = cv2.inRange(image_blur_hsv, min_red2, max_red2)
		image_red = image_red1 + image_red2
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
		image_red_closed = cv2.morphologyEx(image_red, cv2.MORPH_CLOSE, kernel)
		image_red_closed_then_opened = cv2.morphologyEx(image_red_closed, cv2.MORPH_OPEN, kernel)

		contours, red_mask, centers = find_biggest_contour(image_red_closed_then_opened)

		image_with_com = image.copy()
		for center in centers:
			cv2.circle(image_with_com, tuple(center), 10, (255, 255, 0), -1)
		plt.imsave("./outputs/" + os.path.basename(fname).split('.')[0] + "_com.png", image_with_com)

		image_with_ellipse = image.copy()

		for contour in contours:
			ellipse = cv2.fitEllipse(contour)
			cv2.ellipse(image_with_ellipse, ellipse, (255, 255, 0), 5)
		plt.imsave("./outputs/" + os.path.basename(fname).split('.')[0] + "_ellipse.png", image_with_ellipse)
