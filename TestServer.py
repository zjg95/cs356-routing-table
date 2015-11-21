#!/usr/bin/env python3

# -------------------------------
# cs356-routing-table/TestServer.py
# Copyright (C) 2015
# Zachary J. Goodman
# -------------------------------

# https://docs.python.org/3.4/reference/simple_stmts.html#grammar-token-assert_stmt

# -------
# imports
# -------

from io       import StringIO
from unittest import main, TestCase

from socket import *

serverName = 'localhost'
serverPort = 4444

def getResponse (request) :
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    clientSocket.send(request.encode())
    modifiedSentence = clientSocket.recv(2048)
    
    response = modifiedSentence.decode()

    clientSocket.close()

    return response

# ------------
# TestTastyTTP
# ------------

class TestServer (TestCase) :

    def test_update_1 (self) :
        request = "UPDATE\r\nA 200.34.55.0/24 22\r\nEND\r\n"
        response = getResponse(request)
        self.assertEqual("ACK\r\nEND\r\n", response)

    def test_query_1 (self) :
        request = "QUERY\r\n200.35.55.13\r\nEND\r\n"
        response = getResponse(request)
        self.assertEqual("RESULT\r\n200.35.55.13\r\nEND\r\n", response)

# ----
# main
# ----

if __name__ == "__main__" :
    main()
