#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import json
import os
from merkle import MerkleTree

class Verify():
    
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
        
        valid_trans = True
        for trans in block['transactions']:
            t = self.verify_trans(trans)
            if t == False:
                valid_trans = False
                break
        
        if root and proof_work and prev_hash and valid_trans:
            return True
        else:
            return False
        
    def verify_root(self, block):
        
        given_root = block['header']['merkle_root']
        computed_root = MerkleTree(block['transactions']) # block['transactions'] should be a list
        
        if given_root == computed_root:
            return True
        else:
            return False
        
    def verify_pow(self, header):
        
        diff = header["difficulty_target"]
        hashed = Verify.sha(header)
        
        if hashed[:len(diff)] == diff:
            return True
        else:
            return False
    
    def verify_prev_block(self, header):
        
        path = os.getcwd() + "/blocks"
        with open(path + "/counter.txt") as f:
            block_num = int(f.read())
            
        with open(path + f"/block_{block_num}") as f:
            block = json.load(f)
            
        hashed = Verify.sha(block['header'])
        
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
            
        
    def get_prev_trans(self, txid, utxo): ######### HOW TO ACCESS UTXO
        ######### ASSUMPTION THAT ALL UNSPENT TRANSACTIONS ARE IN THE UTXO DATABASE
        """ 
        txid : string
            hash of the transaction to be retrieved
        utxo : object of UTXO
            allows to query utxo database to find the block where transaction
            is stored
        """
        
        block_num = utxo.get_by_txid(txid)[-1] 
        with open(os.getcwd() + "/blocks" + f"/block_{block_num}") as f:
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
        hashed = Verify.sha(trans)
        
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
            prev_trans = self.get_prev_trans(t['txid'])
            change = t['change']
            trans = prev_trans['vout'][change]
            sig = t['sig']
            n, e = trans['address']
            check = pow(sig, e, n)
            if check != t['txid']:
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
        
        for i in len(trans['vout']):
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
        
    def double_spend(self, trans, pool, utxo): ##### POOL SOMEHOW NEEDS TO BE INCORPORATED
        ##### ASSUMES TRANSACTION IS IN UTXO
        """
        -   check all transaction after the "input" transaction, ensure
            that no output has this transaction as input
        -   check current pool to ensure no other transaction has the same 
            input
        complexity: O(mn), m --> # of inputs, n --> # transactions to check
        """        
        
        path = os.getcwd() + "/blocks"
        with open(path + "/counter.txt") as f:
                end_block = int(f.read())
        # check block chain     
        txids, start = [ ], [ ]
        for t in trans['vin']: # vin is a list of dictionaries
            txids.append(t['txid'])
            start.append(utxo.get_by_txid(t['txid'])[-1])
            
        for block_num in range(min(start), end_block+1):
            with open(path + f"/block_{block_num}") as f:
                trans = json.load(f)['transactions']
                
            for t in trans:
                check = [i['txid'] for i in t['vin']]
                if any(ids in check for ids in txids):
                    return False
        # check pool
        for txid in txids:
            if pool.check_in_pool(txid):
                return False
        return True
        
    @staticmethod
    def sha(data):
        
        hashed = hashlib.sha256(data.encode())
        return hashed











