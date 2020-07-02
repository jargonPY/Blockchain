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
    SERVER = "192.168.0.22"
    #SERVER = "127.0.0.1"
    ADDR =  (SERVER, PORT)
    DISCONNECT_MESSAGE = "DISCONNECT"
    
    def __init__(self):
        
        self.pool = TransactionPool()
        self.client = Client()
        
        self.client.req_chain() # update chain since last startup
        self.listen()
        
    def listen(self):
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4, TCP
        server.bind(self.ADDR)
        server.listen()
        print("SERVER STARTED")
        while True:
            conn, addr = server.accept() ## ADD ADDRESS TO NODE IPS FILE
            self.client.connect_to_ip(addr[0])
            print("Server connected to: ", addr)
            thread = threading.Thread(target=self.route_request, args=(conn,))
            thread.start()
           
    def route_request(self, conn):
        
        try:
            req = conn.recv(1024).decode()
            while req != self.DISCONNECT_MESSAGE:
                if req == "NEW_TRANS":
                    print(req)
                    self.get_data(conn)
                elif req == "NEW_BLOCK":
                    print(req)
                    self.get_data(conn, trans=False)
                elif req == "GET_CHAIN_LEN":
                    print(req)
                    self.get_chain_len(conn)
                elif req == "GET_BLOCKS":
                    print(req)
                    self.get_block(conn)
                elif req == "GET_NODES":
                    print(req)
                    self.get_nodes(conn)
                else:
                    msg = "FAILED_REQUEST".encode()
                    conn.send(msg)
                req = conn.recv(1024).decode()
        except Exception as e:
            print("Exception occured with peer: ", e)
        conn.close()
        # when this function returns the thread will be closed
            
    def get_data(self, conn, trans=True):
        
        # request the size of file to be received
        conn.send("GET_SIZE".encode())
        size = int(conn.recv(1024).decode())
        # get the file
        conn.send("SEND_DATA".encode())
        data = conn.recv(1024)
        total_recv = len(data)
        while total_recv < size:
            data += conn.recv(1024)
            total_recv += len(data)
        # deseralize the data
        data = data.decode() 
        # convert from JSON to Python dictionary
        data = json.loads(data)
        if trans:
            self.new_trans(conn, data)
        else:
            self.new_block(conn, data)
            
    def verify(self, data_type, data):
        """
        data_type : str
            'trans' or 'block'
        data : dict
            the transaction or block
        
        return : boolean
            True if verfied, False otherwise
        """
        
        ver = Verify(self.pool)
        if data_type == "trans":
            return ver.verify_trans(data)
        else:
            return ver.verify_block(data)
            
    def new_trans(self, conn, trans):
        
        # check if in transaction pool
        if self.pool.check_in_pool(trans['txid']):
            return None
        
        if not self.verify("trans", trans):
            return None
        print("New transaction verified")
        # add transaction to pool
        self.pool.insert(trans)
        # propogate transaction
        self.client.prop_trans(trans)
    
    def new_block(self, conn, block):
        
        utxo = UTXO()
        blockdb = Blockdb()
        # check if block is already in the local chain
        exists = blockdb.get_block_by_hash(sha(block))
        if exists != None:
            return None
        # ensure the block is valid
        if not self.verify("block", block):
            return None
        print("New block verified")
        # remove all transaction in the block from unconfirmed pool
        self.pool.check_new_block(sha(block))
        # add all transaction outputs to utxo
        utxo.add_trans(block['transactions'], sha(json.dumps(block)))
        # remove all inputs from utxo
        utxo.remove_trans(block['transactions'])
        # save block in Blockdb
        blockdb.add_block(block)
        # propogate block
        self.client.prop_block(json.dumps(block).encode())
    
    def get_chain_len(self, conn):

        blockdb = Blockdb()
        latest = blockdb.get_latest()
        conn.send(str(latest).encode())

    def get_block(self, conn):
        
        blockdb = Blockdb()
        primary_key = int(conn.recv(1024).decode())
        blocks = blockdb.get_from(primary_key)
        conn.send(str(len(blocks)).encode()) 
        
        if len(blocks) == 0:
            return None
        
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

    
    
    






