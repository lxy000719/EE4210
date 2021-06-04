import socket
import multiprocessing
import os
import sys
import webbrowser
import re

def connection(ip, port):
	# create udp client socket
	udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	request = 'GET / HTTP/1.1\r\nHost: {}:{}\r\nConnection: keep-alive\r\n\n'.format(ip, port)
	# send request to server
	udp_client_socket.sendto(request.encode('utf-8'), (ip, port))
	# receive from server
	recv_file = udp_client_socket.recvfrom(1024)
	data = recv_file[0].decode('utf-8')
	addr = recv_file[1]
	print('Current process id: ', os.getpid())
	print('Received from server:', addr)
	print(data)
	udp_client_socket.close()

def main(ip, port):
	# create multiple concurrent process of request to the server
	for i in range(3):
		p = multiprocessing.Process(target=connection, args=(ip, port,))
		p.start()

if __name__ == '__main__':
    if len(sys.argv) == 3:
    	ip = sys.argv[1]
    	port = int(sys.argv[2])
    	main(ip, port)
    else:
        print('Invalid command, please indicate <ip> <port>')
        print('Example: python3 udpclient.py 127.0.0.1 9999')

