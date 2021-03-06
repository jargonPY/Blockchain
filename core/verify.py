#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
from Crypto.PublicKey import RSA
from core.sha import sha

currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from core.utxo import UTXO
from core.blockdb import Blockdb

class Verify():
    
    def __init__(self, pool):
        
        self.pool = pool
        self.utxo = UTXO()
        self.blockdb = Blockdb()
        self.path = parentdir + "/blocks"
        
    def get_block_num(self):
        """ make seperate method because block number is always changing """
        
        return self.blockdb.get_latest()
    
    def verify_block(self, block):
        """
        Valid block:
            - valid transactions
            - valid proof of work
            - valid merkle root
            - valid hash of previous block
        """
        
        root = self.verify_root(block)
        proof_work = self.verify_pow(block['header'])
        prev_hash = self.verify_prev_block(block['header'])
        
        for trans in block['transactions']:
            t = self.verify_trans(trans)
            if not t:
                return False
        if root and proof_work and prev_hash:
            return True
        else:
            return False
        
    def verify_root(self, block):
        
        given_root = block['header']['merkle_root']
        #computed_root = MerkleTree(block['transactions']) # block['transactions'] should be a list
        computed_root = "1"
        
        if given_root == computed_root:
            return True
        else:
            return False
        
    def verify_pow(self, header):
        
        diff = header["difficulty_target"]
        hashed = sha(json.dumps(header))
        if hashed[:len(diff)] == diff:
            return True
        else:
            return False
    
    def verify_prev_block(self, header):
        
        block_num = self.get_block_num()
        with open(self.path + f"/block_{block_num}.json") as f:
            block = json.load(f)
            
        hashed = sha(json.dumps(block['header']))
        if hashed == header['prev_block_hash']:
            return True
        else:
            return False
            
    def verify_trans(self, trans):
        """ 
        Valid transactions:
            - valid hash (txid)
            - input amount >= output amount
            - valid signatures
            - ensure transaction is not double spent
        """
        
        v_hash = self.verify_hash(trans)
        v_sig = self.verify_sig(trans)
        v_bal = self.verify_balance(trans)
        v_double = self.double_spend(trans)
            
        if v_hash and v_sig and v_bal and v_double:
            return True
        else:
            return False
            
        
    def get_prev_trans(self, txid):
        """ 
        txid : string
            hash of the transaction to be retrieved
        """
        
        block_hash = self.utxo.get_by_txid(txid)[-1]
        filename  = self.blockdb.get_block_by_hash(block_hash)[-1]
        with open(self.path + f"/{filename}") as f:
            trans = json.load(f)['transactions']
        
        for t in trans:
            if t['txid'] == txid:
                break
        return t
    
    def verify_hash(self, trans):
        """ trans : dict
                transaction data structure
                
            returns : boolean
                True if txid matches the hash of the transaction
        """
        
        tcopy = trans.copy()
        del tcopy['txid']
        hashed = sha(json.dumps(tcopy))
        
        if trans['txid'] == hashed:
            return True
        else:
            return False
    
    def verify_sig(self, trans):
        """ trans : dict
                transaction data structure
                
            returns : boolean
                True if all signatures match, False otherwise
        """
        
        for t in trans['vin']:
            sig = t['sig']
            pk = self.utxo.get_by_txid(t['txid'])[2] # (id, txid, address, change, amount, block)
            pk = RSA.importKey(pk)
            if not pk.verify(bytes.fromhex(t['txid']), sig):
                return False
        return True
        
    def verify_balance(self, trans):
        """ trans : dict
                transaction data structure
                
            returns : boolean
                True if all input > output, False otherwise
        """
        
        in_amount = 0
        out_amount = 0
        
        for i in range(len(trans['vout'])):
            out_amount += trans['vout'][i]['amount']
        
        for t in trans['vin']:
            prev_trans = self.get_prev_trans(t['txid'])
            change = t['change']
            trans = prev_trans['vout'][change]
            in_amount += trans['amount']

        if in_amount >= out_amount:
            return True
        else:
            return False
        
    def double_spend(self, trans):
        """
        -   check all transaction after the "input" transaction, ensure
            that no output has this transaction as input
        -   check current pool to ensure no other transaction has the same 
            input
        complexity: O(m) + O(n), m --> # of inputs, n --> # of transactions to check
        """        
        
        # check block chain     
        txids, start = [ ], [ ]
        for t in trans['vin']: # vin is a list of dictionaries
            txids.append(t['txid'])
            block_hash = self.utxo.get_by_txid(t['txid'])[-1]
            block_num = self.blockdb.get_block_by_hash(block_hash)[0]
            start.append(block_num)
        
        end_block = self.get_block_num()
        for block_num in range(min(start), end_block+1):
            if min(start) == 1: continue ## The genesis block is skipped
            with open(self.path + f"/block_{block_num}.json") as f:
                trans = json.load(f)['transactions']
            
            for t in trans:
                check = [i['txid'] for i in t['vin']]
                print("txids: ", txids)
                print("CHECK: ", check)
                if any(ids in check for ids in txids):
                    return False
        # check pool
        for txid in txids:
            if self.pool.check_in_pool(txid):
                return False
        return True
            
    
    
    
    
    





