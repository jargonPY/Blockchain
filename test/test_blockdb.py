#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import unittest
from core.blockdb import Blockdb

class BlockdbClone(Blockdb):
    
    def __init__(self):
      
        self.conn = sqlite3.connect(":memory:")
        self.c = self.conn.cursor()
        
        self.c.execute("""CREATE TABLE blocks (
                    id INTEGER PRIMARY KEY,
                    hash TEXT
                    )""")
        
        self.conn.commit()

class BlockdbTestCase(unittest.TestCase):
    
    blockdb = BlockdbClone()
    block_a = None
    block_b = None
    
    def test_add_block(self):
        
        pass
    
    def test_get_block_by_hash(self):
        
        pass
    
    def test_get_latest(self):
        
        pass
    
    def test_get_from(self):
        
        pass


