import socket
import re
import multiprocessing
import os
import sys

def service_client(new_socket, client_addr):
    # receive and deocde the HTTP request
    request = new_socket.recv(1024).decode('utf-8')
    print('Current process id: ', os.getpid())
    print('Received requst from client: ', client_addr)
    print(request)

    # check request data without any input
    if "GET / HTTP/1.1" in request:
        response = 'HTTP/1.1 200 OK\r\n' +\
          'Content-Type: text/html\r\n' + '\r\n' +\
          '<HTML><HEAD>\r\n' +\
          '<TITLE>200 OK</TITLE>' +\
          '</HEAD><BODY>\r\n' +\
          '<form action="" method="get"><input type="text" name="input" value=""><br><br><input type="submit" value="Submit"></form>\r\n' +\
          '</BODY></HTML>\r\n'
        new_socket.send(response.encode('utf-8'))

    # check request data with an input
    elif "GET /?input=" in request: 
        data = re.search('/?input=(.*) HTTP/1.1',request).group(1)
        response = 'HTTP/1.1 200 OK\r\n' +\
          'Content-Type: text/html\r\n' + '\r\n' +\
          '<HTML><HEAD>\r\n' +\
          '<TITLE>200 OK</TITLE>' +\
          '</HEAD><BODY>\r\n' +\
          data +\
          '</BODY></HTML>\r\n'
        new_socket.send(response.encode('utf-8'))

    new_socket.close()  

def main(port):
    # create tcp server socket
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(('', port))
    tcp_server_socket.listen(128)
    print('Binding on port: ', port)
    print('\n')

    while True:
        new_socket, client_addr = tcp_server_socket.accept()
        # create multiple processes to handle concurrent client requests
        p = multiprocessing.Process(target=service_client, args=(new_socket,client_addr,))
        p.start()
        new_socket.close()

    tcp_server_socket.close()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
        main(port)
    else:
        print('Invalid command')
        print('Example: python3 tcpserver.py 9999')
