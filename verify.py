#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib

class Verify():
    
    def verify_block(self, block):
        
        pass
    
    def verify_trans(self, trans):
        """ 
        Valid transactions:
            - valid hash (txid)
            - input amount > output amount
            - valid signatures
        """
        
        v_hash = self.verify_hash(trans)
        v_sig = self.verify_sig(trans)
        v_bal = self.verify_balance(trans)
            
        if v_hash and v_sig and v_bal:
            return True
        else:
            return False
            
        
    def get_prev_trans(self, txid):
        """ HOW TO ACCESS PREVIOUS TRANSACTIONS??? """
        pass
    
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
        
    @staticmethod
    def sha(data):
        
        hashed = hashlib.sha256(data.encode())
        return hashed

