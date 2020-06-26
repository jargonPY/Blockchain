#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import socket
import threading
import os
import sys

currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from core.verify import Verify
from core.sha import sha
from core.pool import TransactionPool
from core.utxo import UTXO
from core.blockdb import Blockdb
from client import Client

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
    
    PORT = 5050
    #SERVER = socket.gethostbyname(socket.gethostname())
    SERVER = "127.0.0.1"
    ADDR =  (SERVER, PORT)
    DISCONNECT_MESSAGE = "!DISCONNECT"
    
    def __init__(self):
        
        self.pool = TransactionPool()
        self.utxo = UTXO()
        self.blockdb = Blockdb()
        self.client = Client()
        self.listen()
        
    def listen(self):
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP
        server.bind(Server.ADDR)
        server.listen()
        print("SERVER STARTED")
        while True:
            conn, addr = server.accept() ## ADD ADDRESS TO NODE IPS FILE
            self.client.connect_to_ip(addr[0])
            print("Server connected to: ", addr)
            thread = threading.Thread(target=self.route_request, args=(conn,))
            thread.start()
            
    def route_request(self, conn):
        
        req = conn.recv(1024).decode()
        while req != Server.DISCONNECT_MESSAGE:
            if req == "NEW_TRANS":
                self.get_data(conn)
            elif req == "NEW_BLOCK":
                self.get_data(conn, trans=False)
            elif req == "GET_CHAIN_LEN":
                self.get_chain_len(conn)
            elif req == "GET_BLOCKS":
                self.get_block(conn)
            elif req == "GET_NODES":
                self.get_nodes(conn)
            else:
                msg = "FAILED_REQUEST".encode()
                conn.send(msg)
            req = conn.recv(1024).decode()
        conn.close()
            
    def get_data(self, conn, trans=True):
        
        # request the size of file to be received
        size = conn.recv(1024).decode()
        # get the file
        data = conn.recv(1024)
        total_recv = len(data)
        while total_recv < size:
            data += conn.recv(1024)
            total_recv += len(data)
        # deseralize the data
        data = data.decode() 
        # convert from to JSON to Python dictionary
        data = data.loads()
        if trans:
            self.new_trans(conn, data)
        else:
            self.new_block(conn, data)
            
    def new_trans(self, conn, trans):
        
        # check if in transaction pool
        if self.pool.check_in_pool(self, trans['txid']):
            return None
        
        if not Verify.verify_trans(trans):
            return None
        # add transaction to pool
        self.pool.insert(trans)
        # propogate transaction
        self.client.prop_trans(trans)
    
    def new_block(self, conn, block):
        
        # check if block is already in the local chain
        exists = self.blockdb.get_block_by_hash(sha(block))
        if exists != None:
            return None
        # ensure the block is valid
        if not Verify.verify_block(block):
            return None
        # remove all transaction in the block from unconfirmed pool
        self.pool.check_new_block(sha(block))
        # add all transaction outputs to utxo
        self.utxo.add_trans(block['transactions'], sha(block))
        # remove all inputs from utxo
        self.utxo.remove_trans(block['transactions'])
        # save block in Blockdb
        self.blockdb.add_block(block)
        # propogate block
        self.client.prop_blcok(block)
    
    def get_chain_len(self, conn):

        latest = self.utxo.get_latest()
        conn.send(str(latest).encode())

    def get_block(self, conn):
        
        primary_key = int(conn.recv(1024).decode())
        blocks = self.blockdb.get_from(primary_key)
        conn.send(str(blocks).encode()) 
        
        path = os.path.dirname(os.getcwd())
        for filename in blocks[3]: # WHAT IF RETURNS NONE
            file = path + "/core/" + filename + ".json"
            size = str(os.path.getsize(file))
            conn.send(size.encode())
            
            with open(os.getcwd() + "/addr.json") as file:
                data = json.load(file)
        
            data = json.dumps(data)
            conn.sendall(data.encode())
            
    
    def get_nodes(self, conn):
        
        with open(os.getcwd() + "/addr.json") as file:
            data = json.load(file)
        
        data = json.dumps(data)
        conn.send(str(sys.getsizeof(data)).encode())
        conn.sendall(data.encode()) ## WONT WORK NEEDS TO BE A JSON OBJECT
        
if __name__ == "__main__":
    server = Server()

    
    
    






