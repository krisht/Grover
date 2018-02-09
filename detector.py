import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import shutil
import time


class SeeBerries: 
    def __init__():
        pass

    def overlay_mask(mask, image):
        rgb_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        img = cv2.addWeighted(rgb_mask, 0.5, image, 0.5, 0)
        return img

    def find_biggest_contour(image):
        # Copy to prevent modification
        image = image.copy()
        contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        centers = []
        for ii in range(len(contours)):
            moments = cv2.moments(contours[ii])
            centers.append((int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00'])))

        mask = np.zeros(image.shape, np.uint8)
        cv2.drawContours(mask, contours, -1, 255, -1)
        return contours, mask, centers



if __name__ == '__main__':
    files = [os.path.join('./inputs', f) for f in os.listdir('./inputs') if f.endswith('.jpeg') or f.endswith('.jpg')]

    if os.path.exists("./outputs"):
        shutil.rmtree('./outputs')
    os.makedirs("./outputs")

    if os.path.exists("./outputs/bs_outputs"):
        shutil.rmtree('./outputs/bs_outputs')
    os.makedirs("./outputs/bs_outputs")

    if os.path.exists("./outputs/true_outputs"):
        shutil.rmtree('./outputs/true_outputs')
    os.makedirs("./outputs/true_outputs")
    
    print("here")

    for f in files:
	start = time.time()
        # Convert image to RGB from BGR
        image = cv2.imread(f)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Blur image slightly

        image_blur = cv2.GaussianBlur(image, (7, 7), 0)
        image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)

        # 0-10 hue
        min_red = np.array([0, 100, 80])
        max_red = np.array([10, 256, 256])
        image_red1 = cv2.inRange(image_blur_hsv, min_red, max_red)
        #plt.imsave("./outputs/bs_outputs/" + os.path.basename(f).split(".")[0] + "_a_1.png", image_red1, cmap='gray')

        # 170-180 hue
        min_red2 = np.array([170, 100, 80])
        max_red2 = np.array([175, 256, 256])
        image_red2 = cv2.inRange(image_blur_hsv, min_red2, max_red2)
        #plt.imsave("./outputs/bs_outputs/" + os.path.basename(f).split(".")[0] + "_a_2.png", image_red2, cmap='gray')
        image_red = image_red1 + image_red2
        #plt.imsave("./outputs/bs_outputs/" + os.path.basename(f).split(".")[0] + "_b.png", image_red, cmap='gray')
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        image_red_closed = cv2.morphologyEx(image_red, cv2.MORPH_CLOSE, kernel)
        image_red_closed_then_opened = cv2.morphologyEx(image_red_closed, cv2.MORPH_OPEN, kernel)
        #plt.imsave("./outputs/bs_outputs/" + os.path.basename(f).split(".")[0] + "_c.png", image_red_closed, cmap='gray')
        #plt.imsave("./outputs/bs_outputs/" + os.path.basename(f).split(".")[0] + "_d.png", image_red_closed_then_opened, cmap='gray')


        contours, red_mask, centers = find_biggest_contour(image_red_closed_then_opened)

        #plt.imsave("./outputs/bs_outputs/" + os.path.basename(f).split(".")[0] + "_e.png", red_mask, cmap='gray')
        image_overlayed_mask = overlay_mask(red_mask, image)
        #plt.imsave("./outputs/bs_outputs/" + os.path.basename(f).split(".")[0] + "_f.png", image_overlayed_mask)

        image_with_com = image.copy()
        for center in centers:
            cv2.circle(image_with_com, tuple(center), 10, (255, 255, 0), -1)
        #plt.imsave("./outputs/bs_outputs/" + os.path.basename(f).split('.')[0] + "_g.png", image_with_com)

        image_with_ellipse = image.copy()

        for contour in contours:
            ellipse = cv2.fitEllipse(contour)
            cv2.ellipse(image_with_ellipse, ellipse, (255, 255, 0), 10)
        plt.imsave("./outputs/true_outputs/" + os.path.basename(f).split('.')[0] + "_h.png", image_with_ellipse)
	print(time.time() - start)