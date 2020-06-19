#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.pool import TransactionPool
from core.verify import Verify
from core.utxo import UTXO
from network.server import Node

class Main():
    
    def __init__(self):
        
        self.pool = TransactionPool()
        self.utxo = UTXO()
        self.node = Node(self) # passes self.Main instance
        
        
        
        