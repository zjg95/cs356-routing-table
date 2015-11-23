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
from ipaddress import *
from sys import argv, exit

# ----------------
# server meta data
# ----------------

serverName = "Routah"
serverVersion = "1.0"
MAX_FILE_SIZE = 8192
endl = "\r\n"

DEFAULT_MASK = IPv4Network("0.0.0.0/0")
DEFAULT_HOST = 'A'
DEFAULT_COST = 100

hostList = {}

# -----------------
# address not found
# -----------------

class AddressNotFoundException (Exception) :
	pass

# ----
# host
# ----

class Host :

	# [mask : cost]
	# [0.0.0.0/0: 100]

	def __init__(self, name) :
		self.name = name
		self.addresses = {}

	def query(self, address) :
		bestNetwork = DEFAULT_MASK
		bestCost = DEFAULT_COST
		for network in self.addresses :
			if address in network :
				# is this network cheaper than the cheapest?
				cost = self.addresses[network]
				if cost < bestCost :
					bestNetwork = network
					bestCost = cost
		if bestNetwork != DEFAULT_MASK :
			return bestNetwork, bestCost
		raise AddressNotFoundException

	def update(self, mask, cost) :
		self.addresses[mask] = cost

	def name(self) :
		return str(self.name)

# -----
# query
# -----

def query (address) :
	ip = IPv4Address(address)

	mask = DEFAULT_MASK
	name = DEFAULT_HOST
	cost = DEFAULT_COST

	for hostName in hostList :
		try :
			currentMask, currentCost = hostList[hostName].query(ip)

			if currentCost < cost or (currentCost == cost and currentMask.prefixlen > mask.prefixlen) :
				name = hostName
				mask = currentMask
				cost = currentCost

		except AddressNotFoundException :
			pass

	return address + " " + name + " " + str(cost)

# ------
# update
# ------

def update (line) :
	host, mask, cost = line.split(' ')
	mask = IPv4Network(mask)
	cost = int(cost)
	hostList[host].update(mask, cost)

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
	print(request)
	return request

# -------------
# parse request
# -------------

def parseRequest (request) :
	"""
    parse the pieces of the request, store in a dictionary
    request a string containing the client's request
    return a dictionary
    """
	details = {}
    
	lines = request.splitlines()
	size = len(lines)

	assert size >= 3
	assert lines[size - 1] == "END"

	details["command"] = lines[0]
	details["body"] = [lines[i] for i in range(1, size - 1)]
	assert len(details["body"]) == size - 2
	assert len(details["body"]) > 0

	return details

# ------------
# get response
# ------------

def getResponse (details) :
	"""
    create a string response containing the appropriate HTTP headers
    details a dictionary containing the header data
    return a string
    """
	response = ""
	if details["command"] == "UPDATE" :
		response += "ACK" + endl
		assert len(details["body"]) > 0
		for line in details["body"] :
			update(line)
	else :
		response += "RESULT" + endl
		assert len(details["body"]) == 1
		response += query(details["body"][0]) + endl
	response += "END" + endl
	print(response + "----------")
	return response.encode()

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

		# parse the request into a dictionary
		parsedRequest = parseRequest(rawRequest)

		# get an encoded string for our response
		rawResponse = getResponse(parsedRequest)

		# send the response over the wire
		returnResponse(rawResponse, clientSocket)

		#close the connection
		clientSocket.close()

# ----
# main
# ----

print("----------")
print(serverName + "/" + serverVersion)
print("----------")

# define port number and socket
port = getPort()
serverSocket = socket(AF_INET, SOCK_STREAM)

# initialize host list
for i in range(ord('A'), ord('I')) :
	hostList[chr(i)] = Host(chr(i))

# activate socket
serverSocket.bind(('', port))
serverSocket.listen(1)
listen()
