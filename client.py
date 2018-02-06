import socket
import numpy as np
from cStringIO import StringIO
import cv2




def send_file(image):
	if not isinstance(image, np.ndarray):
		print("Not a valid numpy image")
		return
	client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		server_address = ('192.168.1.14', 10000)
		client_sock.connect(server_address)
	except socket.error:
		print('Connection to %s on port %s failed: %s' % (server_address[0], server_address[1], str(socket.error)))
		return

	f = StringIO()

	np.savez_compressed(f, frame=image)

	f.seek(0)
	out = f.read()
	client_sock.sendall(out)
	client_sock.shutdown(1)
	client_sock.close()



def capture_video():
	cap = cv2.VideoCapture(0)
	while True: 
		ret, frame = cap.read()
		# Any color conversion operations here
		send_file(frame)


if __name__ == '__main__':
	for ii in range(10): 
		img = cv2.imread('./inputs/strawberry3.jpg')
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		send_file(img)