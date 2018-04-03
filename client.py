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
		server_address = ('192.168.1.57', 10000)
		csock.connect(server_address)

	except socket.error as e:
		print('Connection to %s on port %s failed: %s' % (server_address[0], server_address[1], e.strerror))
		return

	out = dumps(image, protocol=2)
	csock.sendall(out)
	csock.shutdown(1)
	csock.close()



def capture_video(cap1, cap2):
	_, frame1 = cap1.read()
	frame1 = frame1[:,int(frame1.shape[1]/4):int(3*frame1.shape[1]/4),:]
	frame1 = np.stack((frame1, frame1))
	#_, frame2 = cap2.read()
	send_file(frame1)

def capture_images():
	for ii in range(10): 
		img1 = cv2.imread('./inputs/strawberry3.jpg')
		img2 = cv2.imread('./inputs/strawberry3.jpg')
		img = np.stack((img1, img2))
		send_file(img)

if __name__ == '__main__':
	#capture_video()
	capture_images()
