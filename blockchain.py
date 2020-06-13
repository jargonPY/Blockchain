#!/usr/bin/env python3

import hashlib
import random
import datetime
import json
from merkle import MerkleTree
    
class NewBlock():
    
    def __init__(self, prev_block_hash, transactions):
        """
        prev_block_hash : string
            Hash of the header of the previous block in the chain
        transactions : list
            A list of all transactions being mined in the current block
        """
        
        self.prev_block_hash = prev_block_hash
        self.trans = transactions
        self.header_hash = self.header()
        
    def header(self):
        
        merkle_root = MerkleTree(self.trans).root
        data = merkle_root + self.prev_block_hash
        nonce, timestamp = self.proof_of_work(data)
        self.create_block(merkle_root, nonce, timestamp)
    
    def proof_of_work(self, data):
        
        hashed = None
        while hashed[0] != 0:
            nonce = random.getrandbits(32)
            timestamp = datetime.datetime.now().isoformat()
            data += nonce + timestamp
            hashed = NewBlock.sha(data)
        return nonce, timestamp
    
    def create_block(self, root, nonce, time):
        
        data = {
                "prev_block_hash": self.prev_block_hash,
                "merkle_root": root,
                "timestamp": time,
                "nonce": nonce,
                "difficulty_target": None,
                "transactions":self.trans
            }
        with open("block.json", "w") as file:
            json.dump(data, file)
            
    @staticmethod
    def sha(data):
        
        hashed = hashlib.sha256(data.encode())
        return hashed
        
        

    
class UTXO():
    
    pass

    
class TransactionPool():
    
    pass



    
    
    
    
    
        
        