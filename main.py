#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.blockdb import Blockdb
from core.pool import TransactionPool
from core.utxo import UTXO
from core.wallet import Wallet
from network.server import Server
from network.server import Client

"""
Node A --> (client A, server A)
When client A connects to server B, node B tells client B to connect to server A
"""

class Main():
    
    def __init__(self):
        
        self.pool = TransactionPool()
        self.blockdb = Blockdb()
        self.utxo = UTXO()
        self.client = Client(self.blockdb)
        self.server = Server(self.pool, self.utxo, self.client, self.blockdb)
        self.wallet = Wallet(self.pool, self.utxo, self.client)
        
        
        
    def add_client(self, addr):
        """
        Called by the Server class to establish a two-way connection 
        """
        
        self.client.connect_to_ip(addr)
        
    def broadcast(self, data, data_type=""):
        
        if data_type == "trans":
            self.client.prop_trans(data)
        elif data_type == "block":
            self.client.prop_block(data)
        else:
            return None
            
        
        
        
        