import socket
import hashlib
import json

import _globals
        
class Server():
    """Simple server class."""
    def __init__(self, port = _globals.PORT, pwd = 1234):
        """Initializes the server with a port number."""
        self.s = socket.socket()               # Initialize the socket
        self.host = _globals.HOST              # Host in static
        self.port = port                       # Initialize port, defaults to 9999
        self.s.bind((self.host, self.port))    # Bind the socket
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
            self.handleRequest(c, request)     # Now handle what happens due to this request

            c.close()                          # Close the client when we are done
        
    def handleRequest(self, client, request):
        """Handles a reqest. The request recieved is in JSON format"""
        jsonRequest = json.loads(request)      # Make it into a dictionary
        query = jsonRequest["request"]         # Save this because we are going to use it a lot
        if query == "file":                    # If we are asked to send a file, do that
            filename = jsonRequest["specifier"]# The filename should be specified
            print("Client requested file " + filename) # Print this
            self.sendFile(client, filename)    # Call the method with the correct specifier
        
    def sendFile(self, client, filename):
        """Sends the file named filename to the client."""
        try: # Try opening the file
            with open("/home/pi/Documents/Python/Server/Data/" + filename) as fileID:
                client.send(fileID.read()) # Send the data contained in the file
                fileID.close()
        except IOError: # File could not be opened
            print(IOError) # Print the error
                    

class Client:
    """Client class to make handeling various requests easier."""
    def __init__(self, port = _globals.PORT):
        """Initializes the client."""
        self.s = socket.socket()   # Create a socket instance
        self.host = _globals.HOST  # Set the host
        self.port = port           # Set the port
        self.s.connect((self.host, self.port)) # Connect to the server
        
        print(self.s.recv(1024))  # Print whatever the server sends, such as confirmation
        
    def sendRequest(self, request):
        """Handles requests."""
        print("Requesting...")             # Some more printing
        self.s.send(request)               # Sends the request to the server
        dataReceived = ''                  # String to save the received data
        tempData = self.s.recv(1024)       # Receive the data we are waiting for and store it in a temp string
        while tempData:                    # While there is still data to be gathered
            dataReceived += tempData       # Update the data we received
            tempData = self.s.recv(1024)   # Query for more data
        print(dataReceived)
        print("Data received succesful!")  # Some printing



















