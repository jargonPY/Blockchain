#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sqlite3
import unittest
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from core.pool import TransactionPool
from core.sha import sha
from core.utxo import UTXO

class UTXOClone(UTXO):
    
    def __init__(self):
      
        self.conn = sqlite3.connect(":memory:")
        self.c = self.conn.cursor()
        
        self.c.execute("""CREATE TABLE utxo (
                id INTEGER PRIMARY KEY,
                txid TEXT,
                address TEXT,
                change INTEGER,
                amount REAL,
                block INTEGER
                )""")
        
        self.conn.commit()

class VerifyTestCase(unittest.TestCase):
    
    def test_verify_root(self):
        
        pass
    
    def test_verify_pow(self):
        
        pass
    
    def test_verify_prev_block(self):
        
        pass
    
    def test_get_prev_trans(self):
        
        pass
    
    def test_verify_hash(self):
        
        pass
    
    def test_verify_sig(self):
        
        pass
    
    def test_verify_balance(self):
        
        pass
    
    def test_double_spend(self):
        
        pass
    
    def test_verify_trans(self):
        
        pass
    
    def test_verify_block(self):
        
        pass

if __name__ == '__main__':
    unittest.main()