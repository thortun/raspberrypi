#!/usr/bin/python               # This is client.py file
import socket 

import classes
import _globals

def main():

    s = socket.socket()         # Create a socket object
    host = '192.168.1.10'       # Get local machine ip
    port = _globals.PORT                 # Reserve a port for your service.

    print(s.recv(1024).decode('utf-8'))
    
    # Now wend a request
    request = 'talk'
    s.send(bytes(_globals.REQUESTDICT[request]))
    
    # Close the socket with the server
    s.close()
    

if __name__ == '__main__':
    main()