#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import json
import os
import sys
from Crypto.PublicKey import RSA

currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from core.blockchain import NewBlock
from core.sha import sha
from core.utxo import UTXO
from core.blockdb import Blockdb
from core.pool import TransactionPool
from core.verify import Verify

from Crypto.PublicKey import RSA
def gen_keys():
        
    key = RSA.generate(1024)
    return key
    
def gen_sig(key, trans):
        
    byte_id = bytes.fromhex(trans['txid'])
    sig = key.sign(byte_id, 32)
    return sig

key1 = gen_keys()
with open(parentdir + "/core" + "/key.pem") as f:
    key2 = RSA.importKey(f.read())

""" First transaction for first block """
trans1 = {
          "vin": [None], # First transaction
                       
          "vout":[{
                      "amount": 100.0,
                      "address": key2.publickey().exportKey().decode()
                  }]
          }

trans1["txid"] = sha(json.dumps(trans1))

""" Transaction for second block """
trans2 = {
          "vin": [{
                      "txid": trans1["txid"],
                      "change": 0,
                      "sig": gen_sig(key2, trans1)
                  }],
                       
          "vout":[{
                      "amount": 90.0,
                      "address": key1.publickey().exportKey().decode()
                  },
              
                  {
                      "amount": 10.0,
                      "address": key2.publickey().exportKey().decode()
                  }]
          }

trans2["txid"] = sha(json.dumps(trans2))


block1 = {
             "header": {
                            "prev_block_hash": None,
                            "merkle_root": None,
                            "timestamp": None,
                            "nonce": None,
                            "difficulty_target": "0"
                       },
             "transactions": [trans1]
         }
        
block2 = NewBlock(sha(json.dumps(block1['header'])), [trans2]).block

    
    
utxo = UTXO()
blockdb = Blockdb()
pool = TransactionPool()


blockdb.add_block(block1)
utxo.add_trans(block1['transactions'], sha(json.dumps(block1['header'])))

blockdb.add_block(block2)
utxo.add_trans(block2['transactions'], sha(json.dumps(block2)))
        






















                


