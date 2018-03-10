import socket

class Request():
    """Class to handle which requests are sent to my server."""
    def __init__(self, requestType):
        """Initializes the instance."""
        self.requestType = requestType          # Initialize the request type
        
        
class Server():
    """Simple server class."""
    def __init__(self, port = 9079):
        """Initializes the server with a port number."""
        self.s = socket.socket()               # Initialize the socket
        self.host = '192.168.1.10'             # Host in static
        self.port = port                       # Initialize port, defaults to 9999
        self.s.bind((self.host, self.port))    # Bind the socket
        self.s.listen(5)                       # Start listening
        
        while True:
            c, addr = self.s.accept()          # Accept connections
            print("Accepted connection from", addr)
            c.send("Connection successful".encode('utf-8'))
            
            # Now listen for a request
            dataReceived = c.recv(1024) # Store data in a vaiable
            while dataReceived:                # While we are still gethering data
                print(dataReceived)            # For now, print it
                dataReceived = c.recv(1024)    # Gather more data
            
            c.close()
        
    def close(self):
        """Closes the server."""
        self.s.close() # Close the server down