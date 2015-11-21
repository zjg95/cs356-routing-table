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
    try :

        response = modifiedSentence.decode()

    except UnicodeDecodeError :
        response = ""
        for byte in modifiedSentence :
            response += chr(byte)

    clientSocket.close()

    return response

# ------------
# TestTastyTTP
# ------------

class TestServer (TestCase) :

    def test_connect_1 (self) :
        response = getResponse("test")
        self.assertEqual(1, 1)

# ----
# main
# ----

if __name__ == "__main__" :
    main()
