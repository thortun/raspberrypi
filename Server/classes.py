import socket
import hashlib

import _globals

class Request():
    """Class to handle which requests are sent to my server."""
    def __init__(self, type):
        """Initializes the instance."""
        self.type = type                       # Initialize the request type
        
        
        
            
class Server():
    """Simple server class."""
    def __init__(self, port = _globals.PORT, pwd = 1234):
        """Initializes the server with a port number."""
        self.s = socket.socket()               # Initialize the socket
        self.host = '192.168.1.10'             # Host in static
        self.port = port                       # Initialize port, defaults to 9999
        try:
            self.s.bind((self.host, self.port)) # Bind the socket
        except socket.error:
            self.port += (self.port + 1) % 10000 # Try a different port 
        self.s.listen(5)                       # Start listening
        
        m = hashlib.sha256()                   # Start hashing
        m.update(bytes(pwd))                   # Hash the password
        self.pwd = m.hexdigest()               # Store hash as the password
        
        while True:
            c, addr = self.s.accept()          # Accept connections
            print("Accepted connection from", addr)
            c.send("Connection successful".encode('utf-8'))
            
            # Now listen for a request
            request = c.recv(1024)             # This is the request-code we got
            print(object(request))
            print(object(_globals.REQUESTDICT['talk']))
            print(request == _globals.REQUESTDICT['talk'])
            self.handleRequest(c, request)

            c.close()                          # Close the client when we are done
        
    def close(self):
        """Closes the server."""
        self.s.close() # Close the server down
        
    def handleRequest(self, client, request):
        """Handles a reqest."""
        if request == 0: # We just want to talk
            client.send('You wanted to talk?'.encode('utf-8'))
        else:
            print('Unknown request')        