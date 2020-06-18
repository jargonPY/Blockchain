#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pool import TransactionPool
from verify import Verify
from utxo import UTXO

class Main():
    
    def __init__(self):
        
        self.pool = TransactionPool()
        self.utxo = UTXO()
        