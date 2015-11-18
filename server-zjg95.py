#!/usr/bin/env python3

# -------------------------------
# cs356-routing-table/server-zjg95.py
# Copyright (C) 2015
# Zachary J. Goodman
# -------------------------------

# -------
# imports
# -------

from socket	import *
from sys import argv, exit

# ----------------
# server meta data
# ----------------

serverName = "Server"
serverVersion = "0.1"

# --------
# get port
# --------

def getPort () :
	"""
    parse the port number from the command line; if failure, terminate program
    return an int value containing the port number
    """
	if len(argv) != 2 :
		print("Usage requires exactly one command line argument! python3 server-zjg95.py <port>")
		exit()
	return int(argv[1])

# ---------------
# return response
# ---------------

def returnResponse (response, socket) :
	"""
    send bytes over a socket
    response the bytes to send
    socket the client socket to use
    """
	# return the result to the client
	socket.send(response)

def listen() :
	pass

# ----
# main
# ----

print("------------")
print(serverName + "/" + serverVersion)
print("------------")

# define port number and socket
port = getPort()
serverSocket = socket(AF_INET, SOCK_STREAM)

# activate socket
serverSocket.bind(('localhost', port))
serverSocket.listen(1)
listen()
