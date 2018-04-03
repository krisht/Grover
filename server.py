import socket
import time
import numpy as np
from matplotlib import pyplot as plt
import cv2
import SeeBerries
from pickle import loads, dumps


def startServer():
	ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('192.168.1.57', 10000)
	ssock.bind(server_address)

	ssock.listen(5)
	print("Listening on %s:%s" % server_address)
	while True: 
		conn, c_address = ssock.accept()
		print("Received request from %s:%s" % c_address)
		data = b''
		while True:
			chunk = conn.recv(4096)
			if not chunk:
				break
			data += chunk
		conn.close()
		t = time.time()
		img = loads(data, encoding='bytes')
		img1 = SeeBerries.detect_berries(img[0], 'frame1_%s.png' % t)
		img2 = SeeBerries.detect_berries(img[1],' frame2_%s.png' % t)
		plt.imsave('./received/frame1_%s.png' % t, img1)
		plt.imsave('./received/frame2_%s.png' % t, img2)
		#SeeBerries.stereo_vision(img1, img2, './received/depthmap_%s' % t)

if __name__ == '__main__':
	startServer()