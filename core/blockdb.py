#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import json
import os
import sqlite3
from sha import sha

"""
All blocks are added to Blockdb even local one, this will also automatically save the block
in a corresponding file

Blockdb is an append only database
"""

class Blockdb():
    
    def __init__(self):
        
        self.conn = sqlite3.connect("blocks.db")
        self.c = self.conn.cursor()

    def add_block(self, block):
        
        block_num = self.get_latest()[0] + 1 
        file = f"/block_{block_num}.json"
        # save the block as a file
        with open(os.getcwd() + "/blocks" +  file, "w") as f:
            json.dump(block, f)
        
        block = sha(block)
        # add block to hash-table database
        with self.conn:
            self.c.execute("INSERT INTO blocks VALUES (:file, :hash)", {'file':file, 'hash':block})

    def get_block_by_hash(self, block_hash):
        
        self.c.execute(f"SELETCT * FROM blocks WHERE hash={block_hash}")
        self.c.fetchone()
    
    def get_latest(self):
        """
        return : tuple
            the lastest entry in the database
        """
        
        self.c.execute("SELECT max(id) FROM blocks")
        self.c.fetchone()
        
    def get_from(self, primary_key):
        """
        primary_key : int
            the primary key identifier of the block in the database
        
        returns : cursor (iterable)
            an iterable object where each iteration will return an entry from the db
        """
        
        self.c.execute(f"SELECT * FROM blocks WHERE ID > {primary_key}")
        return self.c