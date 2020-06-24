#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import socket
import threading
import os
import sys
from core.blockdb import Blockdb

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
    
    def __init__(self):
        
        self.blockdb = Blockdb()
        self.ips = json.load(os.getcwd() + "/addr.json")
        self.connections = [ ] # list of tuples (conn, conn_id)
        self.startup_connect()
    
    def startup_connect(self):
        """
        This method is called when a node first enters/reenters a network,
        it queries its database of known nodes in the network and
        establishes a connection
        """
       
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP ## SHOULD IT BE IN THE FOR LOOP ???
        for num, ip in enumerate(self.ips['working']): # a list of ip addresses to connect to
            addr = (ip, self.PORT)
            try:
                client.connect(addr)
                self.connections.append((client, num+1))
            except: ## ENSURE THE FAILURE IS DUE TO A SERVER BEING DOWN
                self.failed_conn(ip)
    
    def connect_to_ip(self, ip): ## CHECK TO ENSURE CONNECTION IS NOT ALREADY MADE
        """
        When a new node on the network connects to local node, this 
        method is establisehd a two-way connection
        """
        
        addr = (ip, self.PORT)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(addr)
            num = len(self.connections) + 1
            self.connections.append((client, num))
        except:
            self.failed_conn(ip)
    
    def check_conn(self):
        
        pass
    
    def failed_conn(self, ip):
        """
        When a node can't be reached this method is called 
        """
        
        if self.ips[ip] < 3:
            self.ips[ip] += 1
        else:
            del self.ips[ip]

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
            conn.sendall(trans.encode()) ## RETURNS NONE IF SUCESSFUL, THROWS ERROR OTHERWISE, ADD ERROR HANDLING
    
    def prop_block(self, block):
        
        block = json.dump(block)
        for conn in self.connections:
            conn.send("NEW_BLOCK".encode())
            get_size = conn.recv(1024)
            if get_size != "GET_SIZE":
                pass
            conn.send(sys.getsizeof(block))
            conn.sendall(block.encode())

    def req_chain(self):

        longest = (None, 0)
        for conn in self.connections:
            conn.send("GET_CHAIN_LEN")
            chain_len = conn.recv(1024)
            if chain_len > longest[1]:
                longest = (conn, chain_len)
        # once longest chain is found request the blocks
        self.req_block(longest[0])
    
    def req_block(self, conn):
        """
        conn : socket object
            the connection with the longest chain

        Send the hash of the latest block all nodes will send back the 
        number of missing blocks, this node will extend using the longest chain
        method
        """
        
        latest = self.blockdb.get_latest()[1] # (id, hash, filename)
        conn.send("NEW_BLOCKS".encode())
        recv = conn.recv(1024)
        if recv != "LATEST":
            pass
        conn.send(latest.encode())
        num_blocks = conn.recv(1024)

        block = 1
        while block <= num_blocks:
            block_size = conn.recv(1024).decode()
            data = conn.recv(1024)
            while len(data) < block_size:
                data += conn.recv(1024)
            self.blockdb.add_block(data.decode()) ## DOESNT VARIFY THE BLOCK
            block += 2

    
    def req_node(self):
        
        for conn in self.connections:
            conn.send("GET_NODES")
            nodes = conn.recv(1024).decode()
            for key in nodes.keys():
                if key not in self.ips.keys:
                    self.ips[key] = 0
                    
    def close(self):
        
        for conn in self.connections:
            conn.send(self.DISCONNECT_MESSAGE)
            conn.close()

    
    