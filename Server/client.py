#!/usr/bin/python               # This is client.py file
import socket
import json
# Local modules
import classes
import _globals

def main():

    c = classes.Client()
    filename = 'weatherData.txt'
    request = {"request":"file", "specifier": filename}
    request = json.dumps(request) # Make into json string
    c.sendRequest(request)

if __name__ == '__main__':
    main()