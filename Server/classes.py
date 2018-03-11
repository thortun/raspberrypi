import socket
import hashlib
import time

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
            try:
                self.handleRequest(c, int(request))# Now handle what happens due to this request
            except ValueError: # This happens if the client does not request anything
                print('Invalid request, client did not send any request?')
            print(request)

            c.close()                          # Close the client when we are done
        
    def close(self):
        """Closes the server."""
        self.s.close() # Close the server down
        
    def handleRequest(self, client, request):
        """Handles a reqest."""
        if request == 0: # We just want to talk
            client.send("You wanted to talk?".encode('utf-8'))
        elif request == _globals.REQUESTDICT['file']:    # Requesting a file
            print('Client requesting file')
        elif request == _globals.REQUESTDICT['weather']: # Requested weather data
            print('Client requesting weather')
            # Begin by opening the current weather data file
            filePath = '/home/pi/Documents/Python/Server/Data/weatherData.txt' # Filepath
            with open(filePath, 'r') as fileID: # Open for reading
                data = fileID.read()            # Read the data
                fileID.close()                  # Reading done, close down the file
            client.send(data.encode('utf-8'))   # Send the correctly encoded data
            print(data.encode('utf-8'))
            
        else:
            print('Unknown request. Undefined request code.')
            
class Client:
    """Client class to make handeling various requests easier."""
    def __init__(self, port = _globals.PORT):
        """Initializes the client."""
        self.s = socket.socket()   # Create a socket instance
        self.host = _globals.HOST  # Set the host
        self.port = port           # Set the port
        self.s.connect((self.host, self.port)) # Connect to the server
        
        print(self.s.recv(1024))   # Print whatever the server sends, such as confirmation
        
    def sendRequest(self, request):
        """Handles requests."""
        if request == _globals.REQUESTDICT['talk']:      # We just want to talk
            pass
        elif request == _globals.REQUESTDICT['file']:    # Request a file
            pass
        elif request == _globals.REQUESTDICT['weather']: # Request weather data
            self.s.send(str(request).encode('utf-8'))    # Send the correct request
            time.sleep(1)
            print('Retrieving weather data')             # Print a message
            data = self.s.recv(1024)                     # Receive the first data block
            weatherData = ''                             # Make a variable to store all the data
            while data:                                  # While there are still data to recieve
                weatherData += data                      # Append the new block to the weather data
                data = self.s.recv(1024)                 # Store the next block of data
            print('Data retrieved successful!')          # Some more information printed
            print(data)
            # Now append the data to a file, or make a new file and add the data
            filePath = '/home/pi/Documents/Python/Server/ClientData/weatherData.txt' # Path to save the data
            with open(filePath, 'w') as fileID:
                fileID.write(data)                       # Finally append the weather data
                fileID.close()                           # And close the file
                
