import socket
import numpy as np
from cStringIO import StringIO
import sys
from matplotlib import pyplot as plt
import time
import cv2

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

def startServer():
	server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('192.168.1.14', 10000)
	server_sock.bind(server_address)

	server_sock.listen(1)
	while True: 
		client_connection, client_address = server_sock.accept()
		#print("Connected to: ", client_address)
		ultimate_buffer=''
		while True:
			receiving_buffer = client_connection.recv(1024)
			if not receiving_buffer:
				break
			ultimate_buffer += receiving_buffer
		final_image = np.load(StringIO(ultimate_buffer))['frame']
		client_connection.close()

		final_image = process_image(final_image)
		plt.imsave('./received/frame_%s.png' % time.time(), final_image)

def send_file(image):
	if not isinstance(image, np.ndarray):
		print("Not a valid numpy image")
		return
	client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		server_address = ('192.168.1.14', 10000)
		client_sock.connect(server_address)
	except socket.error:
		print('Connection to %s on port %s failed: %s' % (server_address[0], server_address[1]))
		return

	f = StringIO()

	np.savez_compressed(f, frame=image)

	f.seek(0)
	out = f.read()
	client_sock.sendall(out)
	client_sock.shutdown(1)
	client_sock.close()

def process_image(image):
	#image = cv2.imread(f)
	#image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
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
	return image_with_ellipse
	#plt.imsave("./outputs/true_outputs/" + os.path.basename(f).split('.')[0] + "_h.png", image_with_ellipse)

def capture_video():
	cap = cv2.VideoCapture(0)
	while True: 
		ret, frame = cap.read()
		# Any color conversion operations here
		send_file(frame)


if sys.argv[1] == 'server':
	startServer()
elif sys.argv[1] == 'client':
	# capture_video()
	for ii in range(10): 
		img = plt.imread('./inputs/strawberry3.jpg')
		send_file(img)