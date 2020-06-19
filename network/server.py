#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import socket
import threading
import os
from core.verfiy import Verify

class Server():
    
    """
    Server should only respond to requests/data from client
     - listen for new transactions
     - listen for new blocks
     - provide most recent blocks (after some specified block #)
        - every block recieved is confirmed and all transactions are added to UTXO
        - if several blocks have to be recieved CHECK IN ORDER
     - provide IP addresses for node connections
    """
    
    HEADER = 64
    PORT = 5050
    #SERVER = socket.gethostbyname(socket.gethostname())
    SERVER = "127.0.0.1"
    ADDR =  (SERVER, PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"
    
    def __init__(self, node):
        
        self.node = node
        self.connections = [ ] # list of tuples (conn, conn_id)
        self.listen()
        
    def listen(self):
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP
        server.bind(Server.ADDR)
        server.listen()
        print("SERVER STARTED")
        while True:
            conn, addr = server.accept() ## ADD ADDRESS TO NODE IPS FILE
            self.node.add_client(addr)
            thread = threading.Thread(target=self.route_request, args=(conn,))
            thread.start()
            
    def route_request(self, conn):
        
        req = conn.recv(1024).decode()
        if req == "NEW_TRANS":
            self.new_trans()
        elif req == "NEW_BLOCK":
            self.new_block()
        elif req == "GET_BLOCK":
            self.get_block()
        elif req == "GET_NODES":
            self.get_nodes()
        else:
            msg = "FAILED_REQUEST".encode()
            self.conn.send(msg)
    
    def new_trans(self, conn):
        
        pass
        self.route_request(conn)
    
    def new_block(self, conn):
        
        pass
        self.route_request(conn)
        
    def get_block(self, conn):
        
        pass
        self.route_request(conn)
        
    def get_nodes(self, conn):
        
        ips = json.load(os.getcwd() + "/addr.json")
        self.route_request(conn)

    
    
    
    
    
    
    
    
    






