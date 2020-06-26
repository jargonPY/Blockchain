#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sqlite3
import unittest
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from core.utxo import UTXO
from core.sha import sha

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
        

class UTXOTestCase(unittest.TestCase):
    
    trans_a = {"txid":"b1", 
               "vin":[{"txid":"a4", "change":0, "sig":"df42"}],
               "vout":[{"amount":750, "address":"a21"}],
               "block":1}
        
    trans_b = {"txid":"b2", 
               "vin":[{"txid":"a4", "change":0, "sig":"df43"}],
               "vout":[{"amount":750, "address":"a22"}],
               "block":1}
    
    check_a = (1, "b1", "a21", 0, 750, 1)
    check_b = (2, "b2", "a22", 1, 240.0, 2)
    
    def setUp(self):
        """
        Before every method is run a new database is setup and two entries are
        added, this sets up the conditions where each method would be called on,
        and allows for the independent testing of each method
        """
        
        self.utxo = UTXOClone()
        for trans in [self.trans_a, self.trans_b]:
            with self.utxo.conn:
                self.utxo.c.execute("INSERT INTO utxo VALUES (NULL, :txid, :address, :change, :amount, :block)",
                                                            {'txid': trans['txid'],
                                                             'address': trans['vout'][0]['address'],
                                                             'change': 0,
                                                             'amount': trans['vout'][0]['amount'],
                                                             'block': trans['block']})
            
    def test_get_by_txid(self):
        
        self.assertEqual(self.utxo.get_by_txid("b1"), self.check_a)
        self.assertEqual(self.utxo.get_by_txid("b2"), self.check_b)
    
    def test_get_by_pk(self):
        
        self.assertEqual(self.utxo.get_by_pk("a21")[0], self.check_a)
        self.assertEqual(self.utxo.get_by_pk("a22")[0], self.check_b)
    
    def test_add_trans(self):
        
        self.utxo.add_trans([self.check_a, self.check_b], "asd13441")
        self.utxo.c.execute("SELECT * FROM utxo WHERE id = 3")
        self.assertEqual(self.utxo.c.fetchone(), self.check_a)
        self.utxo.c.execute("SELECT * FROM utxo WHERE id = 4")
        self.assertEqual(self.utxo.c.fetchone(), self.check_b)
        
    def test_remove_trans(self):
        
        pass

if __name__ == '__main__':
    unittest.main()














