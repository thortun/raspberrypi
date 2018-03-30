#!/usr/bin/python               # This is client.py file
import socket
import json
# Local modules
import classes
import _globals

def main():

    c = classes.Client()
    request = {"request" : "file", "specifiers": {"filename" : "weatherData.txt", "cleanFile" : False}}
    c.sendRequest(request)
    
    
if __name__ == '__main__':
    main()