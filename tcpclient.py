import socket
import multiprocessing
import os
import sys

def connection(ip, port):
	# create tcp client socket
	tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_client_socket.connect((ip, port))
	request = 'GET / HTTP/1.1\r\nHost: {}:{}\r\nConnection: keep-alive\r\n\n'.format(ip, port)
	# send request to tcp server
	tcp_client_socket.send(request.encode('utf-8'))
	# receive from server
	recv_file = tcp_client_socket.recv(1024).decode('utf-8')
	print('Current process id: ', os.getpid())
	print('Received from server:', (ip, port))
	print(recv_file)

	tcp_client_socket.close()


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
        print('Invalid command')
        print('Example: python3 tcpclient.py 127.0.0.1 9999')
