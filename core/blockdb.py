#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sqlite3
from core.sha import sha

currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)

"""
All blocks are added to Blockdb even local one, this will also automatically save the block
in a corresponding file

Blockdb is an append only database
"""

class Blockdb():
    
    def __init__(self):
        
        self.conn = sqlite3.connect(parentdir + "/databases" + "/blocks.db")
        self.c = self.conn.cursor()

    def add_block(self, block):
        
        block_hash = sha(json.dumps(block['header']))
        # check if block is already saved
        get_block = self.get_block_by_hash(block_hash)
        if get_block != None:
            return None
        
        block_num = self.get_latest()
        if block_num == None:
            block_num = 1
        else:
            block_num += 1
        
        
        file = f"/block_{block_num}.json"
        # save the block as a file
        with open(parentdir + "/blocks" +  file, "w") as f:
            json.dump(block, f)
        
        # add block to hash-table database
        with self.conn:
            self.c.execute("INSERT INTO blocks VALUES (NULL, :hash, :file)", {'hash':block_hash, 'file':f'block_{block_num}.json'})

    def get_block_by_hash(self, block_hash):
        
        self.c.execute(f"SELECT * FROM blocks WHERE hash = '{block_hash}'")
        return self.c.fetchone()
    
    def get_latest(self):
        """
        return : int
            the id of the lastest entry in the database
        """
        
        self.c.execute("SELECT max(id) FROM blocks")
        return self.c.fetchone()[0]
        
    def get_from(self, primary_key):
        """
        primary_key : int
            the primary key identifier of the block in the database
        
        returns : cursor (iterable)
            an iterable object where each iteration will return an entry from the db
        """
        
        self.c.execute(f"SELECT * FROM blocks WHERE ID > {primary_key}")
        return self.c.fetchall()