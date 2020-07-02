#!/usr/bin/env python3

import random
import datetime
import json
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
        self.block = self.create_block()
    
    def merkle_root(self, leaves):

        num_leaves = len(leaves)
        if num_leaves == 1:
            if type(leaves[0]) == dict: # For blocks with a single transaction
                return sha(json.dumps(leaves[0]))
            else:
                return leaves[0]
        
        parent = [ ]
        i = 0
        while i < num_leaves:
            left = sha(json.dumps(leaves[i]))
            if (i + 1) < num_leaves:
                right = sha(json.dumps(leaves[i + 1]))
            else:
                right = sha(json.dumps(leaves[i]))
                
            parent.append(sha(left + right))
            i += 2
        return self.merkle_root(parent)
    
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
    
    def create_block(self):
        """
        return : dict
            returns a dict object containing the block
        """
        
        merkle_root = self.merkle_root(self.trans)
        header = self.proof_of_work(merkle_root)
        
        block = {
                "header": header,
                "transactions": self.trans
            }
        
        return block



