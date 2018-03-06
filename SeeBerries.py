import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
import shutil
import sys
import time


def overlay_mask(mask, image):
    rgb_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    img = cv2.addWeighted(rgb_mask, 0.5, image, 0.5, 0)
    return img

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

def detect_berries(image, name):
    #image = cv2.imread(f)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Blur image slightly

    image_blur = cv2.GaussianBlur(image, (7, 7), 0)
    image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)

    # 0-10 hue
    min_red = np.array([0, 100, 80])
    max_red = np.array([10, 256, 256])
    image_red1 = cv2.inRange(image_blur_hsv, min_red, max_red)
    plt.imsave("/home/krishna/Dropbox/Grover/outputs/" + os.path.basename(name).split(".")[0] + "_image_red1.png", image_red1, cmap='gray')

    # 170-180 hue
    min_red2 = np.array([170, 100, 80])
    max_red2 = np.array([175, 256, 256])
    image_red2 = cv2.inRange(image_blur_hsv, min_red2, max_red2)
    plt.imsave("/home/krishna/Dropbox/Grover/outputs/" + os.path.basename(name).split(".")[0] + "_image_red2.png", image_red2, cmap='gray')
    image_red = image_red1 + image_red2
    plt.imsave("/home/krishna/Dropbox/Grover/outputs/" + os.path.basename(name).split(".")[0] + "_image_red.png", image_red, cmap='gray')
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    image_red_closed = cv2.morphologyEx(image_red, cv2.MORPH_CLOSE, kernel)
    image_red_closed_then_opened = cv2.morphologyEx(image_red_closed, cv2.MORPH_OPEN, kernel)
    plt.imsave("/home/krishna/Dropbox/Grover/outputs/" + os.path.basename(name).split(".")[0] +  "_image_red_closed.png", image_red_closed, cmap='gray')
    plt.imsave("/home/krishna/Dropbox/Grover/outputs/" + os.path.basename(name).split(".")[0] + "_image_red_closed_then_opened.png", image_red_closed_then_opened, cmap='gray')


    contours, red_mask, centers = find_biggest_contour(image_red_closed_then_opened)

    plt.imsave("/home/krishna/Dropbox/Grover/outputs/" + os.path.basename(name).split(".")[0] +  "_red_mask.png", red_mask, cmap='gray')
    image_overlayed_mask = overlay_mask(red_mask, image)
    plt.imsave("/home/krishna/Dropbox/Grover/outputs/" + os.path.basename(name).split(".")[0] + "_image_overlayed_mask.png", image_overlayed_mask)

    image_with_com = image.copy()
    for center in centers:
        cv2.circle(image_with_com, tuple(center), 10, (255, 255, 0), -1)
    plt.imsave("/home/krishna/Dropbox/Grover/outputs/" + os.path.basename(name).split(".")[0] + "_image_with_com.png", image_with_com)

    image_with_ellipse = image.copy()

    for contour in contours:
        ellipse = cv2.fitEllipse(contour)
        cv2.ellipse(image_with_ellipse, ellipse, (255, 255, 0), 10)
    return image_with_ellipse
    #plt.imsave("./outputs/true_outputs/" + os.path.basename(f).split('.')[0] + "_h.png", image_with_ellipse)

def stereo_vision(img1, img2, title):
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    stereo_vision = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity=stereo_vision.compute(img1, img2)
    plt.imsave(title, disparity)


if __name__=='__main__':
    files = [os.path.join(sys.argv[1], f) for f in os.listdir(sys.argv[1]) if f.endswith('.jpeg') or f.endswith('.jpg')]
    for f in files:
        img = cv2.imread(f, cv2.COLOR_BGR2RGB)
        plt.imsave('/home/krishna/Dropbox/Grover/outputs/' + f.replace('./', '').replace('jpg', 'png'), detect_berries(img, f))
