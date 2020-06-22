#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import socket
import threading
import os
from blockdb import Blockdb
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
        self.db = Blockdb()
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
        while req != Server.DISCONNECT_MESSAGE:
            if req == "NEW_TRANS":
                self.get_data(conn)
            elif req == "NEW_BLOCK":
                self.get_data(conn, trans=False)
            elif req == "GET_BLOCK":
                self.get_block(conn)
            elif req == "GET_NODES":
                self.get_nodes(conn)
            else:
                msg = "FAILED_REQUEST".encode()
                conn.send(msg)
            req = conn.recv(1024).decode()
            
    def get_data(self, conn, trans=True):
        
        # request the size of file to be received
        conn.send("GET_SIZE".encode())
        size = conn.recv(1024).decode()
        # get the file
        data = conn.recv(1024)
        total_recv = len(data)
        while total_recv < size:
            data += conn.recv(1024)
            total_recv += len(data)
        
        data = data.decode()
        if trans:
            self.new_trans(conn, data)
        else:
            self.new_block(conn, data)
            
    def new_trans(self, conn, trans):
        
        # check if in transaction pool
        if self.node.pool.check_in_pool(self, trans['txid']):
            return None
        
        if not Verify.verify_trans(trans):
            return None
        # add transaction to pool
        self.node.pool.insert(trans)
        # propogate transaction
        self.node.prop_data(trans, data_type="trans")
    
    def new_block(self, conn, block):
        
        # check if block is already in the local chain
        exists = self.db.get_block_by_hash(Blockdb.sha(block))
        if exists != None:
            return None
        # ensure the block is valid
        if not Verify.verify_block(block):
            return None
        # remove all transaction in the block from unconfirmed pool
        self.node.pool.check_new_block(Blockdb.sha(block))
        # add all transaction outputs to utxo
        self.node.utxo.add_trans(block['transactions'])
        # remove all inputs from utxo
        self.node.utxo.remove_trans(block['transactions'])
        # save block in Blockdb
        self.node.blockdb.add_block(block)
        # propogate block
        self.node.prop_data(block, data_type="block")
        
    def get_block(self, conn):
        
        conn.send("LASTEST")
        latest = conn.recv(1024).decode()
        primary_key = self.db.get_block_by_hash(latest)
        
        for filename in self.db.get_from(primary_key)[3]: # WHAT IF RETURNS NONE, is 3 the correct index
            size = str(os.path.getsize(filename))
            conn.send(f"BLOCK SIZE {size}".encode())
            
            with open(filename, 'rb') as f:
                data = f.read(1024)
                conn.send(data)
                while data != "":
                    data = f.read(1024)
                    conn.send(data)
        conn.send("DONE")
    
    def get_nodes(self, conn):
        
        ips = json.load(os.getcwd() + "/addr.json")
        conn.send(ips.encode())
        

    

    
    
    






