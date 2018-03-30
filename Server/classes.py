import socket         # To use sockets
import hashlib        # For some hashing
import json           # JSON usability
import random as rand # Generating random numbers. NOT CRYPTO SECURE!!!! Change to something secure

import _globals       # Global variables
import serverUtilities as su # Server utilities
import crypto         # Library of cryptography

class Server():
    """Simple server class."""
    def __init__(self, port = _globals.PORT, pwd = 1234):
        """Initializes the server with a port number."""
        self.s = socket.socket()               # Initialize the socket
        self.host = _globals.HOST              # Host in static
        self.port = port                       # Initialize port, defaults to 9999
        self.s.bind((self.host, self.port))    # Bind the socket
        self.s.listen(5)                       # Do some listening
        
        while True:
            c, addr = self.s.accept()          # Accept connections
            # Run diffie hellman
            self.DHSecret = crypto.DHProtocol(c)
            print("Accepted connection from", addr)
            
            # Now listen for a request
            request = c.recv(1024)             # This is the request-code we got
            self.handleRequest(c, request)     # Now handle what happens due to this request

            c.close()                          # Close the client when we are done
        
    def handleRequest(self, client, request):
        """Handles a reqest. The request recieved is in JSON format"""
        jsonRequest = json.loads(request)       # Make it into a dictionary
        query = jsonRequest["request"]          # Save this because we are going to use it a lot
        if query == "file":                     # If we are asked to send a file, do that
            specifiers = jsonRequest["specifiers"]# Different specifications
            filename = specifiers["filename"]
            print("Client requested file " + filename) # Print this
            self.sendFile(client, specifiers)   # Call the method with specifiers
        
    def sendFile(self, client, specifiers):
        """Sends the file named 'filename' to the client."""
        filename = specifiers["filename"]   # The filename should be specified
        cleanFile = specifiers["cleanFile"] # Whether or not to clean the file
        try: # Try opening the file
            with open("/home/pi/Documents/Python/Server/Data/" + filename, 'r+') as fileID:
                contents = fileID.read()   # Read the data from the file
                payload = {"contents" : contents, "error" : {"code": 0, "errMessage" : ""}} # Make the payload
                client.send(json.dumps(payload)) # Send the payload
                if cleanFile:
                    fileID.truncate(0)     # Clean the file from the start, this also closes the file
                else:                      # If we are not truncating, just close
                    fileID.close()         # Close it up
        except IOError, e:    # File could not be opened
            payload = {"contents": "", "error" : {"code" : 2, "errMessage":  "[Errno 2] No such file in directory"}}
            print(e) # Print the error
                    
class Client:
    """Client class to make handeling various requests easier."""
    def __init__(self, port = _globals.PORT):
        """Initializes the client."""
        self.s = socket.socket()   # Create a socket instance
        self.host = _globals.HOST  # Set the host
        self.port = port           # Set the port
        self.s.connect((self.host, self.port)) # Connect to the server
        
        self.DHSecret = crypto.DHProtocol(self.s) # Run the DH protocol
        
    def sendRequest(self, jsonRequest):
        """Sends and handles a requests to the server. The request
        should be in JSON format, NOT a string."""
        print("Requesting...")              # Some more printing
        query = jsonRequest["request"]      # Save the query because we are going to use it a lot
        self.s.send(json.dumps(jsonRequest))#Sends the request to the server as a JSON string
        # Now handle what happens if we are to receive any information
        if query == "file":                     # If we queried a file
            dataReceived = ''                   # String to save the received data
            tempData = self.s.recv(1024)        # Receive the data we are waiting for and store it in a temp string
            while tempData:                     # While there is still data to be gathered
                dataReceived += tempData        # Update the data we received
                tempData = self.s.recv(1024)    # Query for more data
            print("Data received succesfully!") # Some printing
            # Now append the data to datafile we have or create a new one
            payload = json.loads(dataReceived)  # Make the data JSON format
            error = payload["error"]    # Extract the error code
            if error["code"] == 0:      # If there is no error
                filename = jsonRequest["specifiers"]["filename"] # This is the filename the client requested
                with open("/home/pi/Documents/Python/Server/ClientData/" + filename, "a") as fileID:
                    fileID.write(payload["contents"])            # Append the data to the file
                    fileID.close()              # Close the file when we are done
            elif error["code"] == 2:            # File not found
                print(error["errMessage"])         # There was an error, print what happens now
