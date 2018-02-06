import socket
import numpy as np
from cStringIO import StringIO
import sys
from matplotlib import pyplot as plt
import time



def startServer():

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.0.106', 10000)
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
	    plt.imsave('./received/frame_%s.png' % time.time(), final_image)

def send_file(image):
    if not isinstance(image, np.ndarray):
        print("Not a valid numpy image")
        return
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_address = ('192.168.0.106', 10000)
        client_sock.connect(server_address)
    except socket.error, e:
        print('Connection to %s on port %s failed: %s' % (server_address, port, e))
        return

    f = StringIO()

    np.savez_compressed(f, frame=image)

    f.seek(0)
    out = f.read()
    client_sock.sendall(out)
    client_sock.shutdown(1)
    client_sock.close()


if sys.argv[1] == 'server':
    startServer()
elif sys.argv[1] == 'client': 
	for ii in range(10): 
		img = plt.imread('./inputs/strawberry3.jpg')
		send_file(img)