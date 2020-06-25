#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sqlite3
import unittest
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from core.blockdb import Blockdb
from core.sha import sha

class BlockdbClone(Blockdb):
    
    def __init__(self):
      
        self.conn = sqlite3.connect(":memory:")
        self.c = self.conn.cursor()
        
        self.c.execute("""CREATE TABLE blocks (
                    id INTEGER PRIMARY KEY,
                    hash TEXT,
                    file TEXT
                    )""")
        
        self.conn.commit()
        

class BlockdbTestCase(unittest.TestCase):
    
    block_a = {"data":"random", "more":"random_data"}
    block_b = {"data_b":"random", "more_b":"random_data"}
    check_a = (1, sha(json.dumps(block_a)), 'block_1')
    check_b = (2, sha(json.dumps(block_b)), 'block_2')
    
    def setUp(self):
        
        self.blockdb = BlockdbClone()
    
    def test_get_latest(self):
        
        self.assertEqual(self.blockdb.get_latest(), None)
        self.blockdb.c.execute("INSERT INTO blocks VALUES (NULL, '2312341234', 'block_1')")
        self.blockdb.conn.commit()
        self.assertEqual(self.blockdb.get_latest(), 1)
        
    def test_add_block(self):
        """
        Uses the add_block method to add blocks and then fetches the blocks to 
        ensure they were correctly inserted
        """
        
        self.blockdb.add_block(self.block_a)
        self.blockdb.c.execute("SELECT * FROM blocks WHERE id = 1")
        self.assertEqual(self.blockdb.c.fetchone(), self.check_a)
        
        self.blockdb.add_block(self.block_b)
        self.blockdb.c.execute("SELECT * FROM blocks WHERE id = 2")
        self.assertEqual(self.blockdb.c.fetchone(), self.check_b)
        
    def test_get_block_by_hash(self):
        
        self.blockdb.add_block(self.block_a)
        self.blockdb.add_block(self.block_b)
        
        value = self.blockdb.get_block_by_hash(self.check_a[1])
        self.assertEqual(value, self.check_a)
        
        value = self.blockdb.get_block_by_hash(self.check_b[1])
        self.assertEqual(value, self.check_b)
    
    def test_get_from(self):
        
        # odd entries --> block_a , even entries --> block_b
        for i in range(10):
            self.blockdb.add_block(self.block_a)
            self.blockdb.add_block(self.block_b)
        
        start = 4
        iterator = self.blockdb.get_from(start)
        for num, entry in enumerate(iterator):
            id_ = start + num + 1
            
            if id_ % 2 != 0:
                check_a = (id_, self.check_a[1], f'block_{id_}')
                self.assertEqual(entry, check_a)
            else:
                check_b = (id_, self.check_b[1], f'block_{id_}')
                self.assertEqual(entry, check_b)


if __name__ == '__main__':
    unittest.main()
    
    
    


