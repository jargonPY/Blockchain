#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.blockdb import Blockdb
from core.pool import TransactionPool
from core.verify import Verify
from core.utxo import UTXO
from network.server import Server
from network.server import Client

"""
Node A --> (client A, server A)
When client A connects to server B, node B tells client B to connect to server A
"""

class Main():
    
    def __init__(self):
        
        self.pool = TransactionPool()
        self.utxo = UTXO()
        self.server = Server(self) # passes self.Main instance
        self.client = Client(self)
        self.blockdb = Blockdb()
        
    def add_client(self, addr):
        """
        Called by the Server class to establish a two-way connection 
        """
        
        self.client.connect_to_server(addr)
        
    def prop_data(self, data, data_type=""):
        
        if data_type == "trans":
            self.client.prop_trans(data)
        elif data_type == "block":
            self.client.prop_block(data)
        else:
            return None
            
        
        
        
        