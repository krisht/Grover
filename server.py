import socket
import sys


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('192.168.0.106', 10000)

print('Starting up on %s port %s' % server_address)
sock.bind(server_address)



sock.listen(1)

while True:
	print("Waiting for a  connection")
	connection, client_address = sock.accept()

	try:
		print("Connection from", client_address)

		while True: 
			data = connection.recv(16)
			print("Received '%s'" % data)
			if data:
				print('sending data back to the client')
				connection.sendall(data)
			else:
				print('no more data from', client_address)
				break

	finally: 
		connection.close()
            
