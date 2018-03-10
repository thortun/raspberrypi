import socket

def main():
    
    s = socket.socket()
    
    host = '192.168.1.10'
    port = 9077
    s.bind((host,port))
    s.listen(5)


    while True:
        s.listen(5)
        c, addr = s.accept()
        
        # Connection talk
        print("Connection accepted from ", addr)
        c.send("Thank you for connecting")
        
        # Open a file to write to
        fileID = open('/home/pi/Documents/Python/Scraping/utilities.py', 'wb')
        
    
        data_received = c.recv(1024)
        while data_received: # While there is still data to be found
            fileID.write(data_received)
            data_received = c.recv(1024) # Retrieve more data
        
        fileID.close()
        c.close()

if __name__ == '__main__':
    main()
