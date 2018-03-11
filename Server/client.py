#!/usr/bin/python               # This is client.py file
import socket 

import classes
import _globals

def main():

    c = classes.Client()
    c.sendRequest(2)

if __name__ == '__main__':
    main()