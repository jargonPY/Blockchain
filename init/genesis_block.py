#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os 
import sys
from Crypto.PublicKey import RSA

currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(os.path.abspath(currentdir))
sys.path.append(parentdir)

from core.utxo import UTXO
from core.blockdb import Blockdb
from core.sha import sha
import init_db

def create_block():
    
    with open(parentdir + "/core" + "/key.pem") as f:
        key = RSA.importKey(f.read())

    """ First transaction for first block """
    trans1 = {
              "vin": [None], # First transaction
                           
              "vout":[{
                          "amount": 1000000.0,
                          "address": key.publickey().exportKey().decode()
                      }]
              }
    trans1["txid"] = sha(json.dumps(trans1))
    
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
    
    utxo = UTXO()
    blockdb = Blockdb()
    
    blockdb.add_block(block1)
    utxo.add_trans(block1['transactions'], sha(json.dumps(block1['header'])))
    
if __name__ == "__main__":
    init_db.init_utxo()
    init_db.init_blocks()
    create_block()



