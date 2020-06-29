#!/usr/bin/env python3

import hashlib
import random
import datetime
import json
import os
from core.merkle import MerkleTree
from core.sha import sha
    
class NewBlock():
    
    def __init__(self, prev_block_hash, transactions, diff='0'):
        """
        prev_block_hash : string
            Hash of the header of the previous block in the chain
        transactions : list
            A list of all transactions being mined in the current block
        diff : string
            difficulty of the hash puzzle, the number of zeroes 
        """
        
        self.prev_block_hash = prev_block_hash
        self.trans = transactions
        self.diff = diff
        self.block = self.header()
        
    def header(self):
        
        #merkle_root = MerkleTree(self.trans).root
        merkle_root = "1"
        header = self.proof_of_work(merkle_root)
        block = self.create_block(header)
        return block
    
    def proof_of_work(self, merkle_root):
        
        hashed = "1" * len(self.diff)
        while hashed[:len(self.diff)] != self.diff:
            header = {
                        "prev_block_hash": self.prev_block_hash,
                        "merkle_root": merkle_root,
                        "timestamp": str(datetime.datetime.now().isoformat()),
                        "nonce": str(random.getrandbits(32)),
                        "difficulty_target": self.diff
                     }
            hashed = sha(json.dumps(header))
        return header
    
    def create_block(self, header):
        """
        header : dict
            containing the proof-of-work and all header data
            
        return : dict
            returns a dict object containing the block
        """
        
        data = {
                "header": header,
                "transactions": self.trans
            }
        
        return data



