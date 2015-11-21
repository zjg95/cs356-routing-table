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
MAX_FILE_SIZE = 8192

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

# -----------
# get request
# -----------

def getRequest (socket) :
	"""
    receive bytes from a socket
    socket the socket of the client
    return a string containing the client's request
    """
	request = socket.recv(MAX_FILE_SIZE)
	request = bytes.decode(request)
	return request

# ---------------
# return response
# ---------------

def returnResponse (response, socket) :
	"""
    send bytes over a socket
    response the bytes to send
    socket the client socket to use
    """
	socket.send(response)

# ------
# listen
# ------

def listen() :
	"""
    listen for clients, accept the connection, handle the request, close the connection
    """
	while True:

		# accept the connection to a client
		clientSocket, addr = serverSocket.accept()

		# obtain the request through the wire
		rawRequest = getRequest(clientSocket)

		# add the headers to the response
		# rawResponse = getResponse(responseDict)
		rawResponse = "test".encode()

		# send the response over the wire
		returnResponse(rawResponse, clientSocket)

		#close the connection
		clientSocket.close()

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
