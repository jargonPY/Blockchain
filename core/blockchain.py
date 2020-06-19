#!/usr/bin/env python3

import hashlib
import random
import datetime
import json
import os
from merkle import MerkleTree
    
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
        self.header_hash = self.header()
        
    def header(self):
        
        merkle_root = MerkleTree(self.trans).root
        data = merkle_root + self.prev_block_hash
        nonce, timestamp = self.proof_of_work(data)
        self.create_block(merkle_root, nonce, timestamp)
    
    def proof_of_work(self, data):
        
        hashed = None
        while hashed[:len(self.diff)] != self.diff:
            nonce = random.getrandbits(32)
            timestamp = datetime.datetime.now().isoformat()
            data += nonce + timestamp
            hashed = NewBlock.sha(data)
        return nonce, timestamp
    
    def create_block(self, root, nonce, time):
        """
        root : string
            a hash value of the root of the merkle tree
        nonce : int
            a value used for mining (source of 'randomness' for the cryptographic hash puzzle)
        time : datetime
            timestamp for when the puzzle was completed and the block was created
        
        Saves a json file containing the block --> header and transactions
        """
        
        data = {
                "header": {
                    "prev_block_hash": self.prev_block_hash,
                    "merkle_root": root,
                    "timestamp": time,
                    "nonce": nonce,
                    "difficulty_target": self.diff
                },
                "transactions": self.trans
            }
        
        block_num = NewBlock.get_block_num()
        path = os.getcwd() + "/blocks" + f"/block_{block_num}.json"
        with open(path, "w") as file:
            json.dump(data, file)
    
    @staticmethod
    def get_block_num():
        
        with open(os.getcwd() + "/blocks" + "/counter.txt") as f:
            block_num = int(f.read())
        return block_num
            
    @staticmethod
    def sha(data):
        
        hashed = hashlib.sha256(data.encode())
        return hashed
        





    
    
    
    
        
        