#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import socket
import threading
import os
import sys

class Client():
    
    """
    Client should initiate all data transfer
     - progpogate for new transactions
     - progpogate for new block
     - request recent blocks
     - request IPs
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
        self.startup_connect()
    
    def startup_connect(self):
        """
        This method is called when a node first enters/reenters a network,
        it queries its database of known nodes in the network and
        establishes a connection
        """
       
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP ## SHOULD IT BE IN THE FOR LOOP ???
        ips = json.load(os.getcwd() + "/addr.json")
        for num, server in enumerate(ips['working']): # a list of ip addresses to connect to
            addr = (server, Client.PORT)
            try:
                client.connect(addr)
                self.connections.append((client, num+1))
            except: ## ENSURE THE FAILURE IS DUE TO A SERVER BEING DOWN
                self.remove_node(server)
    
    def connect_to_server(self, server): ## CHECK TO ENSURE CONNECTION IS NOT ALREADY MADE
        """
        When a new node on the network connects to local node, this 
        method is establisehd a two-way connection
        """
        
        addr = (server, Client.PORT)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)
        num = len(self.connections) + 1
        self.connections.append((client, num))
    
    def check_conn(self):
        
        pass
    
    def remove_node(self, server):
        """
        When a node can't be reached this method is called 
        """
        
        pass

    def prop_trans(self, trans):
        """
        trans : dict
            dictionary containing transaction data
        """

        trans = json.dump(trans)
        for conn in self.connections:
            conn.send("NEW_TRANS".encode())
            # wait for server to request size
            get_size = conn.recv(1024)
            if get_size != "GET_SIZE":
                pass
            ## JSON Object --> y = json.dumps(trans)
            conn.send(sys.getsizeof(trans))
            conn.sendall(bytes(trans, encoding="utf-8")) ## RETURNS NONE IF SUCESSFUL, THROWS ERROR OTHERWISE, ADD ERROR HANDLING
    
    def prop_block(self, block):
        
        block = json.dump(block)
        for conn in self.connections:
            conn.send("NEW_BLOCK".encode())
            get_size = conn.recv(1024)
            if get_size != "GET_SIZE":
                pass
            conn.send(sys.getsizeof(trans))
            conn.sendall(bytes(block, encoding="utf-8"))

    def req_chain(self):

        pass
    
    def req_block(self, conn):
        """
        conn : socket object
            the connection with the longest chain

        Send the hash of the latest block all nodes will send back the 
        number of missing blocks, this node will extend using the longest chain
        method
        """
        
        latest = self.node.blockdb.get_latest()[1] # (id, hash, filename)
        conn.send("NEW_BLOCKS".encode())
        recv = conn.recv(1024)
        if recv != "LATEST":
            pass
        conn.send(latest.encode())

    
    def req_node(self):
        
        conn.send("GET_NODES")
        nodes = conn.recv(1024) 
    
    