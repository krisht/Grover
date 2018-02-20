import socket
import numpy as np
import cv2
import os
import time
from pickle import loads, dumps



def send_file(image):
	if not isinstance(image, np.ndarray):
		print("Not a valid numpy image")#smh
		return
	csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


	try:
		server_address = ('127.0.0.1', 10000)
		csock.connect(server_address)

	except socket.error as e:
		print('Connection to %s on port %s failed: %s' % (server_address[0], server_address[1], e.strerror))
		return

	out = dumps(image, protocol=2)
	csock.sendall(out)
	csock.shutdown(1)
	csock.close()



def capture_video():
	cap1 = cv2.VideoCapture(0)
	cap2 = cv2.VideoCapture(1)
	cap1.set(3, 80)
	cap1.set(4, 60)
	cap2.set(3, 80)
	cap2.set(4, 60)
	
	while True: 
		_, frame1 = cap1.read()
		_, frame2 = cap2.read()
		frame = np.stack((frame1, frame2))
		# Any color conversion operations here
		send_file(frame)

def capture_images():
	for ii in range(10): 
		img1 = cv2.imread('./inputs/strawberry3.jpg')
		img2 = cv2.imread('./inputs/strawberry3.jpg')
		img = np.stack((img1, img2))
		send_file(img)

if __name__ == '__main__':
	#capture_video()
	capture_images()
