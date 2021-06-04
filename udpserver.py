import socket
import re
import multiprocessing
import os
import sys

def service_client(udp_server_socket, request):

    # receive and deocde the HTTP request
    data = request[0].decode('utf-8')
    addr = request[1]
    print('Current process id: ', os.getpid())
    print('Received requst from client: ', addr)
    print(data)

    # check request http header
    if "GET / HTTP/1.1" in data:
        response = 'HTTP/1.1 200 OK\r\n' +\
          'Content-Type: text/html\r\n' + '\r\n' +\
          '<HTML><HEAD>\r\n' +\
          '<TITLE>200 OK</TITLE>' +\
          '</HEAD><BODY>\r\n' +\
          'EE-4210: Continuous assessment\r\n' +\
          '</BODY></HTML>\r\n'
     # send response to the client
    udp_server_socket.sendto(response.encode('utf-8'), addr)

    udp_server_socket.close()


def main(port):
	# create udp server socket
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_socket.bind(('', port))
    print('Binding on port: ', port)
    print('\n')

    while True:
    	# create multiple process of server for concurrent request
        request = udp_server_socket.recvfrom(1024)
        p = multiprocessing.Process(target=service_client, args=(udp_server_socket,request,))
        p.start()

    udp_server_socket.close()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
        main(port)
    else:
    	print('Invalid command, please indicate port number')
    	print('Example: python3 udpserver.py 9999')




