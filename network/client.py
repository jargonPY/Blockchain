#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import socket
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
    
    PORT = 5050
    SERVER = "127.0.0.1"
    DISCONNECT_MESSAGE = "!DISCONNECT"
    
    def __init__(self):
        
        self.blockdb = Blockdb()
        self.connections = { } # {ip : conn}
        with open(os.getcwd() + "/addr.json") as file:
            self.ips = json.load(file)
        self.startup_connect()
    
    def startup_connect(self):
        """
        This method is called when a node first enters/reenters a network,
        it queries its database of known nodes in the network and
        establishes a connection
        """
        
        for num, ip in enumerate(self.ips.keys()): # a list of ip addresses to connect to
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP ## SHOULD IT BE IN THE FOR LOOP ???
            try:
                client.connect((ip, self.PORT))
                self.connections[ip] = client
                print("Client connected to :", ip)
            except: ## ENSURE THE FAILURE IS DUE TO A SERVER BEING DOWN
                self.failed_conn(ip)
    
    def connect_to_ip(self, ip): ## CHECK TO ENSURE CONNECTION IS NOT ALREADY MADE
        """
        When a new node on the network connects to local node, this 
        method is establisehd a two-way connection
        """
        
        if ip in self.connections.keys():
            return None
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((ip, self.PORT))
            self.connections[ip] = client
        except:
            self.failed_conn(ip)
        else:
            self.add_ip(ip)
        
    def add_ip(self, ip):
        
        if ip not in self.ips.keys():
            self.ips[ip] = 0
    
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

        trans = json.dumps(trans)
        for conn in self.connections.values():
            conn.send("NEW_TRANS".encode())
            conn.send(sys.getsizeof(trans))
            conn.sendall(trans.encode()) ## RETURNS NONE IF SUCESSFUL, THROWS ERROR OTHERWISE, ADD ERROR HANDLING
    
    def prop_block(self, block):
        
        block = json.dumps(block)
        for conn in self.connections.values():
            conn.send("NEW_BLOCK".encode())
            conn.send(sys.getsizeof(block))
            conn.sendall(block.encode())

    def req_chain(self):

        longest = (None, 0)
        for conn in self.connections.values():
            conn.send("GET_CHAIN_LEN")
            chain_len = int(conn.recv(1024).decode())
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
        
        latest = self.blockdb.get_latest()
        conn.send("GET_BLOCKS".encode())
        conn.send(str(latest).encode())
        num_blocks = int(conn.recv(1024).decode())

        block = 1
        while block <= num_blocks:
            block_size = int(conn.recv(1024).decode())
            data = conn.recv(1024)
            
            while len(data) < block_size:
                data += conn.recv(1024)
            
            data = json.loads(data.decode())
     #       self.blockdb.add_block(data) ## DOESNT VARIFY THE BLOCK
            block += 1
    
    def req_node(self):
        
        for conn in self.connections.values():
            conn.send("GET_NODES")
            file_size = int(conn.recv(1024).decode())
            
            data = conn.recv(1024).decode()
            while len(data) < file_size:
                data += conn.recv(1024)
            
            data = json.loads(data.decode())
            for key in data.keys():
                if key not in self.ips.keys:
                    self.ips[key] = 0 ## HAVE TO RECIEVE LOTS OF DATA
                    
    def close(self):
        
        for conn in self.connections.values():
            conn.send(self.DISCONNECT_MESSAGE)
            conn.close()

    
    