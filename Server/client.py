#!/usr/bin/python               # This is client.py file
import socket 

def main():

    s = socket.socket()         # Create a socket object
    host = '192.168.1.10'       # Get local machine ip
    port = 9079                 # Reserve a port for your service.

    s.connect((host, port))
    print(s.recv(1024).decode('utf-8'))


    s.close()
    

if __name__ == '__main__':
    main()